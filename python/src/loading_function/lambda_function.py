import boto3
import os
import logging
from datetime import datetime
from pg8000.native import Connection
from lambda_utils import (
    retrieve_processed_data,
    write_table_data_to_warehouse,
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
    SecretId=f"totesys_warehouse_username"
)["SecretString"]
WAREHOUSE_PASSWORD = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_warehouse_password"
)["SecretString"]
WAREHOUSE_HOST, WAREHOUSE_PORT = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_warehouse_endpoint"
)["SecretString"].split(":")
WAREHOUSE_NAME = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_warehouse_name"
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

    response_data = {}
    total_loaded_rows = 0

    payload = event["data"]
    for table_name, object_key in payload.items():
        data_frame = retrieve_processed_data(S3_PROCESSED_BUCKET, object_key, s3_client)
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
    return {"statusCode": 200, "data": response_data}
