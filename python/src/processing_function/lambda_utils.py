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


# def transform_to_star_schema(sales_order_df, staff_df, address_df, currency_df, design_df, counterparty_df):


def transform_sales_order(sales_order_df):
    fact_sales_order = sales_order_df.copy()

    fact_sales_order['created_date'] = pd.to_datetime(fact_sales_order['created_at']).dt.date
    fact_sales_order['created_time'] = pd.to_datetime(fact_sales_order['created_at']).dt.time
    fact_sales_order['last_updated_date'] = \
        pd.to_datetime(fact_sales_order['last_updated']).dt.date
    fact_sales_order['last_updated_time'] = \
        pd.to_datetime(fact_sales_order['last_updated']).dt.time

    fact_sales_order.rename(columns={
        'sales_order_id': 'sales_order_id',
        'staff_id': 'sales_staff_id',
        'units_sold': 'units_sold',
        'unit_price': 'unit_price',
        'currency_id': 'currency_id',
        'design_id': 'design_id',
        'agreed_payment_date': 'agreed_payment_date',
        'agreed_delivery_date': 'agreed_delivery_date',
        'agreed_delivery_location_id': 'agreed_delivery_location_id'
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
