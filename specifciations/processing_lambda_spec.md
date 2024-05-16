# Processing Lambda

A Python Lambda application to:

- Collect new data from the ingestion bucket (JSON lines format) when triggered.
- Process it into the star schema format as specified by the client's data analysts.
- Write the new data in Parquet format to an object in the processed bucket.

## Overview

- **Use:** Lambda
- **Terraform Objects**

  - **Lambda function** to run processing.
  - **Permissions**... like lots of them.

- **Inputs:** Lambda function triggered by ingestion lambda function once successfully completed. Input JSON payload in the form:

    ```json
    {"packets": [
        {"table": <table_name>, "id": <sequential_id>}
        {...}
    ]}
    ```

- **Processes:**
  1. Gather data from new object in s3 ingestion bucket.
  1. Check object IDs against payload.
  1. Record success/failure, timestamp. Log to CloudWatch.
  1. If object ids are not sequential, log a warning to CloudWatch.
  1. Record to the parameter store the latest object id ingested.
  1. Proccess the data in Python to conform to warehouse schema.
  1. Write processed data to a Parquet file and save to s3 processed bucket.
  1. Record success/failure, quantity of data processed, timestamp. Log to CloudWatch.
  1. On failure, wait a few mins and retry. On multiple failures, send an alert via CloudWatch and trigger an email to administrators.
- **Other Notes**
  - How to store the latest object processed? This may go in AWS Parameter Store?
  - Should we benchmark this lambda and try to optimise it?

## Functions

- Write ingested data to S3 bucket per table

        '''

        Write file to S3 bucket in Parquet format

        Args:
            table_name (string)
            most_recent_timestamp (timestamp) : timestamp of most recent records in data
            table_data (list) : list of dictionaries all data in table, one dictionary per row keys will be column headings
            sequential_id (int) : integer stored in parameter store retrieved earlier in application flow


        Raises:
            FileExistsError: S3 object already exists with the same name
            ConnectionError : connection issue to S3 bucket

        Returns:
            None
        '''

- Read sequential_id

        '''

        From parameter store retrieves table_name : sequential_id key value pair

        Args:
            table_name (string)


        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store

        Returns:
            sequential_id(int)

        '''

- Write sequential_id

        '''

        To parameter store write table_name : sequential_id key value pair
        -- checks sequential_id is one greater than previous sequential_id

        Args:
            table_name (string)
            sequential_id(int)


        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store

        Returns:
            None
        '''

- Lambda application flow
- Log start of lambda run
  For each table
  - Log entry at start of each run
  - Retrieve timestamps from parameter store
  - Collect data from one database table
  - Gathers latest timestamp
  - Read sequential_id
  - Write ingested data to S3 bucket per table
  - Write sequential_id
  - Log update of table
  - Log completion/errors

            table_data (list) : list of dictionaries all data in table, one dictionary per row keys will be column headings
        '''
