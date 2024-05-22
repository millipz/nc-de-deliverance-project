import os
import pytest
import boto3
import pandas as pd
from moto import mock_aws
import json
from python.src.processing_function.lambda_utils import (
    get_packet_id,
    write_packet_id,
    retrieve_data,
    transform_sales_order
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
        conn.create_bucket(Bucket="nc-totesys-ingest",
                           CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
        yield conn


# sample dataframe fixtures for each table

@pytest.fixture(scope="function")
def sample_sales_order_dataframe(s3_client):
    with mock_aws():
        with open("python/tests/processing_function/sales_order_table.jsonl",
                  'r', encoding='utf-8') as data_file:
            json_data = json.load(data_file)
            s3_client.put_object(Bucket="nc-totesys-ingest",
                                 Body=json.dumps(json_data), Key="test-data")
            dataframe = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            yield dataframe


class TestGetPacketId:
    def test_table_name_does_not_exist(self, ssm_client):
        with pytest.raises(KeyError):
            get_packet_id("non_existent_table", ssm_client)

    def test_successful_retrieval(self, ssm_client):
        ssm_client.put_parameter(
            Name="/processing/example_table/latest_packet_id",
            Value="00000100",
            Type="String",
        )

        ssm_client.put_parameter(
            Name="/processing/example_table/latest_packet_id",
            Value="00000101",
            Type="String",
            Overwrite=True,
        )

        # Get the latest timestamp
        id = get_packet_id("example_table", ssm_client)
        assert id == 101

    # TODO: Add a test for connection issues


class TestWritePacketId:

    def test_id_writtem_to_param_store(self, ssm_client):
        id_to_write = 101
        write_packet_id(id_to_write, "test_table", ssm_client)
        id = get_packet_id("test_table", ssm_client)
        assert id == 101


class TestRetrieveData:

    def test_if_object_key_does_not_exist(self, s3_client):
        with pytest.raises(KeyError):
            retrieve_data("nc-totesys-ingest", "false-key", s3_client)

    def test_function_returns_dataframe(self, s3_client):
        with open("python/tests/processing_function/address_table.jsonl",
                  'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
            s3_client.put_object(Bucket="nc-totesys-ingest",
                                 Body=json.dumps(data), Key="test-data")

            result = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            assert isinstance(result, pd.DataFrame)

    def test_proper_data_structure(self, s3_client):
        with open("python/tests/processing_function/address_table.jsonl",
                  'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
            s3_client.put_object(Bucket="nc-totesys-ingest",
                                 Body=json.dumps(data), Key="test-data")
            result = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            assert list(result.columns) == ['address_id',
                                            'address_line_1',
                                            'address_line_2',
                                            'city',
                                            'country',
                                            'created_at',
                                            'district',
                                            'last_updated',
                                            'phone',
                                            'postal_code']


class TestTransformData:

    def test_transform_sales_order_columns(self, sample_sales_order_dataframe):
        result = transform_sales_order(sample_sales_order_dataframe)
        expected_columns = ['sales_order_id',
                            'created_date',
                            'created_time',
                            'last_updated_date',
                            'last_updated_time',
                            'sales_staff_id',
                            'counterparty_id',
                            'units_sold',
                            'unit_price',
                            'currency_id',
                            'design_id',
                            'agreed_payment_date',
                            'agreed_delivery_date',
                            'agreed_delivery_location_id']

        assert list(result.columns) == expected_columns

    def test_transform_sales_order_values(self, sample_sales_order_dataframe):
        result = transform_sales_order(sample_sales_order_dataframe)
        assert result['sales_order_id'].iloc[0] == 2
        assert result['units_sold'].iloc[0] == 42972
        assert result['unit_price'].iloc[0] == "3.94"
        assert result['currency_id'].iloc[0] == 2
        assert result['design_id'].iloc[0] == 3
        assert result['sales_staff_id'].iloc[0] == 19
        assert result['counterparty_id'].iloc[0] == 8
        assert result['agreed_payment_date'].iloc[0] == '2022-11-08'
        assert result['agreed_delivery_date'].iloc[0] == '2022-11-07'
        assert result['agreed_delivery_location_id'].iloc[0] == 8
        assert result['created_date'].iloc[0] == pd.Timestamp('2022-11-03').date()
        assert result['created_time'].iloc[0] == pd.Timestamp('14:20:52.186000').time()
        assert result['last_updated_date'].iloc[0] == pd.Timestamp('2022-11-03').date()
        assert result['last_updated_time'].iloc[0] == \
            pd.Timestamp('14:20:52.186000').time()

    def test_transform_sales_order_types(self, sample_sales_order_dataframe):
        result = transform_sales_order(sample_sales_order_dataframe)
        print(sample_sales_order_dataframe.dtypes)
        print(result.dtypes)
        assert 0
