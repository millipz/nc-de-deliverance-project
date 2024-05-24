import os
import pytest
import boto3
import pandas as pd
from moto import mock_aws
import json
from python.src.processing_function.lambda_utils import (
    retrieve_data,
    transform_sales_order,
    transform_staff,
    transform_location,
    transform_currency,
    transform_design,
    transform_counterparty,
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
        conn = boto3.client("s3")
        conn.create_bucket(
            Bucket="nc-totesys-ingest",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        yield conn


@pytest.fixture(scope="function")
def sample_address_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/address_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe

@pytest.fixture(scope="function")
def sample_dim_location_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/dim_location_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe

@pytest.fixture(scope="function")
def sample_sales_order_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/sales_order_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe


@pytest.fixture(scope="function")
def sample_staff_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/staff_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe


@pytest.fixture(scope="function")
def sample_department_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/department_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe


@pytest.fixture(scope="function")
def sample_currency_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/currency_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe


@pytest.fixture(scope="function")
def sample_design_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/design_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe


@pytest.fixture(scope="function")
def sample_counterparty_dataframe(s3_client):
    with mock_aws():
        with open(
            "python/tests/processing_function/sample_jsonl_data/counterparty_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(json_data), Key="test-data"
            )
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe


class TestRetrieveData:

    def test_if_object_key_does_not_exist(self, s3_client):
        with pytest.raises(KeyError):
            retrieve_data("nc-totesys-ingest", "false-key", s3_client)

    def test_function_returns_dataframe(self, s3_client):
        with open(
            "python/tests/processing_function/sample_jsonl_data/address_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(data), Key="test-data"
            )

            result = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            assert isinstance(result, pd.DataFrame)

    def test_proper_data_structure(self, s3_client):
        with open(
            "python/tests/processing_function/sample_jsonl_data/address_table.jsonl",
            "r",
            encoding="utf-8",
        ) as data_file:
            data = json.load(data_file)
            s3_client.put_object(
                Bucket="nc-totesys-ingest", Body=json.dumps(data), Key="test-data"
            )
            result = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            assert list(result.columns) == [
                "address_id",
                "address_line_1",
                "address_line_2",
                "city",
                "country",
                "created_at",
                "district",
                "last_updated",
                "phone",
                "postal_code",
            ]


class TestTransformData:

    def test_transform_sales_order(self, sample_sales_order_dataframe):
        result = transform_sales_order(sample_sales_order_dataframe)
        expected_columns = [
            "sales_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "sales_staff_id",
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "design_id",
            "agreed_payment_date",
            "agreed_delivery_date",
            "agreed_delivery_location_id",
        ]

        assert list(result.columns) == expected_columns

        assert result["sales_order_id"].iloc[0] == 2
        assert result["units_sold"].iloc[0] == 42972
        assert result["unit_price"].iloc[0] == "3.94"
        assert result["currency_id"].iloc[0] == 2
        assert result["design_id"].iloc[0] == 3
        assert result["sales_staff_id"].iloc[0] == 19
        assert result["counterparty_id"].iloc[0] == 8
        assert result["agreed_payment_date"].iloc[0] == "2022-11-08"
        assert result["agreed_delivery_date"].iloc[0] == "2022-11-07"
        assert result["agreed_delivery_location_id"].iloc[0] == 8
        assert result["created_date"].iloc[0] == "2022-11-03"
        assert result["created_time"].iloc[0] == "14:20:52.186000"
        assert result["last_updated_date"].iloc[0] == "2022-11-03"
        assert result["last_updated_time"].iloc[0] == "14:20:52.186000"

    # def test_create_dim_date(self):
    #     start_date = "2023-01-01"
    #     end_date = "2023-01-10"
    #     result = create_dim_date(start_date, end_date)

    #     expected_num_rows = 10
    #     assert len(result) == expected_num_rows

    #     expected_columns = [
    #         "date_id",
    #         "year",
    #         "month",
    #         "day",
    #         "day_of_week",
    #         "day_name",
    #         "month_name",
    #         "quarter",
    #     ]
    #     assert (list(result.columns)) == expected_columns

    #     first_date = result.iloc[0]
    #     assert first_date["date_id"] == pd.Timestamp("2023-01-01")
    #     assert first_date["year"] == 2023
    #     assert first_date["month"] == 1
    #     assert first_date["day"] == 1
    #     assert first_date["day_of_week"] == 6
    #     assert first_date["day_name"] == "Sunday"
    #     assert first_date["month_name"] == "January"
    #     assert first_date["quarter"] == 1

    def test_transform_staff(self, sample_staff_dataframe, sample_department_dataframe):
        result = transform_staff(sample_staff_dataframe, sample_department_dataframe)
        expected_columns = [
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address",
        ]
        assert list(result.columns) == expected_columns

        assert result["staff_id"].iloc[0] == 1
        assert result["first_name"].iloc[0] == "Jeremie"
        assert result["last_name"].iloc[0] == "Franey"
        assert result["department_name"].iloc[0] == "Purchasing"
        assert result["location"].iloc[0] == "Manchester"
        assert result["email_address"].iloc[0] == "jeremie.franey@terrifictotes.com"

    def test_transform_location(self, sample_address_dataframe):
        result = transform_location(sample_address_dataframe)
        expected_columns = [
            "location_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
        ]
        assert list(result.columns) == expected_columns

        assert result["location_id"].iloc[0] == 1
        assert result["address_line_1"].iloc[0] == "6826 Herzog Via"
        assert result["address_line_2"].iloc[0] is None
        assert result["district"].iloc[0] == "Avon"
        assert result["city"].iloc[0] == "New Patienceburgh"
        assert result["postal_code"].iloc[0] == "28441"
        assert result["country"].iloc[0] == "Turkey"
        assert result["phone"].iloc[0] == "1803 637401"

    def test_transform_currency(self, sample_currency_dataframe):
        result = transform_currency(sample_currency_dataframe)
        expected_columns = ["currency_id", "currency_code", "currency_name"]
        assert list(result.columns) == expected_columns

        assert result["currency_id"].iloc[0] == 1
        assert result["currency_code"].iloc[0] == "GBP"
        assert result["currency_name"].iloc[0] == "British Pound"

    def test_transform_design(self, sample_design_dataframe):
        result = transform_design(sample_design_dataframe)
        expected_columns = ["design_id", "design_name", "file_location", "file_name"]
        assert list(result.columns) == expected_columns

        assert result["design_id"].iloc[0] == 8
        assert result["design_name"].iloc[0] == "Wooden"
        assert result["file_location"].iloc[0] == "/usr"
        assert result["file_name"].iloc[0] == "wooden-20220717-npgz.json"

    def test_transform_counterparty(
        self, sample_counterparty_dataframe, sample_dim_location_dataframe
    ):
        result = transform_counterparty(
            sample_counterparty_dataframe, sample_address_dataframe
        )
        expected_columns = [
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_legal_phone_number",
        ]
        assert list(result.columns) == expected_columns

        assert result["counterparty_id"].iloc[0] == 1
        assert result["counterparty_legal_name"].iloc[0] == "Fahey and Sons"
        assert (
            result["counterparty_legal_address_line_1"].iloc[0]
            == "605 Haskell Trafficway"
        )
        assert result["counterparty_legal_address_line_2"].iloc[0] == "Axel Freeway"
        assert result["counterparty_legal_district"].iloc[0] is None
        assert result["counterparty_legal_city"].iloc[0] == "East Bobbie"
        assert result["counterparty_legal_postal_code"].iloc[0] == "88253-4257"
        assert (
            result["counterparty_legal_country"].iloc[0]
            == "Heard Island and McDonald Islands"
        )
        assert result["counterparty_legal_phone_number"].iloc[0] == "9687 937447"
