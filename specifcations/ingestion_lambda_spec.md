# Ingestion Lambda

A Python application to check for changes to the database tables and ingest any new or updated data

## Overview

- **Use:** Lambda
- **Terraform Objects**
- **Lambda function** to run ingest
- **Permissions**... like lots of them
- **Inputs:** Event triggered on regular schedule by Eventbridge
- **Processes:**
     1. Query OLTP database and return all new records. As we can't mark ingested in the db, our querys should check timestamps for any newer than the previous most recent ingested for each table, then collect all newer records. Also collect any with an updated timestamp newer than this time.
     2. Record the latest timestamp ingested for each table for future reference (in Parameter Store?)
     3. Add an object per table to ingestion s3 bucket, storing the data in ... json lines format?
     4. Record success/failure, quantity of data ingested, timestamp. Log to CloudWatch
     5. On failure, wait a few mins and retry. On multiple failures, send an alert via Cloudwatch and trigger an email to administrators. Should we set up a new account for this?
     6. Add functionality to allow
- **Other Notes**
  - How to store the latest record ingested? This may go in AWS Parameter Store?
  - How to check for historic records that have been updated?
  - Check timestamps

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
