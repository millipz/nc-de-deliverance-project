from datetime import datetime


def retrieve_timestamp(table_name: str, ssm_client) -> datetime:
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
        response = ssm_client.get_parameter(Name=(table_name + "_latest_extracted"))

        timestamp = response["Parameter"]["Value"]
        return timestamp

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(f"Table name '{table_name}' does not exist.")

    # TODO connection errors should be checked when connecting with
    # credentials so this might not be needed here
    # except (ssm_client.exceptions.ConnectionError):
    #     raise ConnectionError("Connection issue to Parameter Store.")


def write_timestamp(timestamp: datetime, table_name: str, ssm_client):
    """

    Writes timestamp to parameter store for given table

    Args:
        timestamp (timestamp) : timestamp of latest extracted data
        table_name (str) : table name to store timestamp for
        client (boto3 SSM Client) : avoid recreating for each invocation

    Raises:
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    try:
        ssm_client.put_parameter(
            Name=f"{table_name}_latest_extracted",
            Description=f"Latest timestamp ingested data for {table_name}",
            Value=timestamp.isoformat(),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The timestamp could not be written: {e}")


def collect_table_data(table_name: str, timestamp: datetime, db_conn):
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
        table_data (list) : list of dictionaries all data in table,
        one dictionary per row keys will be column headings
    """

    """

        Collect data from one database table()
            returns the most recent timestamp

        Args:
            table_data (list) : list of dictionaries

        Raises:
            KeyError: created_at/updated_at does not exist



        Returns:
            most_recent_timestamp (timestamp):
                from list returns most recent timestamp
        """

    """

        Write file to S3 bucket as Json lines format

        Args:
            table_name (string)
            most_recent_timestamp (timestamp) :
                timestamp of most recent records in data
            table_data (list) : list of dictionaries all data in table,
                one dictionary per row keys will be column headings
            sequential_id (int) : integer stored in parameter store
                retrieved earlier in application flow


        Raises:
            FileExistsError: S3 object already exists with the same name
            ConnectionError : connection issue to S3 bucket

        Returns:
            None
        """

    """

        From parameter store retrieves table_name :
            sequential_id key value pair

        Args:
            table_name (string)


        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store

        Returns:
            sequential_id(int)

        """

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
