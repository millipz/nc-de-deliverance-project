import boto3


def retrieve_timestamps(table_name):
    """
    Return a dictionary with timestamps showing most recent entry from the OLTP database that has been processed
    by the ingestion lambda.
    -- awaiting looking at data in database to confirm how created and updated timestamps are processed

    Args:
        table_name (str): table name to get timestamp for

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        timestamp (datetime timestamp) : stored timestamp of most recent ingested data for given table
    """
    try:
        ssm_client = boto3.client("ssm")

        response = ssm_client.get_parameter(Name=table_name)

        timestamp = response["Parameter"]["Value"]
        return timestamp

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(f"Table name '{table_name}' does not exist.")

    # TODO connection errors should be checked when connecting with credentials so this might not be needed here
    # except (ssm_client.exceptions.ConnectionError):
    #     raise ConnectionError("Connection issue to Parameter Store.")
