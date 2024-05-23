import os
import pytest
import boto3
from pg8000.native import Connection
from moto import mock_aws
from datetime import datetime, date
from freezegun import freeze_time
import json
from mock import Mock
from dotenv import load_dotenv
from python.src.ingestion_function.lambda_utils import (
    get_timestamp,
    write_timestamp,
    collect_table_data,
    find_latest_timestamp,
    write_table_data_to_s3,
    get_seq_id,
    write_seq_id,
)


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
        yield boto3.client("s3")


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

    # TODO: Add a test for connection issues
    # def test_connection_issue(self):
    #     # Set up an SSM client without credentials
    #     ssm_client = boto3.client("ssm")
    #     with self.assertRaises(NoCredentialsError):
    #         ssm_client.get_parameter(Name='example_table')


class TestWriteTimestamp:

    def test_timestamp_writtem_to_param_store(self, ssm_client):
        time_to_write = datetime.fromisoformat("2024-05-16T10:50:30.123000")
        write_timestamp(time_to_write, "test_table", ssm_client)
        timestamp = get_timestamp("test_table", ssm_client)
        assert timestamp.isoformat() == "2024-05-16T10:50:30.123000"


class TestFindLatestTimestamp:
    def test_returns_timestamp(self):
        dummy_data = [
            {"last_updated": datetime.fromisoformat("2024-05-16T10:50:30.123000")},
            {"last_updated": datetime.fromisoformat("2024-05-16T12:50:30.123000")},
        ]
        assert isinstance(find_latest_timestamp(dummy_data), datetime)

    def test_returns_latest_date(self):
        dummy_data = [
            {"last_updated": datetime.fromisoformat("2024-05-16T10:50:30.123000")},
            {"last_updated": datetime.fromisoformat("2024-05-16T12:50:30.123000")},
        ]
        assert (
            find_latest_timestamp(dummy_data).isoformat()
            == "2024-05-16T12:50:30.123000"
        )

    def test_allows_passing_custom_columns(self):
        dummy_data = [
            {
                "last_updated": datetime.fromisoformat("2024-05-16T10:50:30.123000"),
                "other_column": datetime.fromisoformat("2024-05-20T10:10:10.123000"),
            },
            {
                "last_updated": datetime.fromisoformat("2024-05-16T12:50:30.123000"),
                "other_column": datetime.fromisoformat("2024-01-20T10:10:10.123000"),
            },
        ]
        assert (
            find_latest_timestamp(
                dummy_data, columns=["last_updated", "other_column"]
            ).isoformat()
            == "2024-05-20T10:10:10.123000"
        )


class TestWriteTableDataToS3:
    staff_sample_data = [
        {
            "created_at": "2022-11-03 14:20:51.563000",
            "department_id": 2,
            "email_address": "jeremie.franey@terrifictotes.com",
            "first_name": "Jeremie",
            "last_name": "Franey",
            "last_updated": "2022-11-03 14:20:51.563000",
            "staff_id": 1,
        },
        {
            "created_at": "2022-11-03 14:20:51.563000",
            "department_id": 6,
            "email_address": "deron.beier@terrifictotes.com",
            "first_name": "Deron",
            "last_name": "Beier",
            "last_updated": "2022-11-03 14:20:51.563000",
            "staff_id": 2,
        },
        {
            "created_at": "2022-11-03 14:20:51.563000",
            "department_id": 6,
            "email_address": "jeanette.erdman@terrifictotes.com",
            "first_name": "Jeanette",
            "last_name": "Erdman",
            "last_updated": "2022-11-03 14:20:51.563000",
            "staff_id": 3,
        },
    ]

    @freeze_time("2024-01-01")
    def test_key_is_as_expected(self):
        table_name = "staff"
        sequential_id = 101
        time_format = "%H%M%S%f"
        expected_key = (
            f"{date.today()}/{table_name}_"
            f"{str(sequential_id).zfill(8)}_"
            f"{datetime.now().strftime(time_format)}.jsonl"
        )
        assert expected_key == "2024-01-01/staff_00000101_000000000000.jsonl"

    @freeze_time("2024-01-01")
    def test_table_data_written_in_json_lines(self, s3_client):
        bucket_name = "ingestion_bucket"
        table_name = "staff"
        sequential_id = 101
        time_format = "%H%M%S%f"
        expected_key = (
            f"{date.today()}/{table_name}_"
            f"{str(sequential_id).zfill(8)}_"
            f"{datetime.now().strftime(time_format)}.jsonl"
        )

        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        write_table_data_to_s3(
            table_name,
            self.staff_sample_data,
            bucket_name,
            sequential_id,
            s3_client,
        )
        result = json.loads(
            s3_client.get_object(Bucket=bucket_name, Key=expected_key)["Body"]
            .read()
            .decode("utf-8")
        )
        assert result == self.staff_sample_data


class TestGetSeqId:
    def test_table_name_does_not_exist(self, ssm_client):
        with pytest.raises(KeyError):
            get_seq_id("non_existent_table", ssm_client)

    def test_successful_retrieval(self, ssm_client):
        ssm_client.put_parameter(
            Name="example_table_latest_packet_id",
            Value="00000100",
            Type="String",
        )

        ssm_client.put_parameter(
            Name="example_table_latest_packet_id",
            Value="00000101",
            Type="String",
            Overwrite=True,
        )

        # Get the latest timestamp
        id = get_seq_id("example_table", ssm_client)
        assert id == 101

    # TODO: Add a test for connection issues


class TestWriteSeqId:

    def test_id_writtem_to_param_store(self, ssm_client):
        id_to_write = 101
        write_seq_id(id_to_write, "test_table", ssm_client)
        id = get_seq_id("test_table", ssm_client)
        assert id == 101


class TestCollectTableData:

    def test_list_of_dicts_returned(self):
        with open("python/tests/ingestion_function/test_staff_response.txt") as f:
            data = f.read()
        mock_conn = Mock()
        mock_conn.run.return_value = data
        mock_conn.columns = [
            {"name": "created_at"},
            {"name": "department_id"},
            {"name": "email_address"},
            {"name": "first_name"},
            {"name": "last_name"},
            {"name": "last_updated"},
            {"name": "staff_id"},
        ]

        result = collect_table_data("staff", datetime.now(), mock_conn)
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

    # Not sure how to mock PSQL filter - testing with real test_db credentials
    @pytest.mark.skipif(
        (os.getenv("ENVIRONMENT") != "DEV"), reason="Skipping for CI/CD"
    )
    def test_results_filtered_by_date(self):
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

        query_date = datetime.fromisoformat("2023-01-01")
        result = collect_table_data("design", query_date, db)
        assert all([design["last_updated"] > query_date for design in result])
