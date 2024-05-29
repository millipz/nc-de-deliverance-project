# retrieve_processed_data


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
    

# write_table_data_to_warehouse


    Write pandas dataframe to database

    Args:
        data_frame (pd.DataFrame)
        table_name (string)
        db (pg8000 Connection)

    Returns:
        response: database response
    

# create_dim_date


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
    

