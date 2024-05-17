import boto3
import os
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
logs_client = boto3.client("logs")
rds_client = boto3.client("rds")

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


def lambda_handler(event, context):
    for table in tables:
        try:
            timestamp = get_timestamp(table, ssm_client)
            print(f"On last run the latest data from {table} was dated {timestamp}")
        except KeyError:
            # assume first run, get all data
            timestamp = datetime.fromisoformat("2000-01-01")
            print(f"No previous data logged from {table}")
        data = collect_table_data(table, timestamp, db)
        print(f"Data ingested for {table}")
        latest = find_latest_timestamp(data)
        try:
            last_id = get_seq_id(table, ssm_client)
        except KeyError:
            # assume first run
            last_id = 0
            print("no previous runs logged for {table}")
        id = last_id + 1
        print(f"this is run {id}")
        try:
            write_table_data_to_s3(table, data, "nc-totesys-ingest", id, s3_client)
        except Exception as e:
            return {"statusCode": 500, "body": f"Error 500 Server Error: {e}"}
        else:
            write_timestamp(latest, table, ssm_client)
            write_seq_id(id, table, ssm_client)
            print(f"{table} data written to S3")

        # TODO - Invoke processing lambda

    return {"statusCode": 200, "body": "Completed."}
