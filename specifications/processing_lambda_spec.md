# Processing Lambda Function Specification

- A Python Lambda application to:

  - Collect new data from the ingestion bucket (JSON lines format) when triggered.
  - Process it into the star schema format as specified by the client's data analysts.
  - Write the new data in Parquet format to an object in the processed bucket.

- **Terraform Objects:**

  - **Lambda function:** To run the transformation process.

  - **Permissions**: Including (but not limited to):
    - Access to S3 buckets
    - Access to SSM Parameter Store
    - Access to CloudWatch for logging and monitoring
    - Access to Secrets Manager for retrieving credentials

- **Inputs:** Lambda function triggered by ingestion lambda function once successfully completed. Input JSON payload in the form:

    ```json
    {"packets": [
        {"table": <table_name>, "id": <packet_id>}
        {...}
    ]}
    ```

- **Processes:**
  1. **Extract Object Keys**:
      - Use the table name and packet ID from the input JSON payload to construct the S3 object keys.
      - Retrieve the list of new objects from the "ingestion" S3 bucket.
      - If object IDs are not sequential, log a warning to CloudWatch.

  1. **Transform Data**:
      - Retrieve and read the JSON lines file from the "ingestion" S3 bucket into a pandas DataFrame.
      - Apply transformation logic to convert raw data into the predefined schema.
      - Ensure all foreign key relationships are maintained and data types are correct.
      - Handle date and time conversions appropriately.

  1. **Validate Data**:
      - Validate that the transformed data conforms to the schema.
      - Handle missing or null values appropriately.
      - Log any discrepancies or errors.

  1. **Write Transformed Data to S3**:
      - Convert the transformed DataFrame to Parquet format.
      - Save the Parquet file to the "processed" S3 bucket.
      - Use the structured naming convention for the Parqeut files as set out in the S3 specification.
      - Write packet_id to parameter store.

  1. **Record Processing Status**:
      - Record success or failure, quantity of data processed, and timestamp. Log to CloudWatch.

  1. **Error Handling and Retry Mechanism**:
      - Implement try-except blocks for error handling.
      - In case of failure, wait a few minutes and retry.
      - After multiple failures, send an alert via CloudWatch and trigger an email to administrators.

- **Data Schema**: Transform the data to fit into the following tables:
  - `fact_sales_order`
  - `dim_date`
  - `dim_staff`
  - `dim_location`
  - `dim_currency`
  - `dim_design`
  - `dim_counterparty`

- **Date Handling**: Convert date and time fields to the appropriate formats required by the schema. (timestamp -> date; timestamp -> time)

- **File Naming Convention**: `{tablename}_packet_ID_processed_{timestamp}.parquet`

## Functions

- Retrieve data from S3 ingestion bucket

        """
        Retrieve and read the JSON lines file from S3.

        Args:
            bucket_name (str): The name of the S3 bucket.
            object_key (str): The key of the S3 object.

        Returns:
            DataFrame: The raw data as a pandas DataFrame.
        """

- Transform the data into the the star schema

        """
        Apply transformation logic to convert raw data to predefined schema.

        Args:
            df (DataFrame): The raw data as a pandas DataFrame.

        Returns:
            dict: A dictionary of transformed DataFrames for each table.
        """

- Write data to S3 bucket per table

        '''
        Write file to S3 bucket in Parquet format

        Args:
            table_name (string)
            most_recent_timestamp (timestamp) : timestamp of most recent records in data
            table_data (list) : list of dictionaries all data in table, one dictionary per row keys will be column headings
            packet_id (int) : integer stored in parameter store retrieved earlier in application flow

        Raises:
            FileExistsError: S3 object already exists with the same name
            ConnectionError : connection issue to S3 bucket

        Returns:
            None
        '''

- Read packet_id

        '''
        From parameter store retrieves table_name : packet_id key value pair

        Args:
            table_name (string)

        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store

        Returns:
            packet_id(int)
        '''

- Write packet_id

        '''
        To parameter store write table_name : packet_id key value pair
        -- checks packet_id is one greater than previous packet_id

        Args:
            table_name (string)
            packet_id(int)

        Raises:
            KeyError: table_name does not exist
            ConnectionError : connection issue to parameter store

        Returns:
            None
        '''