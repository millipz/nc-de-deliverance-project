# Project Plan

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

You need to create:

1. A job scheduler to run the ingestion job. AWS Eventbridge is the recommended way to do this. Since data has to be visible in the data warehouse within 30 minutes of being written to the database, you need to schedule your job to check for changes much more frequently.
1. An S3 bucket that will act as a "landing zone" for ingested data.
1. A Python application to check for changes to the database tables and ingest any new or updated data. It is _strongly_ recommended that you use AWS Lambda as your computing solution. It is possible to use EC2, but it will be much harder to create event-driven jobs, and harder to log events in Cloudwatch. The data should be saved in the "ingestion" S3 bucket in a suitable format. Status and error messages should be logged to Cloudwatch.
1. A Cloudwatch alert should be generated in the event of a major error - this should be sent to email.
1. A second S3 bucket for "processed" data.
1. A Python application to transform data landing in the "ingestion" S3 bucket and place the results in the "processed" S3 bucket. The data should be transformed to conform to the warehouse schema (see above). The job should be triggered by either an S3 event triggered when data lands in the ingestion bucket, or on a schedule. Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.
1. A Python application that will periodically schedule an update of the data warehouse from the data in S3. Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.
1. **In the final week of the course**, you will be asked to provide some SQL to perform a complex query on the data warehouse.
