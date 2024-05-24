import boto3
import os
import logging
from pg8000.native import Connection
from datetime import datetime, timedelta
from lambda_utils import (
    retrieve_processed_data,
    write_table_data_to_warehouse,
    create_dim_date,
    get_timestamp,
    write_timestamp,
)

s3_client = boto3.client("s3")
secrets_manager_client = boto3.client("secretsmanager")
ssm_client = boto3.client("ssm")
rds_client = boto3.client("rds")
logs_client = boto3.client("logs")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_PROCESSED_BUCKET = os.getenv("S3_PROCESSED_BUCKET")
ENVIRONMENT = os.getenv("ENVIRONMENT")

WAREHOUSE_USERNAME = secrets_manager_client.get_secret_value(
    SecretId="totesys_warehouse_username"
)["SecretString"]
WAREHOUSE_PASSWORD = secrets_manager_client.get_secret_value(
    SecretId="totesys_warehouse_password"
)["SecretString"]
WAREHOUSE_HOST, WAREHOUSE_PORT = secrets_manager_client.get_secret_value(
    SecretId="totesys_warehouse_endpoint"
)["SecretString"].split(":")
WAREHOUSE_NAME = secrets_manager_client.get_secret_value(
    SecretId="totesys_warehouse_name"
)["SecretString"]

db = Connection(
    user=WAREHOUSE_USERNAME,
    password=WAREHOUSE_PASSWORD,
    database=WAREHOUSE_NAME,
    port=WAREHOUSE_PORT,
    host=WAREHOUSE_HOST,
)


def lambda_handler(event, context):
    logger.info("## ENVIRONMENT VARIABLES")
    logger.info(os.environ["AWS_LAMBDA_LOG_GROUP_NAME"])
    logger.info(os.environ["AWS_LAMBDA_LOG_STREAM_NAME"])
    logger.info("## EVENT")
    logger.info(event)

    future_date = datetime.today() + timedelta(years=50)

    try:
        last_date = get_timestamp(f"{ENVIRONMENT}_loaded_date", ssm_client)
    except KeyError:
        # if no last date exists, assume first run
        last_date = datetime.fromisoformat("2020-01-01")

    if last_date != future_date:
        date_dataframe = create_dim_date(last_date, future_date)
        write_timestamp(future_date, f"{ENVIRONMENT}_dim_date", ssm_client)
        try:
            response = write_table_data_to_warehouse(date_dataframe, "dim_date", db)
        except Exception as e:
            logger.error(f"Error loading dim_date data to warehouse: {e}")
            return {"statusCode": 500, "body": f"Error: {e}"}

    response = ""
    response_data = {}
    total_loaded_rows = 0
    table_order = [
        "dim_currency",
        "dim_design",
        "dim_location",
        "dim_date",
        "dim_staff",
        "dim_counterparty",
        "fact_sales_order",
    ]

    payload = event["data"]
    # for table_name, object_key in payload.items():
    for table_name in table_order:
        if table_name in payload.keys():
            data_frame = retrieve_processed_data(
                S3_PROCESSED_BUCKET, payload[table_name], s3_client
            )
            loaded_rows = len(data_frame.index)
            total_loaded_rows += loaded_rows
            try:
                response = write_table_data_to_warehouse(data_frame, table_name, db)
            except Exception as e:
                logger.error(f"Error loading {table_name} data to warehouse: {e}")
                return {"statusCode": 500, "body": f"Error: {e}"}
            else:
                logger.info(
                    f"{table_name} data loaded to warehouse, {loaded_rows} rows ingested"
                )
                response_data[table_name] = loaded_rows
    logger.info(f"{total_loaded_rows} rows ingested this run")
    return {"statusCode": 200, "data": response_data, "message": response}
