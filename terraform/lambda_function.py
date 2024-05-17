import os
import boto3
import json
from datetime import datetime

s3_client = boto3.client("s3")
logs_client = boto3.client("logs")
S3_BUCKET = os.getenv("S3_BUCKET")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def lambda_handler(event, context):
    timestamp = datetime.now().isoformat()
    s3_client.put_object(
        Bucket=S3_BUCKET, Key=f"log/{timestamp}.txt", Body=bytes(timestamp, "utf-8")
    )
    return {"statusCode": 200, "body": json.dumps("Timestamp file created.")}
