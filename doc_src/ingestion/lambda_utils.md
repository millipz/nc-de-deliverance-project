# get_timestamp


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
    

# write_timestamp



    Writes timestamp to parameter store for given table

    Args:
        timestamp (timestamp) : timestamp of latest extracted data
        table_name (str) : table name to store timestamp for
        client (boto3 SSM Client) : client passed in to avoid recreating for each invocation

    Raises:
        ConnectionError : connection issue to parameter store

    Returns:
        None
    

# collect_table_data


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
    

# find_latest_timestamp



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
    

# write_table_data_to_s3


    Write file to S3 bucket as Json lines format

    Args:
        table_name (string)
        table_data (list) : list of dictionaries all data in table,
            one dictionary per row keys will be column headings
        s3_client (boto3 s3 client)


    Raises:
        FileExistsError: S3 object already exists with the same name
        ConnectionError : connection issue to S3 bucket

    Returns:
        key (str): The S3 object key the data is written to
    

# get_seq_id


    From parameter store retrieves table_name : sequential_id key value pair

    Args:
        table_name (string)


    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        sequential_id(int)

    

# write_seq_id



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
    

