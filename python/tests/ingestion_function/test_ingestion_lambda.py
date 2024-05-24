import os
import boto3
import pytest
from moto import mock_aws
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

from python.src.ingestion_function.lambda_function import lambda_handler, tables

load_dotenv(".secrets/db_credentials.env")
db_endpoint = os.getenv("TEST_DB_ENDPOINT")
db_name = os.getenv("TEST_DB_NAME")
db_username = os.getenv("TEST_DB_USERNAME")
db_password = os.getenv("TEST_DB_PASSWORD")


# Fixtures for AWS clients
@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    """Create an S3 client using moto for mocking."""
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture(scope="function")
def secrets_manager_client(aws_credentials):
    with mock_aws():
        client = boto3.client("secretsmanager", region_name="eu-west-2")
        client.create_secret(Name="totesys_dev_db_username", SecretString=db_username)
        client.create_secret(Name="totesys_dev_db_password", SecretString=db_password)
        client.create_secret(Name="totesys_dev_db_endpoint", SecretString=db_endpoint)
        client.create_secret(Name="totesys_dev_db_name", SecretString=db_name)
        yield client


@pytest.fixture(scope="function")
def ssm_client(aws_credentials):
    """Create an SSM client using moto for mocking."""
    with mock_aws():
        yield boto3.client("ssm", region_name="eu-west-2")


# Fixtures for environment and event/context
@pytest.fixture(scope="function")
def lambda_event():
    return {"key1": "value1", "key2": "value2", "key3": "value3"}


@pytest.fixture(scope="function")
def lambda_context():
    class LambdaContext:

        def __init__(self):
            """Initialize the Lambda context."""
            self.function_name = "lambda_function"
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = (
                "arn:aws:lambda:eu-west-2:123456789012:function:lambda_function"
            )
            self.aws_request_id = "unique-id"

    return LambdaContext()


@patch("python.src.ingestion_function.lambda_function.get_timestamp")
@patch("python.src.ingestion_function.lambda_function.write_timestamp")
@patch("python.src.ingestion_function.lambda_function.collect_table_data")
@patch("python.src.ingestion_function.lambda_function.find_latest_timestamp")
@patch("python.src.ingestion_function.lambda_function.write_table_data_to_s3")
@patch("python.src.ingestion_function.lambda_function.get_seq_id")
@patch("python.src.ingestion_function.lambda_function.write_seq_id")
@patch("pg8000.native.Connection", autospec=True)
def test_lambda_handler(
    mock_pg_connection,
    mock_write_seq_id,
    mock_get_seq_id,
    mock_write_table_data_to_s3,
    mock_find_latest_timestamp,
    mock_collect_table_data,
    mock_write_timestamp,
    mock_get_timestamp,
    s3_client,
    secrets_manager_client,
    ssm_client,
    lambda_event,
    lambda_context,
):
    """
    Test the lambda_handler function.

    This test verifies that the lambda_handler function correctly processes
    data from various tables, writes the data to S3, and updates the
    necessary timestamps and sequence IDs in SSM.

    Args:
        mock_pg_connection: A mocked PostgreSQL connection.
        mock_write_seq_id: A mocked function for writing sequence IDs.
        mock_get_seq_id: A mocked function for getting sequence IDs.
        mock_write_table_data_to_s3: A mocked function for writing table data to S3.
        mock_find_latest_timestamp: A mocked function for finding the latest timestamp.
        mock_collect_table_data: A mocked function for collecting table data.
        mock_write_timestamp: A mocked function for writing timestamps.
        mock_get_timestamp: A mocked function for getting timestamps.
        s3_client: A mocked S3 client.
        secrets_manager_client: A mocked Secrets Manager client.
        ssm_client: A mocked SSM client.
        lambda_event: The sample Lambda event.
        lambda_context: The mocked Lambda context.
    """

    os.environ["S3_BUCKET"] = "my-bucket"
    os.environ["AWS_LAMBDA_LOG_GROUP_NAME"] = "log-group"
    os.environ["AWS_LAMBDA_LOG_STREAM_NAME"] = "log-stream"

    mock_pg_connection.return_value = MagicMock()

    mock_get_timestamp.return_value = "2000-01-01T00:00:00"
    mock_collect_table_data.return_value = [
        {"id": 1, "timestamp": "2023-01-01T00:00:00"}
    ]
    mock_find_latest_timestamp.return_value = "2023-01-01T00:00:00"
    mock_write_table_data_to_s3.return_value = "s3://my-bucket/path/to/data"
    mock_get_seq_id.return_value = 1

    response = lambda_handler(lambda_event, lambda_context)

    assert response["statusCode"] == 200
    assert "data" in response
    for table in tables:
        assert table in response["data"]

    mock_get_timestamp.assert_called()
    mock_collect_table_data.assert_called()
    mock_find_latest_timestamp.assert_called()
    mock_write_table_data_to_s3.assert_called()
    mock_write_timestamp.assert_called()
    mock_write_seq_id.assert_called()
