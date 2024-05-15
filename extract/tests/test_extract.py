import unittest
import boto3
import os
import pytest
from moto import mock_aws
from extract.src.extract import retrieve_timestamps

@pytest.fixture(scope="class")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def ssm_client(aws_credentials):
    with mock_aws():
        yield boto3.client("ssm")


def test_table_name_does_not_exist(ssm_client):
    
    with pytest.raises(KeyError):
        retrieve_timestamps('non_existent_table')

def test_successful_retrieval(ssm_client):

    ssm_client.put_parameter(
        Name='example_table',
        Value='2024-05-14T12:00:00',
        Type='String'
    )
    
    ssm_client.put_parameter(
        Name='example_table',
        Value='2024-05-15T13:00:00',
        Type='String',
        Overwrite=True
    )    

    timestamp = retrieve_timestamps('example_table')
    assert timestamp == "2024-05-15T13:00:00"
    

#TODO connection errors should be checked when connecting with credentials 
# def test_connection_issue(ssm_client):
#     with pytest.raises(ConnectionError):
#         ssm_client.get_parameter(Name='example_table')