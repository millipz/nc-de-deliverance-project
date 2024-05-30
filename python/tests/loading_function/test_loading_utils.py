import os
import pytest
import boto3
from moto import mock_aws
from datetime import datetime
import pandas as pd
from unittest.mock import MagicMock

from python.src.processing_function.lambda_utils import write_data_to_s3
from python.src.loading_function.lambda_utils import (
    retrieve_processed_data,
    write_timestamp,
    get_timestamp,
    create_dim_date,
    write_table_data_to_warehouse,
)

# Was used in TestWriteTableDataToWarehouse below
# to mock pg8000 connection
# load_dotenv(".secrets/db_credentials.env")
# db_endpoint = os.getenv("TEST_DB_ENDPOINT")
# db_name = os.getenv("TEST_DB_NAME")
# db_username = os.getenv("TEST_DB_USERNAME")
# db_password = os.getenv("TEST_DB_PASSWORD")


@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

    # TODO - edit to allow environment variables for dev/test/prod


@pytest.fixture(scope="function")
def ssm_client(aws_creds: None):
    with mock_aws():
        yield boto3.client("ssm")


@pytest.fixture(scope="function")
def s3_client(aws_creds: None):
    with mock_aws():
        conn = boto3.client("s3")
        conn.create_bucket(
            Bucket="nc-totesys-processing",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        yield conn


class TestWriteTableDataToWarehouse:

    def test_writes_successfully(self):

        mock_db = MagicMock()
        data = {"column1": [1, 2], "column2": ["a", "b"]}
        df = pd.DataFrame(data)
        mock_db.run.return_value = {"status": "success"}
        response = write_table_data_to_warehouse(df, "test_table", mock_db)
        assert response == {"status": "success"}


class TestRetrieveProcessedData:

    def test_if_object_key_does_not_exist(self, s3_client):
        with pytest.raises(KeyError) as e:
            retrieve_processed_data("nc-totesys-processing", "false-key", s3_client)

        assert str(e.value) == "\"The key 'false-key' does not exist.\""

    def test_function_returns_dataframe(self, s3_client):

        d = {"col1": [1, 2], "col2": [3, 4]}
        df = pd.DataFrame(data=d)

        key = write_data_to_s3(
            df, "test-table", "nc-totesys-processing", 000000, s3_client
        )

        result = retrieve_processed_data("nc-totesys-processing", key, s3_client)

        assert isinstance(result, pd.DataFrame)

    def test_successful_retrieval(self, s3_client):

        d = {"col1": [1, 2], "col2": [3, 4]}
        df = pd.DataFrame(data=d)

        key = write_data_to_s3(
            df, "test-table", "nc-totesys-processing", 000000, s3_client
        )

        result = retrieve_processed_data("nc-totesys-processing", key, s3_client)

        assert df.equals(result)


# Unable to implement, feel free to attempt
# class TestWriteTableDataToWarehouse:

#     @patch("pg8000.native.Connection", autospec=True)
#     def test_writes_successfully(self, mock_pg_connection):

#         data = {
#             'column1': [1, 2],
#             'column2': ['a', 'b']
#         }
#         df = pd.DataFrame(data)

#         response = write_table_data_to_warehouse(df, "test-table", mock_pg_connection)

#         assert response == 1


class TestGetTimestamp:

    def test_table_name_does_not_exist(self, ssm_client):
        with pytest.raises(KeyError):
            get_timestamp("non_existent_table", ssm_client)

    def test_successful_retrieval(self, ssm_client):
        ssm_client.put_parameter(
            Name="example_table_latest_extracted_timestamp",
            Value="2024-05-16T10:40:30.962473",
            Type="String",
        )

        ssm_client.put_parameter(
            Name="example_table_latest_extracted_timestamp",
            Value="2024-05-16T10:50:30.123000",
            Type="String",
            Overwrite=True,
        )

        # Get the latest timestamp
        timestamp = get_timestamp("example_table", ssm_client)
        assert timestamp == datetime.fromisoformat("2024-05-16T10:50:30.123000")


class TestWriteTimestamp:

    def test_timestamp_writtem_to_param_store(self, ssm_client):
        time_to_write = datetime.fromisoformat("2024-05-16T10:50:30.123000")
        write_timestamp(time_to_write, "test_table", ssm_client)
        timestamp = get_timestamp("test_table", ssm_client)
        assert timestamp.isoformat() == "2024-05-16T10:50:30.123000"


class TestCreateDimDate:

    def test_create_dim_date(self):
        start_date = "2023-01-01"
        end_date = "2023-01-10"
        result = create_dim_date(start_date, end_date)

        expected_num_rows = 10
        assert len(result) == expected_num_rows

        expected_columns = [
            "date_id",
            "year",
            "month",
            "day",
            "day_of_week",
            "day_name",
            "month_name",
            "quarter",
        ]
        assert (list(result.columns)) == expected_columns

        first_date = result.iloc[0]
        assert first_date["date_id"] == pd.Timestamp("2023-01-01")
        assert first_date["year"] == 2023
        assert first_date["month"] == 1
        assert first_date["day"] == 1
        assert first_date["day_of_week"] == 6
        assert first_date["day_name"] == "Sunday"
        assert first_date["month_name"] == "January"
        assert first_date["quarter"] == 1
