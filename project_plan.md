# Deliverance Project Plan

## Setup/Admin

1. Pick AWS account and make users for all members
1. Project overall timeline
1. Schedule stand-ups, sprints, pairing
1. Review spec in detail, and write spec for each component
1. Review previous projects and gather tips
1. Set up CI/CD GitHub actions
1. Make project workflow/guidelines (branching all new code, review processes, documentation/docstings, CI/CD, pair programming)
1. Infrastucure diagram/outline with names/spec
1. Create spec/schema for data storage in each part of the system

## For Each Component

1. Create overall specification - interfaces, inputs/outputs, keep up to date
1. Create tickets for each function/feature

## Required Components for MVP

**Note on performance:** data has to be visible in the data warehouse within 30 minutes of being written to the database, we need to schedule to check for changes much more frequently.

0. **Project repo with makefile, CI/CD actions, suitable .gitignore etc.**

1. **Terraform Setup**

   - **AWS Credentials stored in .env file locally**
   - **Database Credentials stored in AWS secretsmanager**
   - **Create state bucket and init backend**

2. **A job scheduler to run the ingestion job.**

   - **Use:** Eventbridge (could we schedule from prefect to make orchestration easier?)
   - **Terraform Objects**
     - **EventBridge scheduler**
   - **Inputs:** None, runs on a timed schedule. Every 10 mins during working hours?
   - **Processes:** Send trigger to Lambda function
   - **Other Notes**

3. **An S3 bucket that will act as a "landing zone" for ingested data.**

   - **Use:** s3
   - **Terraform Objects**
     - **s3 bucket** - _\_deliverance_totes_ingest_[suffix]\_
   - **Inputs:** Receives data ingested from OLTP in json lines format
   - **Processes:** None
   - **Other Notes** Should be a replica of OLTP data with full history

4. **A Python application to check for changes to the database tables and ingest any new or updated data**

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
     5. On failure, wait a few mins and retry. On multiple failures, send an alert via Cloudwatch and tigger an email to administrators. Should we set up a new account for this?
     6. Add functionality to allow 
   - **Other Notes**
     - How to store the latest record ingested? This may go in AWS Parameter Store?
     - How to check for historic records that have been updated?
     - Check timestamps

5. **A second S3 bucket for "processed" data.**

   - **Use:** s3
   - **Terraform Objects**
     - **s3 bucket** - _\_deliverance_totes_proccessed_[suffix]\_
   - **Inputs:** Receives data processed and ready for use in parquet format
   - **Processes:** None
   - **Other Notes** Data should match warehouse schema

6. **A Python application to transform data landing in the "ingestion" S3 bucket and place the results in the "processed" S3 bucket**

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

7. **A Python application that will periodically schedule an update of the data warehouse from the data in S3**

   - **Use:** Lambda
   - **Terraform Objects**

     - **Lambda function** to run update
     - **Trigger** based on object landing in processed bucket
     - **Permissions**... like lots of them

   - **Inputs:** Event triggered when processed bucket receives a new object
   - **Processes:**
     1. Gather data from new objects in s3 processed bucket
     2. Record the latest object ids ingested for reference
     3. If object ids are not sequential, log a warning to cloudwatch
     4. Write data to Warehouse, checking for any failures, errors, or duplicates
     5. Record success/failure, quantity of data processed. Log to CloudWatch
     6. On failure, wait a few mins and retry. On multiple failures, send an alert via Cloudwatch and tigger an email to administrators.
   - **Other Notes**
      - How to store the latest object processed? This may go in AWS Parameter Store?
      - Should we check for duplicate data in the warehouse? Could we enforce this with unique IDs to ensure duplicates are not possible?

8. **In the final week of the course**, you will be asked to provide some SQL to perform a complex query on the data warehouse.

9. **Qucksight Dashboard**
