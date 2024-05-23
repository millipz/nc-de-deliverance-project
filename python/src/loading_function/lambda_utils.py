from pg8000.native import identifier, literal, Connection
import pandas as pd
import io


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

    rows = data_frame.to_string(header=False, index=False, index_names=False).split(
        "\n"
    )
    print(rows)
    processed_rows = []
    for row in rows:
        values = row.split()
        values = [literal(v) for v in values]
        row_string = ", ".join(values)
        processed_rows.append(f"({row_string})")

    vals_string = ",".join(processed_rows)
    print(vals_string)

    query = (
        f"INSERT INTO {identifier(table_name)} "
        f"({', '.join(data_frame.columns)}) "
        f"VALUES {vals_string};"
    )

    print(query)

    response = db.run(query)
    return response
