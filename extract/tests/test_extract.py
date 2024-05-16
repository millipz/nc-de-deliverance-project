import boto3
import os
import pytest
from moto import mock_aws
from extract.src.extract import (get_timestamp,
                                 write_timestamp,
                                 collect_table_data,
                                 find_latest_timestamp,
                                 write_table_data_to_s3,
                                 get_seq_id, write_seq_id,)
from datetime import datetime



@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def ssm_client(aws_creds):
    with mock_aws():
        yield boto3.client("ssm")


class TestGetTimestamp:

    def test_table_name_does_not_exist(self, ssm_client):
        with pytest.raises(KeyError):
            get_timestamp("non_existent_table", ssm_client)

    def test_successful_retrieval(self, ssm_client):
        ssm_client.put_parameter(
            Name="example_table_latest_extracted",
            Value="2024-05-16T10:40:30.962473",
            Type="String",
        )

        ssm_client.put_parameter(
            Name="example_table_latest_extracted",
            Value="2024-05-16T10:50:30.123456",
            Type="String",
            Overwrite=True,
        )

        # Get the latest timestamp
        timestamp = get_timestamp("example_table", ssm_client)
        assert timestamp == "2024-05-16T10:50:30.123456"

    # TODO: Add a test for connection issues
    # def test_connection_issue(self):
    #     # Set up an SSM client without credentials
    #     ssm_client = boto3.client("ssm")
    #     with self.assertRaises(NoCredentialsError):
    #         ssm_client.get_parameter(Name='example_table')


class TestWriteTimestamp:

    def test_timestamp_writtem_to_param_store(self, ssm_client):
        time_to_write = datetime.fromisoformat("2024-05-16T10:50:30.123456")
        write_timestamp(time_to_write, "test_table", ssm_client)
        timestamp = get_timestamp("test_table", ssm_client)
        assert str(timestamp) == "2024-05-16T10:50:30.123456"


class TestCollectTableData:
    
    def test_returns_list_of_dicts(self):


class TestFindLatestTimestamp:
    pass

class TestWriteTableDataToS3:
    pass

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
        assert id == 00000101

    # TODO: Add a test for connection issues

class TestWriteSeqId:

    def test_id_writtem_to_param_store(self, ssm_client):
        id_to_write = 00000101
        write_timestamp(id_to_write, "test_table", ssm_client)
        id = get_seq_id("test_table", ssm_client)
        assert id == 00000101