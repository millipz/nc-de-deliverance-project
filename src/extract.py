from src.extract_utils import (
    get_timestamp,
    write_timestamp,
    collect_table_data,
    find_latest_timestamp,
    write_table_data_to_s3,
    get_seq_id,
    write_seq_id,
)
from pg8000.native import Connection
import boto3
from datetime import datetime
from dotenv import load_dotenv
import os

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

load_dotenv(".secrets/db_credentials.env")
db_endpoint = os.getenv("TEST_DB_ENDPOINT")
db_name = os.getenv("TEST_DB_NAME")
db_username = os.getenv("TEST_DB_USERNAME")
db_password = os.getenv("TEST_DB_PASSWORD")

db_host, db_port = db_endpoint.split(":")

db = Connection(
    host=db_host,
    database=db_name,
    user=db_username,
    password=db_password,
    port=int(db_port),
)

ssm_client = boto3.client("ssm")
s3_client = boto3.client("s3")

for table in tables:
    try:
        timestamp = get_timestamp(table,ssm_client)
        print(f"On last run the latest data from {table} was dated {timestamp}")
    except KeyError:
        # assume first run, get all data
        timestamp = datetime.fromisoformat("2000-01-01")
        print(f"No previous data logged from {table}")
    data = collect_table_data(table, timestamp, db)
    print(f"Data ingested for {table}")
    latest = find_latest_timestamp(data)
    try:
        last_id = get_seq_id(table,ssm_client)
    except KeyError:
        # assume first run
        last_id = 0
        print("no previous runs logged for {table}")
    id = last_id + 1
    print(f"this is run {id}")
    try:
        write_table_data_to_s3(table, data, "nc-totesys-ingest", id, s3_client)
    except Exception as e:
        print(f"error writing bucket: {e}")
    else:
        print(f"{table} data written to s3")
        write_timestamp(latest,table,ssm_client)
        write_seq_id(id, table, ssm_client)

    # TODO - Invoke processing lambda 