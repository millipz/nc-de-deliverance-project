#index.rst

<!-- docs documentation master file, created by
sphinx-quickstart on Wed May 22 14:35:50 2024.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->

# Welcome to docs’s documentation!

<a id="module-lambda_utils"></a>

### lambda_utils.collect_table_data(table_name: str, timestamp: datetime, db_conn, column='last_updated')

Returns all data from a table newer than most recent timestamp

* **Parameters:**
  * **table_name** (*string*)
  * **timestamp** (*timestamp*)
  * **db_conn** (*pg8000 database connection*)
* **Raises:**
  * **KeyError** – table_name does not exist
  * **ConnectionError** – connection issue to parameter store
* **Returns:**
  list of dictionaries
  : all data in table, one dictionary
    per row keys will be column headings
* **Return type:**
  table_data (list)

### lambda_utils.find_latest_timestamp(table_data: list[dict], columns=['last_updated'])

Iterates over data from one database table and returns the most recent timestamp

* **Parameters:**
  * **table_data** (*list*) – list of dictionaries representing rows of the table
  * **columns** (*list* *[**str* *]* *,* *optional keyword*) – columns to search for timestamps.
    Defauts to [“last_updated”]
* **Raises:**
  **KeyError** – columns do not exist
* **Returns:**
  from list returns most recent
  : timestamp from created_at/updated_at values
* **Return type:**
  most_recent_timestamp (timestamp)

### lambda_utils.get_seq_id(table_name: str, ssm_client)

From parameter store retrieves table_name : sequential_id key value pair

* **Parameters:**
  **table_name** (*string*)
* **Raises:**
  * **KeyError** – table_name does not exist
  * **ConnectionError** – connection issue to parameter store
* **Returns:**
  sequential_id(int)

### lambda_utils.get_timestamp(table_name: str, ssm_client)

Return timestamp showing most recent entry from the given table
that has been processed by the ingestion lambda.

* **Parameters:**
  * **table_name** (*str*) – table name to get timestamp for
  * **ssm_client** (*boto3 SSM Client*) – secrests manager client passed into func
* **Raises:**
  * **KeyError** – table_name does not exist
  * **ConnectionError** – connection issue to parameter store
* **Returns:**
  stored timestamp of most recent ingested data for given table
* **Return type:**
  timestamp (datetime timestamp)

### lambda_utils.write_seq_id(seq_id: int, table_name: str, ssm_client)

To parameter store write table_name : sequential_id key value pair
– checks sequential_id is one greater than previous sequential_id

* **Parameters:**
  * **table_name** (*string*)
  * **sequential_id** (*int*)
* **Raises:**
  * **KeyError** – table_name does not exist
  * **ConnectionError** – connection issue to parameter store
* **Returns:**
  None

### lambda_utils.write_table_data_to_s3(table_name: str, table_data: list[dict], bucket_name: str, sequential_id: int, s3_client)

Write file to S3 bucket as Json lines format

* **Parameters:**
  * **table_name** (*string*)
  * **table_data** (*list*) – list of dictionaries all data in table,
    one dictionary per row keys will be column headings
  * **s3_client** (*boto3 s3 client*)
* **Raises:**
  * **FileExistsError** – S3 object already exists with the same name
  * **ConnectionError** – connection issue to S3 bucket
* **Returns:**
  The S3 object key the data is written to
* **Return type:**
  key

### lambda_utils.write_timestamp(timestamp: datetime, table_name: str, ssm_client)

Writes timestamp to parameter store for given table

* **Parameters:**
  * **timestamp** (*timestamp*) – timestamp of latest extracted data
  * **table_name** (*str*) – table name to store timestamp for
  * **client** (*boto3 SSM Client*) – client passed in to avoid recreating for each invocation
* **Raises:**
  **ConnectionError** – connection issue to parameter store
* **Returns:**
  None

# Indices and tables

* [Index](genindex.md)
* [Module Index](py-modindex.md)
* [Search Page](search.md)
