# S3 Data Storage Specification

## Ingestion Bucket: `nc_totesys_ingest`

- **Purpose**: Stores raw data extracted from the `totesys` database.
- **Data Format**: JSON lines.
- **File Naming Convention**: `{tablename}_sequentialID_{timestamp}.json` (e.g., `sales_order_20240510T120000.json`)
- **Storage Structure**:
  - Data is stored in partitioned folders based on the date of ingestion: `yyy-mm-dd/`
  - Example Path: `s3://nc_totesys_ingest/2024-05-10/sales_order_20240510T120000.json`
- **Data Versioning and Immutability**: Versioning enabled to track and manage historical data versions.

## Processed Bucket: `nc_totesys_processed`

- **Purpose**: Stores data transformed and formatted for loading into the data warehouse.
- **Data Format**: Parquet.
- **File Naming Convention**: `{tablename}_sequentialID_processed_{timestamp}.parquet`
- **Storage Structure**:
  - Data is stored in partitioned folders based on dimensions key for the data warehouse, typically date: `yyyy-mm-dd/`
  - Example Path: `s3://nc_totesys_processed/2024-05-10/fact_sales_order_20240510T123000.parquet`
- **Data Lifecycle**: Older data may be transitioned to colder storage (e.g., Amazon S3 Glacier) based on age and access patterns.

# Data Warehouse Schema Specification

## Fact Tables

### Fact Sales Order

- `sales_record_id`: SERIAL (Primary Key, Auto-increment)
- `sales_order_id`: INT
- `created_date`: DATE
- `created_time`: TIME
- `last_updated_date`: DATE
- `last_updated_time`: TIME
- `sales_staff_id`: INT (Foreign Key to `dim_staff`)
- `counterparty_id`: INT (Foreign Key to `dim_counterparty`)
- `units_sold`: INT
- `unit_price`: NUMERIC(10, 2)
- `currency_id`: INT (Foreign Key to `dim_currency`)
- `design_id`: INT (Foreign Key to `dim_design`)
- `agreed_payment_date`: DATE
- `agreed_delivery_date`: DATE
- `agreed_delivery_location_id`: INT (Foreign Key to `dim_location`)

## Dimension Tables

### Dim Staff

- `staff_id`: INT (Primary Key)
- `first_name`: VARCHAR
- `last_name`: VARCHAR
- `department_name`: VARCHAR
- `location`: VARCHAR
- `email_address`: EMAIL

### Dim Currency

- `currency_id`: INT (Primary Key)
- `currency_code`: VARCHAR(3)
- `currency_name`: VARCHAR

### Dim Design

- `design_id`: INT (Primary Key)
- `design_name`: VARCHAR
- `file_location`: VARCHAR
- `file_name`: VARCHAR

### Dim Location

- `location_id`: INT (Primary Key)
- `address_line_1`: VARCHAR
- `address_line_2`: VARCHAR
- `district`: VARCHAR
- `city`: VARCHAR
- `postal_code`: VARCHAR
- `country`: VARCHAR
- `phone`: VARCHAR

### Dim Counterparty

- `counterparty_id`: INT (Primary Key)
- `counterparty_legal_name`: VARCHAR
- `counterparty_legal_address_line_1`: VARCHAR
- `counterparty_legal_address_line_2`: VARCHAR (nullable)
- `counterparty_legal_district`: VARCHAR (nullable)
- `counterparty_legal_city`: VARCHAR
- `counterparty_legal_postal_code`: VARCHAR
- `counterparty_legal_country`: VARCHAR
- `counterparty_legal_phone_number`: VARCHAR

### Dim Date

- `date_id`: DATE (Primary Key)
- `year`: INT
- `month`: INT
- `day`: INT
- `day_of_week`: INT
- `day_name`: VARCHAR
- `month_name`: VARCHAR
- `quarter`: INT
