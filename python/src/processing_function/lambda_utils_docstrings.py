def retrieve_data(bucket_name: str, object_key: str, s3_client):
    """
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
    """
    pass


def transform_sales_order(sales_order_df):
    """
    Transform loaded sales order data into star schema
        - splits out time and date data into seperate columns
        - renames staff_id to sales_staff_id
        - removes unwanted columns

    Args:
        sales_order_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    pass


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
    pass


def transform_staff(staff_df, department_df):
    """
    Transform loaded staff order data into star schema
        - adds a location by reference to department table

    Args:
        staff_df (pandas dataframe): original data
        department_df (pandas dataframe): department data for location

    Returns:
        data (pandas dataframe): transformed data
    """
    pass


def transform_location(address_df):
    """
    Transform loaded address order data into star schema
        - renames address_id to location_id

    Args:
        address_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    pass


def transform_currency(currency_df):
    """
    Transform loaded currency data into star schema
        - adds currency names from currency codes
        - remove unwanted last_updated column

    Args:
        currency_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    pass


def transform_design(design_df):
    """
    Transform loaded design data into star schema
        - remove unwanted columns

    Args:
        design_df (pandas dataframe): original data

    Returns:
        data (pandas dataframe): transformed data
    """
    pass


def transform_counterparty(counterparty_df, address_df):
    """
    Transform loaded counterparty data into star schema
        - lookup address in address data and add to table
        - renames columns to suit star schema
        - removes unwanted columns

    Args:
        counterparty_df (pandas dataframe): original data
        address_df (pandas dataframe): address data for reference

    Returns:
        data (pandas dataframe): transformed data
    """
    pass


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
    pass


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
    pass


def write_table_data_to_s3(
    dict_name: dict,
    bucket_name: str,
    packet_id: int,
    s3_client,
) -> None:
    """
    Write file to S3 bucket in Parquet format

    Args:
        table_name (string)
        table_data (list) : list of dictionaries all data in table,
            one dictionary per row keys will be column headings
        bucket_name (string)
        packet_id (string)
        s3_client (boto3 s3 client)

    Raises:
        FileExistsError: S3 object already exists with the same name
        ConnectionError : connection issue to S3 bucket

    Returns:
        None
    """
