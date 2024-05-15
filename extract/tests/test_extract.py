import unittest
import boto3
import os
from moto import mock_aws
from extract.src.extract import retrieve_timestamps

@mock_aws
class TestRetrieveTimestamps(unittest.TestCase):

    def setUp(self):
        os.environ["AWS_ACCESS_KEY_ID"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["AWS_SECURITY_TOKEN"] = "test"
        os.environ["AWS_SESSION_TOKEN"] = "test"
        os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

        self.ssm_client = boto3.client("ssm")

    def test_table_name_does_not_exist(self):
        with self.assertRaises(KeyError):
            retrieve_timestamps('non_existent_table')

    def test_successful_retrieval(self):
        # Store multiple timestamps with different values in Parameter Store
        self.ssm_client.put_parameter(
            Name='example_table',
            Value='2024-05-14T12:00:00',
            Type='String'
        )

        self.ssm_client.put_parameter(
            Name='example_table',
            Value='2024-05-15T13:00:00',
            Type='String',
            Overwrite=True
        )    

        # Retrieve the latest timestamp
        timestamp = retrieve_timestamps('example_table')
        self.assertEqual(timestamp, "2024-05-15T13:00:00")

    # TODO: Add a test for connection issues
    # def test_connection_issue(self):
    #     # Set up an SSM client without credentials
    #     ssm_client = boto3.client("ssm")
    #     with self.assertRaises(NoCredentialsError):
    #         ssm_client.get_parameter(Name='example_table')