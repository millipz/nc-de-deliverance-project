import boto3
import os
import logging
from datetime import datetime
from pg8000.native import Connection
from lambda_utils import (
    get_timestamp,
    write_timestamp,
    collect_table_data,
    find_latest_timestamp,
    write_table_data_to_s3,
    get_seq_id,
    write_seq_id,
)

s3_client = boto3.client("s3")
secrets_manager_client = boto3.client("secretsmanager")
ssm_client = boto3.client("ssm")
rds_client = boto3.client("rds")
logs_client = boto3.client("logs")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.getenv("S3_BUCKET")
ENVIRONMENT = os.getenv("ENVIRONMENT")

DB_USERNAME = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_username")["SecretString"]
DB_PASSWORD = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_password")["SecretString"]
DB_HOST, DB_PORT = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_endpoint")["SecretString".split(":")]
DB_NAME = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_name")["SecretString"]

tables = [
    "address",
    "counterparty",
    "currency",
    "department",
    "design",
    "payment_type",
    "payment",
    "purchase_order",
    "sales_order",
    "staff",
    "transaction",
]

db = Connection(
    user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME, port=DB_PORT, host=DB_HOST
)


def lambda_handler(event, context):
    logger.info("## ENVIRONMENT VARIABLES")
    logger.info(os.environ["AWS_LAMBDA_LOG_GROUP_NAME"])
    logger.info(os.environ["AWS_LAMBDA_LOG_STREAM_NAME"])
    logger.info("## EVENT")
    logger.info(event)

    response_data = {}
    total_ingested_rows = 0

    for table in tables:
        try:
            timestamp = get_timestamp(ENVIRONMENT + "_" + table, ssm_client)
            logger.info(
                f"On last run the latest data from {table} was dated {timestamp}"
            )
        except KeyError:
            # assume first run, get all data
            timestamp = datetime.fromisoformat("2000-01-01")
            logger.error(f"No previous data logged from {table}")
        data = collect_table_data(table, timestamp, db)
        total_ingested_rows += len(data)
        if len(data) == 0:
            logger.info(f"No new data for {table}")
        else:
            logger.info(f"Data ingested for {table}")
            latest = find_latest_timestamp(data)
            try:
                last_id = get_seq_id(ENVIRONMENT + "_" + table, ssm_client)
            except KeyError:
                # assume first run
                last_id = 0
                logger.error("No previous runs logged for {table}")
            id = last_id + 1
            logger.info(f"this is run {id}")
            try:
                key = write_table_data_to_s3(table, data, S3_BUCKET, id, s3_client)
            except Exception as e:
                logger.error(f"Error writing {table} data to S3: {e}")
                return {"statusCode": 500, "body": f"Error: {e}"}
            else:
                write_timestamp(latest, ENVIRONMENT + "_" + table, ssm_client)
                write_seq_id(id, ENVIRONMENT + "_" + table, ssm_client)
                logger.info(f"{table} data written to S3, {len(data)} rows ingested")
                response_data[table] = key
    logger.info(f"{total_ingested_rows} rows ingested this run")
    return {"statusCode": 200, "data": response_data}
