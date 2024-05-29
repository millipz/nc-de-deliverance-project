# retrieve_data


    Load data from an s3 object (json lines) into a pandas dataframe

    Args:
        bucket_name (str): bucket where the object is stored
        object_key (str): key of data object
        client (boto3 s3 Client)

    Raises:
        KeyError: table_name does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        data: pandas dataframe
    

# transform_sales_order


    Transform loaded sales order data into star schema
        - splits out time and date data into separate columns
        - renames staff_id to sales_staff_id
        - removes unwanted columns

    Args:
        sales_order_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    

# transform_purchase_order


    Transform loaded purchase order data into star schema
        - splits out time and date data into separate columns
        - removes unwanted columns

    Args:
        purchase_order_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    

# transform_payment


    Transform loaded payment data into star schema
        - splits out time and date data into separate columns
        - renames columns to suit star schema

    Args:
        payment_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    

# transform_staff


    Transform loaded staff order data into star schema
        - adds a location by reference to department table

    Args:
        staff_df (pandas dataframe): original data
        department_df (pandas dataframe): department data for location

    Returns:
        data (pandas dataframe): transformed data
    

# transform_location


    Transform loaded address order data into star schema
        - renames address_id to location_id

    Args:
        address_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    

# transform_payment_type


    Transform loaded payment type data into star schema

    Args:
        payment_type_df (pandas dataframe)

    Returns:
        data (pandas dataframe): transformed data
    

# transform_transaction


    Transform loaded transaction data into star schema

    Args:
        transaction_df (pandas dataframe): original write_data_to_s3

    Returns:
        data (pandas dataframe): transformed data
    

# transform_currency


    Transform loaded currency data into star schema
        - adds currency names from currency codes
        - remove unwanted last_updated column

    Args:
        currency_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    

# transform_design


    Transform loaded design data into star schema
        - remove unwanted columns

    Args:
        design_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    

# transform_counterparty


    Transform loaded counterparty data into star schema
        - lookup address in address data and add to table
        - renames columns to suit star schema
        - removes unwanted columns

    Args:
        counterparty_df (pandas dataframe): original data
        address_df (pandas dataframe): address data for reference

    Returns:
        data (pandas dataframe): transformed data
    

# write_data_to_s3


    Write dataframe to S3 bucket in Parquet format

    Args:
        df (pd.DataFrame): DataFrame to write
        table_name (string)
        bucket_name (string)
        packet_id (string)
        s3_client (boto3 s3 client)

    Raises:
        FileExistsError: S3 object already exists with the same name
        ConnectionError : connection issue to S3 bucket

    Returns:
        key: The S3 object key the data is written to
    

