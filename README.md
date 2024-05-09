# The Data Engineering Project

**Read this document carefully - it contains (almost) all you need to know about the project!**

## Objective

The project phase is intended to allow you to showcase some of the skills and knowledge you have acquired over the past few weeks. You will create applications that will Extract, Transform, and Load data from a prepared source into a data lake and warehouse hosted in AWS. Your solution should be reliable, resilient, and (as far as possible) deployed and managed in code.

By the end of the project, you should have:
- written some applications in Python that interact with AWS and database infrastructure and manipulate data as required
- remodelled data into a data warehouse hosted in AWS
- demonstrated that your project is well-monitored and that you can measure its performance
- deployed at least part of the project using scripting or automation.

Your solution should showcase your knowledge of Python, SQL, database modelling, AWS, good operational practices, and Agile working.

## The Minimum Viable Product (MVP)

The intention is to create a data platform that extracts data from an operational database (and potentially other sources), archives it in a data lake, and makes it available in a remodelled OLAP data warehouse.

The project is open-ended and could include any number of features, but **at a minimum**, you should seek to deliver the following:
- Two S3 buckets (one for ingested data and one for processed data). Both buckets should be structured and well-organised so that data is easy to find. Data should be **immutable** - i.e. once you have written data to S3, it should not be amended or over-written. You should create new data files containing additions or amendments.
- A Python application that continually ingests all tables from the `totesys` database (details below). The data should be saved in files in the "ingestion" S3 bucket in a suitable format. The application must:
  - operate automatically on a schedule
  - log progress to Cloudwatch
  - trigger email alerts in the event of failures
  - follow good security practices (for example, preventing SQL injection and maintaining password security)
- A Python application that remodels __at least some__ of the data into a predefined schema suitable for a data warehouse and stores the data in Parquet format in the "processed" S3 bucket. The application must:
  - trigger automatically when it detects the completion of an ingested data job
  - be adequately logged and monitored
  - populate the dimension and fact tables of a single "star" schema in the warehouse (see details below) 
- A Python application that loads the data into a prepared data warehouse at defined intervals. Again the application should be adequately logged and monitored.
- A Quicksight dashboard that allows users to view useful data in the warehouse (more on this below).

All Python code should be thoroughly tested, PEP8 compliant, and tested for security vulnerabilities with the `safety` and `bandit` packages. Test coverage should exceed 90%.

As far as possible, the project should be deployed automatically using infrastucture-as-code and CI/CD techniques.  

You should be able to demonstrate that a change to the source database will be reflected in the data warehouse within 30 minutes at most.

## The Data

The primary data source for the project is a moderately complex (but not very large) database called `totesys` which is meant to simulate the back-end data of a commercial application. Data is inserted and updated into this database several times a day. (The data itself is entirely fake and meaningless, as a brief inspection will confirm.)

Each project team will be given read-only access credentials to this database. The full ERD for the database is detailed [here](https://dbdiagram.io/d/6332fecf7b3d2034ffcaaa92).

In addition, you will be given credentials for a data warehouse hosted in the Northcoders AWS account. The data will have to be remodelled for this warehouse into three overlapping star schemas. You can find the ERDs for these star schemas:
 - ["Sales" schema](https://dbdiagram.io/d/637a423fc9abfc611173f637)
 - ["Purchases" schema](https://dbdiagram.io/d/637b3e8bc9abfc61117419ee)
 - ["Payments" schema](https://dbdiagram.io/d/637b41a5c9abfc6111741ae8)

The overall structure of the resulting data warehouse is shown [here](https://dbdiagram.io/d/63a19c5399cb1f3b55a27eca).

The tables to be ingested from `totesys` are:
|tablename|
|----------|
|counterparty|
|currency|
|department|
|design|
|staff|
|sales_order|
|address|
|payment|
|purchase_order|
|payment_type|
|transaction|

The list of tables in the complete warehouse is:
|tablename|
|---------|
|fact_sales_order|
|fact_purchase_orders|
|fact_payment|
|dim_transaction|
|dim_staff|
|dim_payment_type|
|dim_location|
|dim_design|
|dim_date|
|dim_currency|
|dim_counterparty|

However, for your minimum viable product, you need only populate the following:
|tablename|
|---------|
|fact_sales_order|
|dim_staff|
|dim_location|
|dim_design|
|dim_date|
|dim_currency|
|dim_counterparty|

This should be sufficient for a single [star-schema](https://dbdiagram.io/d/637a423fc9abfc611173f637).

The structure of your "processed" S3 data should reflect these tables.

Note that data types in some columns may have to be changed to conform to the warehouse data model.

### History
Your warehouse should contain a full history of all updates to _facts_. For example, if a sales order is 
created in `totesys` and then later updated (perhaps the `units_sold` field is changed), you should have _two_ 
records in the `fact_sales_order` table. It should be possible to see both the original and changed number
of `units_sold`. It should be possible to query either the current state of the sale, or get a full history
of how it has evolved (including deletion if applicable).

It is _not_ necessary to do this for dimensions (which should not change very much anyway). The warehouse 
should just have the latest version of the dimension values. However, you might want to keep a full
record of changes to dimensions in the S3 buckets.

## The Dashboard
To demonstrate the use of the warehouse, you will be required to display some of the data on an [AWS Quicksight](https://aws.amazon.com/quicksight/) dashboard. **You are not required to know how to construct a Quicksight dashboard** - Northcoders tutors will help with this part. However, you will be required to supply the SQL queries that are used to retrieve the data you wish to display.

This aspect of the project should not be tackled until the final week of the course, more details will be given then. The major focus of your efforts should be to get the data into the data warehouse.

![img](./mvp.png)


## Possible Extensions

If you have time, you can enhance the MVP. The initial focus for any enhancement should be to ensure that all of the tables in the data warehouse are being updated. You could add other desirable features, such as a _schema registry_ or [data catalogue](https://www.alation.com/blog/what-is-a-data-catalog/) that contains the schema of the data you ingest from the database. Using this, you could check that incoming data has the required structure. If there is any anomaly (eg the database has been changed in some way), you can perform a failure action, such as redirecting the data to some sort of default destination (sometimes called a _dead letter queue_). 

Another simple addition (which might make your presentation more visually appealing) could be a Jupyter Notebook that performs some kind of analysis of the data. (As previously noted, the data is random nonsense, so you won't find any real insights, but it would be good to demonstrate your knowledge of the tools.)

There are several ways to extend the scope of the project. 
1. Ingest data from an external API - eg you could retrieve relevant daily foreign exchange rates from `https://freeforexapi.com/Home/Api`. You can use the `requests` library to make the request and then save the results in S3. Perhaps you can incorporate this data into the warehouse schema?
1. Ingest data from a file source - eg another S3 bucket. We can provide JSON files in a remote S3 bucket that can be fetched at intervals.
1. Create a metadata catalogue for the data in S3 so that it is accessible via Athena.
1. Orchestrate your pipeline with Prefect or similar tool.


## Technical Details

To host your solution, each team will need to host your infrastructure in a single AWS account. You can use one of your Northcoders accounts and give each member of your team credentials to access this. However, these accounts are not permanent. It is likely that you will need several attempts to deploy the infrastructure correctly, so it is in your interest that you script the creation of the resources so that they can be rebuilt as quickly and efficiently as possible.


### Required Components

You need to create:
1. A job scheduler to run the ingestion job. AWS Eventbridge is the recommended way to do this. Since data has to be visible in the data warehouse within 30 minutes of being written to the database, you need to schedule your job to check for changes much more frequently.
1. An S3 bucket that will act as a "landing zone" for ingested data.
1. A Python application to check for changes to the database tables and ingest any new or updated data. It is _strongly_ recommended that you use AWS Lambda as your computing solution. It is possible to use EC2, but it will be much harder to create event-driven jobs, and harder to log events in Cloudwatch. The data should be saved in the "ingestion" S3 bucket in a suitable format. Status and error messages should be logged to Cloudwatch.
1. A Cloudwatch alert should be generated in the event of a major error - this should be sent to email.
1. A second S3 bucket for "processed" data.
1. A Python application to transform data landing in the "ingestion" S3 bucket and place the results in the "processed" S3 bucket. The data should be transformed to conform to the warehouse schema (see above). The job should be triggered by either an S3 event triggered when data lands in the ingestion bucket, or on a schedule. Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.
1. A Python application that will periodically schedule an update of the data warehouse from the data in S3. Again, status and errors should be logged to Cloudwatch, and an alert triggered if a serious error occurs.
1. **In the final week of the course**, you will be asked to provide some SQL to perform a complex query on the data warehouse.
Deployment must be automated. It is strongly recommended that you use Terraform.

## Finally...

This is a fairly realistic simulation of a typical data engineering project. In the real world, such a project would be undertaken over several weeks by a team of experienced data engineers. _It is highly unlikely that you will have time to complete a fully-functioning, "production-ready" solution._ However, you will have an opportunity to tackle lots of the typical problems faced in a real project and put your skills in Python, data, and DevOps to good use. As always, the journey is more important than the destination. 

Above all, don't rush: it will be better to deliver a high-quality MVP than a more complex but poorly-engineered platform. 

Enjoy this! And good luck!
