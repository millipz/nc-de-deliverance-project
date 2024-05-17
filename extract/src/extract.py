# TODO remove below and run checks  when ready
# flake8: noqa
from datetime import datetime, date
import json


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
        return timestamp

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
            Description=f"Latest timestamp of data ingested from Totesys database for {table_name} table",
            Value=timestamp.isoformat(),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The timestamp could not be written: {e}")


def collect_table_data(
    table_name: str,
    timestamp: datetime,
    db_conn,
) -> list[dict]:
    """
    Returns all data from a table newer than most recent timestamp

    Args:
        table_name (string)
        timestamp (timestamp)
        db_conn (pg8000 database connection)

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store


    Returns:
        table_data (list) : list of dictionaries all data in table, one dictionary per row keys will be column headings
    """
    pass


def find_latest_timestamp(
    table_data: list[dict],
    columns=["last_updated"],
) -> datetime:
    """

    Iterates over data from one database table and returns the most recent timestamp

    Args:
        table_data (list) : list of dictionaries representing rows of the table
        columns (list[str], optional keyword) : columns to search for timestamps. Defauts to ["last_updated"]

    Raises:
        KeyError: columns do not exist

    Returns:
        most_recent_timestamp (timestamp) : from list returns most recent timestamp from created_at/updated_at values
    """
    timestamps = []
    for dic in table_data:
        for col in columns:
            timestamps.append(dic[col])
    return max(timestamps)


def write_table_data_to_s3(
    table_name: str,
    table_data: list[dict],
    bucket_name: str,
    sequential_id: int,
    s3_client,
) -> None:
    """
    Write file to S3 bucket as Json lines format

    Args:
        table_name (string)
        table_data (list) : list of dictionaries all data in table, one dictionary per row keys will be column headings
        s3_client (boto3 s3 client)


    Raises:
        FileExistsError: S3 object already exists with the same name
        ConnectionError : connection issue to S3 bucket

    Returns:
        None
    """
    encoded_data = json.dumps(table_data, indent=4, sort_keys=True, default=str).encode(
        "utf-8"
    )
    time_format = "%H%M%S%f"
    key = f"{date.today()}/{table_name}_{str(sequential_id).zfill(8)}_{datetime.now().strftime(time_format)}.jsonl"
    s3_client.put_object(Body=encoded_data, Bucket=bucket_name, Key=key)


def get_seq_id(table_name: str, ssm_client) -> int:
    """
    From parameter store retrieves table_name : sequential_id key value pair

    Args:
        table_name (string)


    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        sequential_id(int)

    """
    try:
        response = ssm_client.get_parameter(Name=(table_name + "_latest_packet_id"))
        id = response["Parameter"]["Value"]
        return int(id)

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(f"Table name '{table_name}' does not have any recorded packets.")

    # TODO connection errors should be checked when connecting with
    # credentials so this might not be needed here
    # except (ssm_client.exceptions.ConnectionError):
    #     raise ConnectionError("Connection issue to Parameter Store.")


def write_seq_id(seq_id: int, table_name: str, ssm_client) -> None:
    """

    To parameter store write table_name : sequential_id key value pair
    -- checks sequential_id is one greater than previous sequential_id

    Args:
        table_name (string)
        sequential_id(int)


    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    try:
        print("writing ")
        ssm_client.put_parameter(
            Name=f"{table_name}_latest_packet_id",
            Description=f"Latest packet_id of data ingested from Totesys database for {table_name} table",
            Value=str(seq_id),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The timestamp could not be written: {e}")
