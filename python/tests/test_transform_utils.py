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
import copy
import pandas as pd
import pprint
from python.src.transform_function.transform_utils import (
    retrieve_data
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


# @pytest.fixture(scope="function")
# def create_bucket(s3_client):
#     yield s3_client.create_bucket(Bucket="nc-totesys-ingest", 
#                                   CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

class TestRetrieveData:

    def test_if_object_key_does_not_exist(self, s3_client):
        
        with pytest.raises(KeyError):
            retrieve_data("nc-totesys-ingest", "false-key", s3_client)

    # def test_original_input_data_is_not_mutated(self, s3_client):

    #     s3_client.put_object(Bucket="nc-totesys-ingest", Body="python/tests/s3_test_data.jsonl", Key="test-data")

    #     with open("python/tests/s3_test_data.jsonl") as data_file:

    #         data = json.loads(data_file)

    #         data_copy = copy.deepcopy(data)

    #         result = retrieve_data("nc-totesys-ingest", "test-data", s3_client)

    #         assert data_copy == json.loads()

    def test_function_returns_dataframe(self, s3_client):

        with open("python/tests/s3_test_data.jsonl", 'r', encoding='utf-8') as data_file:

            data = json.load(data_file)    

            s3_client.put_object(Bucket="nc-totesys-ingest", Body=json.dumps(data), Key="test-data")

            result = retrieve_data("nc-totesys-ingest", "test-data", s3_client)
            
            assert isinstance(result, pd.DataFrame)


    def test_successful_retrieval(self, s3_client):
        
        pass

