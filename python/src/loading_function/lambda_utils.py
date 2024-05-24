from pg8000.native import identifier, literal, Connection
import pandas as pd
import io
from datetime import datetime


def retrieve_processed_data(
    bucket_name: str, object_key: str, s3_client
) -> pd.DataFrame:
    """
    Retrieves parquet data from s3 bucket, given a key

    Args:
        bucket_name (string)
        object_key (string)
        s3_client (boto3 s3 client)

    Raises:
        KeyError: object does not exist
        ConnectionError : connection issue to parameter store


    Returns:
        table_data (pandas dataframe)
    """
    obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    return pd.read_parquet(io.BytesIO(obj["Body"].read()))


def write_table_data_to_warehouse(
    data_frame: pd.DataFrame,
    table_name: str,
    db: Connection,
) -> dict:
    """
    Write pandas dataframe to database

    Args:
        data_frame (pd.DataFrame)
        table_name (string)
        db (pg8000 Connection)

    Returns:
        response: database response
    """

    rows = data_frame.values.tolist()
    print(rows)
    processed_rows = []
    for row in rows:
        values = [literal(v) for v in row]
        row_string = ", ".join(values)
        processed_rows.append(f"({row_string})")

    vals_string = ",".join(processed_rows)
    print(vals_string)



    query = (
        f"INSERT INTO {identifier(table_name)} "
        f"({', '.join(data_frame.columns)}) "
        f"VALUES {vals_string} "
        "ON CONFLICT DO NOTHING;"
    )

    print(query)

    response = db.run(query)
    return response


def create_dim_date(start_date, end_date):
    """
    Creates a table of dates in the given range
    with columns for:
        - year
        - month
        - month name
        - day of month
        - day of year
        - day of week
        - quarter


    Args:
        start_date (datetime)
        end_date (datetime)

    Returns:
        dates (pandas dataframe)
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    dim_date = pd.DataFrame(date_range, columns=["date_id"])
    dim_date["year"] = dim_date["date_id"].dt.year
    dim_date["month"] = dim_date["date_id"].dt.month
    dim_date["day"] = dim_date["date_id"].dt.day
    dim_date["day_of_week"] = dim_date["date_id"].dt.weekday
    dim_date["day_name"] = dim_date["date_id"].dt.day_name()
    dim_date["month_name"] = dim_date["date_id"].dt.month_name()
    dim_date["quarter"] = dim_date["date_id"].dt.quarter
    return dim_date


def get_timestamp(table_name: str, ssm_client) -> datetime:
    """
    Return timestamp showing most recent entry from the given table
    that has been processed by the ingestion lambda.

    Args:
        table_name (str): table name to get timestamp for
        client (boto3 SSM Client)

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        timestamp (datetime timestamp) : stored timestamp of most recent
        ingested data for given table
    """
    try:
        response = ssm_client.get_parameter(
            Name=(table_name + "_latest_extracted_timestamp")
        )

        timestamp = response["Parameter"]["Value"]
        return datetime.fromisoformat(timestamp)

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(
            f"Table name '{table_name}' does not have any recorded latest data."
        )

    # TODO connection errors should be checked when connecting with
    # credentials so this might not be needed here
    # except (ssm_client.exceptions.ConnectionError):
    #     raise ConnectionError("Connection issue to Parameter Store.")


def write_timestamp(timestamp: datetime, table_name: str, ssm_client) -> None:
    """

    Writes timestamp to parameter store for given table

    Args:
        timestamp (timestamp) : timestamp of latest extracted data
        table_name (str) : table name to store timestamp for
        client (boto3 SSM Client) : client passed in to avoid recreating for each invocation

    Raises:
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    try:
        ssm_client.put_parameter(
            Name=f"{table_name}_latest_extracted_timestamp",
            Type="String",
            Description=(
                "Latest timestamp of data ingested"
                f"from Totesys database for {table_name} table"
            ),
            Value=timestamp.isoformat(timespec="milliseconds"),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The timestamp could not be written: {e}")
