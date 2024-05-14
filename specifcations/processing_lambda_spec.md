# Processing Lambda

A Python Lambda application to:

- Collect new data from the ingestion bucket (json lines format) when triggered.
- Process it into into the star schema format as specified by the client's data analysts.
- Write the new data in parquet format to an object in the processed bucket.

## Overview

- **Use:** Lambda
- **Terraform Objects**

  - **Lambda function** to run proccessing
  - **Trigger** based on object landing in ingestion bucket
  - **Permissions**... like lots of them

- **Inputs:** Event triggered when ingest bucket receives a new object
- **Processes:**
  1. Gather data from new object in s3 ingestion bucket
  2. Record the latest object id ingested for reference
  3. If object ids are not sequential, log a warning to cloudwatch
  4. Proccess the data in Python to conform to warehouse schema
  5. Write processed data to a parquet file and save to s3 processed bucket
  6. Record success/failure, quantity of data processed, timestamp. Log to CloudWatch
  7. On failure, wait a few mins and retry. On multiple failures, send an alert via Cloudwatch and tigger an email to administrators.
- **Other Notes**
  - How to store the latest object processed? This may go in AWS Parameter Store?
  - Should we benchmark this lambda and try to optimize it?

## Functions

- Retrieve timestamps from parameter store
  '''
  Return a dictionary with timestamps showing most recent entry from the OLTP database that has been processed
  by the ingestion lambda.
  -- awaiting looking at data in database to confirm how created and updated timestamps are processed

        Args:
            table_name (list): list of all table names to extract data from

        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store

        Returns:
            timestamps (dict) : dictionary of table_name : timestamp key value pairs
        '''

- Write timestamps to parameter store
  '''

        Writes the updated dictionary of table_name : timestamp key value pairs to parameter store

        Args:
            timestamps (dict) : dictionary of table_name : timestamp key value pairs

        Raises:
            ConnectionError : connection issue to parameter store

        Returns:
            None
        '''

- Collect data from one database table
  '''

        Returns all data from a table newer than most recent timestamp

        Args:
            table_name (string)
            timestamp (timestamp)

        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store


        Returns:
            table_data (list) : list of dictionaries all data in table, one dictionary per row keys will be column headings
        '''

- Gathers latest timestamp
  '''

        From Collect data from one database table() returns the most recent timestamp

        Args:
            table_data (list) : list of dictionaries

        Raises:
            KeyError: created_at/updated_at does not exist



        Returns:
            most_recent_timestamp (timestamp) : from list returns most recent timestamp from created_at/updated_at values
        '''

- Write ingested data to S3 bucket per table
  '''

        Write file to S3 bucket as Json lines format

        Args:
            table_name (string)
            timestamp (timestamp)

        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store


        Returns:
            table_data (list) : list of dictionaries all data in table, one dictionary per row keys will be column headings
        '''
