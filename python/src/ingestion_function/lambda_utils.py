from datetime import datetime, date
import json
from pg8000.native import identifier, literal


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
            Name=("/ingestion/" + table_name + "/latest_extracted_timestamp")
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
            Name=f"/ingestion/{table_name}/latest_extracted_timestamp",
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


def collect_table_data(
    table_name: str, timestamp: datetime, db_conn, column="last_updated"
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
        table_data (list) : list of dictionaries
            all data in table, one dictionary
            per row keys will be column headings
    """
    sql_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    query = (
        f"SELECT * FROM {identifier(table_name)} "
        f"WHERE {identifier(column)} > {literal(sql_timestamp)}"
    )
    data = db_conn.run(query)
    headings = [column["name"] for column in db_conn.columns]
    result = [dict(zip(headings, row)) for row in data]
    return result


def find_latest_timestamp(
    table_data: list[dict],
    columns=["last_updated"],
) -> datetime:
    """

    Iterates over data from one database table and returns the most recent timestamp

    Args:
        table_data (list) : list of dictionaries representing rows of the table
        columns (list[str], optional keyword) : columns to search for timestamps.
            Defauts to ["last_updated"]

    Raises:
        KeyError: columns do not exist

    Returns:
        most_recent_timestamp (timestamp) : from list returns most recent
            timestamp from created_at/updated_at values
    """
    timestamps = []
    for dic in table_data:
        print(f"checking {dic}")
        for col in columns:
            print(f"checking {col}")
            timestamps.append(dic[col])
            print(f"==>> dic[col]: {dic[col]}")

    try:
        return max(timestamps)
    except ValueError:
        return None


def write_table_data_to_s3(
    table_name: str,
    table_data: list[dict],
    bucket_name: str,
    packet_id: int,
    s3_client,
) -> None:
    """
    Write file to S3 bucket in JSON Lines format

    Args:
        table_name (string)
        table_data (list): list of dictionaries all data in table,
            one dictionary per row keys will be column headings
        bucket_name (string)
        packet_id (string)
        s3_client (boto3 s3 client)

    Raises:
        FileExistsError: S3 object already exists with the same name
        ConnectionError: connection issue to S3 bucket

    Returns:
        None
    """
    encoded_data = json.dumps(table_data, indent=4, sort_keys=True, default=str).encode(
        "utf-8"
    )
    time_format = "%H%M%S%f"
    key = (
        f"{date.today()}/{table_name}_"
        f"{str(packet_id).zfill(8)}_"
        f"{datetime.now().strftime(time_format)}.jsonl"
    )
    s3_client.put_object(Body=encoded_data, Bucket=bucket_name, Key=key)


def get_packet_id(table_name: str, ssm_client) -> int:
    """
    From parameter store retrieves table_name : packet_id key value pair

    Args:
        table_name (string)


    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        packet_id(int)

    """
    try:
        response = ssm_client.get_parameter(Name=("/ingestion/"+table_name+"/latest_packet_id"))
        id = response["Parameter"]["Value"]
        return int(id)

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(f"Table name '{table_name}' does not have any recorded packets.")

    # TODO connection errors should be checked when connecting with
    # credentials so this might not be needed here
    # except (ssm_client.exceptions.ConnectionError):
    #     raise ConnectionError("Connection issue to Parameter Store.")


def write_packet_id(packet_id: int, table_name: str, ssm_client) -> None:
    """

    Write table_name : packet_id key value pair to Parameter Store

    Args:
        table_name (string)
        packet_id(int)

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    try:
        print("writing ")
        ssm_client.put_parameter(
            Name=f"/ingestion/{table_name}/latest_packet_id",
            Type="String",
            Description=(
                "Latest packet_id of data ingested "
                f"from Totesys database for {table_name} table"
            ),
            Value=str(packet_id),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The packet ID could not be written: {e}")
