import boto3
import os
import logging
from pg8000.native import Connection
from lambda_utils import (
    retrieve_data,
    transform_sales_order,
    transform_staff,
    transform_location,
    transform_currency,
    transform_design,
    transform_counterparty,
    transform_payment,
    transform_payment_type,
    transform_purchase_order,
    transform_transaction,
    write_data_to_s3,
)

s3_client = boto3.client("s3")
secrets_manager_client = boto3.client("secretsmanager")
ssm_client = boto3.client("ssm")
rds_client = boto3.client("rds")
logs_client = boto3.client("logs")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_INGESTION_BUCKET = os.getenv("S3_INGESTION_BUCKET")
S3_PROCESSED_BUCKET = os.getenv("S3_PROCESSED_BUCKET")
ENVIRONMENT = os.getenv("ENVIRONMENT")

DB_USERNAME = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_username"
)["SecretString"]
DB_PASSWORD = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_password"
)["SecretString"]
DB_HOST, DB_PORT = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_endpoint"
)["SecretString"].split(":")
DB_NAME = secrets_manager_client.get_secret_value(
    SecretId=f"totesys_{ENVIRONMENT}_db_name"
)["SecretString"]

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
    processed_data_frames = {}

    payload = event["data"]

    address_key = payload["address"]
    address_data = retrieve_data(S3_INGESTION_BUCKET, address_key, s3_client)
    processed_data_frames["dim_location"] = transform_location(address_data)
    logger.info(
        f"{len(processed_data_frames['dim_location'].index)} rows processed into dim_location."
    )

    department_key = payload["department"]
    department_data = retrieve_data(S3_INGESTION_BUCKET, department_key, s3_client)

    for table_name, object_key in payload.items():
        data_frame = retrieve_data(S3_INGESTION_BUCKET, object_key, s3_client)
        match table_name:
            case "address":
                continue
            case "counterparty":
                new_table_name = "dim_counterparty"
                processed_data_frames[new_table_name] = transform_counterparty(
                    data_frame,
                    processed_data_frames["dim_location"],
                )
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                    rows processed into {new_table_name}"
                )
            case "currency":
                new_table_name = "dim_currency"
                processed_data_frames[new_table_name] = transform_currency(data_frame)
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                    rows processed into {new_table_name}"
                )
            case "design":
                new_table_name = "dim_design"
                processed_data_frames[new_table_name] = transform_design(data_frame)
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                    rows processed into {new_table_name}"
                )
            case "payment":
                new_table_name = "fact_payment"
                processed_data_frames[new_table_name] = transform_payment(data_frame)
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                    rows processed into {new_table_name}"
                )
            case "payment_type":
                new_table_name = "dim_payment_type"
                processed_data_frames[new_table_name] = transform_payment_type(
                    data_frame
                )
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                    rows processed into {new_table_name}"
                )
            case "purchase_order":
                new_table_name = "fact_purchase_order"
                processed_data_frames[new_table_name] = transform_purchase_order(
                    data_frame
                )
            case "sales_order":
                new_table_name = "fact_sales_order"
                processed_data_frames[new_table_name] = transform_sales_order(
                    data_frame
                )
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                      rows processed into {new_table_name}"
                )
            case "staff":
                new_table_name = "dim_staff"
                processed_data_frames[new_table_name] = transform_staff(
                    data_frame, department_data
                )
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                    rows processed into {new_table_name}"
                )
            case "transaction":
                new_table_name = "dim_transaction"
                processed_data_frames[new_table_name] = transform_transaction(
                    data_frame
                )
                logger.info(
                    f"{len(processed_data_frames[new_table_name].index)} \
                    rows processed into {new_table_name}"
                )
            case _:
                logger.error(f"Unknown table name: {table_name}")
                continue
        packet_id = int(object_key.split("_")[-2])
        processed_key = write_data_to_s3(
            processed_data_frames[new_table_name],
            new_table_name,
            S3_PROCESSED_BUCKET,
            packet_id,
            s3_client,
        )
        response_data[new_table_name] = processed_key

    return {"statusCode": 200, "data": response_data}
