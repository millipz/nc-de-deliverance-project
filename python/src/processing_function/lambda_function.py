import boto3
import os
import logging
from datetime import datetime
from pg8000.native import Connection
from lambda_utils import (
    retrieve_data,
    transform_to_star_schema,
    get_packet_id,
    write_packet_id,
)

s3_client = boto3.client("s3")
secrets_manager_client = boto3.client("secretsmanager")
ssm_client = boto3.client("ssm")
rds_client = boto3.client("rds")
logs_client = boto3.client("logs")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.getenv("S3_BUCKET")

DB_USERNAME = secrets_manager_client.get_secret_value(SecretId="totesys-username")[
    "SecretString"
]
DB_PASSWORD = secrets_manager_client.get_secret_value(SecretId="totesys-password")[
    "SecretString"
]
DB_HOST = secrets_manager_client.get_secret_value(SecretId="totesys-hostname")[
    "SecretString"
]
DB_PORT = secrets_manager_client.get_secret_value(SecretId="totesys-port")[
    "SecretString"
]
DB_NAME = secrets_manager_client.get_secret_value(SecretId="totesys-database")[
    "SecretString"
]

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


# def lambda_handler(event, context):
#     logger.info('## ENVIRONMENT VARIABLES')
#     logger.info(os.environ['AWS_LAMBDA_LOG_GROUP_NAME'])
#     logger.info(os.environ['AWS_LAMBDA_LOG_STREAM_NAME'])
#     logger.info('## EVENT')
#     logger.info(event)
    
#     for table in tables: