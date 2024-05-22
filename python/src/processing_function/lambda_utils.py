import pandas as pd
import json


def retrieve_data(bucket_name: str, object_key: str, s3_client):

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        data = json.loads(response["Body"].read().decode('utf-8'))
        df = pd.DataFrame(data)
        return df

    except s3_client.exceptions.NoSuchKey:
        raise KeyError(f"The key '{object_key}' does not exist.")


# def transform_to_star_schema(sales_order_df, staff_df,
# address_df, currency_df, design_df, counterparty_df):


def transform_sales_order(sales_order_df):
    fact_sales_order = sales_order_df.copy()

    fact_sales_order['created_date'] = pd.to_datetime(fact_sales_order['created_at']).dt.date
    fact_sales_order['created_time'] = pd.to_datetime(fact_sales_order['created_at']).dt.time
    fact_sales_order['last_updated_date'] = \
        pd.to_datetime(fact_sales_order['last_updated']).dt.date
    fact_sales_order['last_updated_time'] = \
        pd.to_datetime(fact_sales_order['last_updated']).dt.time

    fact_sales_order.rename(columns={
        'staff_id': 'sales_staff_id',
    }, inplace=True)

    fact_sales_order = fact_sales_order[[
        'sales_order_id',
        'created_date',
        'created_time',
        'last_updated_date',
        'last_updated_time',
        'sales_staff_id',
        'counterparty_id',
        'units_sold',
        'unit_price',
        'currency_id',
        'design_id',
        'agreed_payment_date',
        'agreed_delivery_date',
        'agreed_delivery_location_id']]

    return fact_sales_order


def create_dim_date(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    dim_date = pd.DataFrame(date_range, columns=['date_id'])
    dim_date['year'] = dim_date['date_id'].dt.year
    dim_date['month'] = dim_date['date_id'].dt.month
    dim_date['day'] = dim_date['date_id'].dt.day
    dim_date['day_of_week'] = dim_date['date_id'].dt.weekday
    dim_date['day_name'] = dim_date['date_id'].dt.day_name()
    dim_date['month_name'] = dim_date['date_id'].dt.month_name()
    dim_date['quarter'] = dim_date['date_id'].dt.quarter
    return dim_date


def transform_staff(staff_df, department_df):
    dim_staff = staff_df.copy()
    dim_staff = dim_staff.merge(department_df[['department_id', 'department_name', 'location']],
                                on='department_id', how='left')
    return dim_staff


def transform_location(address_df):
    dim_location = address_df.copy()
    dim_location = dim_location.rename(columns={
        'address_id': 'location_id'    
        })
    return dim_location


def transform_currency(currency_df):
    dim_currency = currency_df.copy()
    dim_currency['currency_name'] = dim_currency['currency_code'].apply(lambda x: 'Unknown')
    return dim_currency


def transform_design(design_df):
    dim_design = design_df.copy()
    return dim_design[[
        'design_id', 'design_name', 'file_location', 'file_name'
    ]]


def transform_counterparty(counterparty_df, address_df):
    dim_counterparty = counterparty_df.copy()
    dim_counterparty = dim_counterparty.merge(address_df, left_on='legal_address_id',
                                              right_on='address_id', how='left')
    dim_counterparty = dim_counterparty.rename(columns={
        'counterparty_id': 'counterparty_id',
        'counterparty_legal_name': 'counterparty_legal_name',
        'address_line_1': 'counterparty_legal_address_line_1',
        'address_line_2': 'counterparty_legal_address_line_2',
        'district': 'counterparty_legal_district',
        'city': 'counterparty_legal_city',
        'postal_code': 'counterparty_legal_postal_code',
        'country': 'counterparty_legal_country',
        'phone': 'counterparty_legal_phone_number'
    })
    return dim_counterparty


def transform_to_star_schema(sales_order_df, staff_df, address_df, currency_df,
                             design_df, counterparty_df, department_df):
    fact_sales_order = transform_sales_order(sales_order_df)
    dim_date = create_dim_date(fact_sales_order)
    dim_staff = transform_staff(staff_df, department_df)
    dim_location = transform_location(address_df)
    dim_currency = transform_currency(currency_df)
    dim_design = transform_design(design_df)
    dim_counterparty = transform_counterparty(counterparty_df, address_df)
    return fact_sales_order, dim_date, dim_staff, dim_location, \
        dim_currency, dim_design, dim_counterparty


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
            Name=f"/processing/{table_name}/latest_packet_id",
            Type="String",
            Description=(
                "Latest packet_id of data processed "
                f"from Totesys database for {table_name} table"
            ),
            Value=str(packet_id),
            Overwrite=True,
        )
    except Exception as e:
        print(f"The packet ID could not be written: {e}")


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
        response = ssm_client.get_parameter(Name=("/processing/"+table_name+"/latest_packet_id"))
        id = response["Parameter"]["Value"]
        return int(id)

    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(f"Table name '{table_name}' does not have any recorded packets.")


# def write_table_data_to_s3(
#     dict_name dict,
#     bucket_name: str,
#     packet_id: int,
#     s3_client,
# ) -> None:
# """
# Write file to S3 bucket in Parquet format

# Args:
#     table_name (string)
#     table_data (list) : list of dictionaries all data in table,
#         one dictionary per row keys will be column headings
#     bucket_name (string)
#     packet_id (string)
#     s3_client (boto3 s3 client)

# Raises:
#     FileExistsError: S3 object already exists with the same name
#     ConnectionError : connection issue to S3 bucket

# Returns:
#     None
# """
