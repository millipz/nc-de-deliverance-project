# Deliverance Data Engineering Project

This repository contains the code and infrastructure for the Totesys Data Engineering project, which aims to build a reliable and resilient data pipeline to extract, transform, and load data from an operational database into a data lake and data warehouse hosted on AWS.

## Project Overview

The primary objective of this project is to showcase skills and knowledge in Python, SQL, database modeling, AWS, operational practices, and Agile methodologies. The project involves the following key components:

1. **Data Ingestion**: A Python application running on AWS Lambda that continually ingests data from the `totesys` database and stores it in an S3 "ingestion" bucket.
2. **Data Processing**: Another Python application running on AWS Lambda that remodels the ingested data into a predefined schema suitable for a data warehouse and stores the processed data in Parquet format in an S3 "processed" bucket.
3. **Data Loading**: A Python application running on AWS Lambda that loads the processed data into a prepared data warehouse hosted on AWS at defined intervals.
4. **Monitoring and Alerting**: Comprehensive logging, monitoring, and alerting mechanisms using AWS CloudWatch to track the progress, detect failures, and trigger email notifications.
5. **Data Visualization**: A QuickSight dashboard that displays useful data from the data warehouse.
6. **Infrastructure as Code**: Automated deployment of the entire infrastructure using Terraform and a CI/CD pipeline with GitHub Actions. Dev, test and prod environments.

## Repository Structure

The repository is organized as follows:

```
.
├── Makefile
├── README.md
├── conventions
│   ├── ci-cd.md
│   ├── code-review.md
│   ├── docs-and-comments.md
│   ├── images
│   ├── pull-request.md
│   ├── terraform.md
│   └── testing.md
├── db
│   ├── connection.py
│   ├── data
│   ├── run_schema.py
│   ├── run_seed.py
│   ├── schema.sql
│   └── seed.py
├── dev-db-terraform
│   ├── dev_db.tf
│   ├── main.tf
│   └── ...
├── python
│   ├── src
│   └── tests
├── requirements.in
├── specifications
│   ├── Deliverance_ETL_architecture_diagram.png
│   ├── Deliverance_ETL_architecture_diagram.svg
│   ├── S3_Data_Storage_Specification.md
│   ├── ingestion_lambda_spec.md
│   ├── project_plan.md
│   ├── specifiction.md
│   └── processing_lambda_spec.md
└── terraform
    ├── data.tf
    ├── dev.tfvars
    ├── eventbridge.tf
    ├── iam.tf
    ├── lambda.tf
    ├── main.tf
    ├── prod.tfvars
    ├── s3.tf
    ├── test.tfvars
    └── variables.tf
```

- `terraform/`: Contains Terraform configuration files for provisioning the AWS infrastructure.
- `python/`: Contains the source code for the Python Lambda functions responsible for data ingestion, processing, and loading. Includes unit tests.
- `.github/workflows/`: Contains GitHub Actions workflows for continuous integration and deployment.
- `README.md`: This file, providing an overview of the project and instructions for setup and deployment.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/totesys-data-engineering.git`
2. Install the required dependencies (e.g., Terraform, AWS CLI, Python, etc.).
3. Configure your AWS credentials and set up the necessary IAM roles and policies.
4. Customize the Terraform configuration files in the `terraform/` directory to match your AWS account and desired settings.
5. Deploy the infrastructure using Terraform: `terraform init` and `terraform apply`.
6. Set up the CI/CD pipeline by configuring the GitHub Actions workflows in the `.github/workflows/` directory.
7. Commit and push your changes to the repository to trigger the CI/CD pipeline and deploy the Lambda functions.
8. Monitor the pipeline execution and check the CloudWatch logs for any issues or failures.
9. Once the deployment is successful, you can trigger the data ingestion process and observe the data flow through the pipeline.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Northcoders](https://northcoders.com/) for providing the project specification and guidance.
- [AWS Documentation](https://docs.aws.amazon.com/) for the comprehensive documentation on AWS services.
- [Terraform Documentation](https://www.terraform.io/docs/) for the Terraform documentation and examples.

Feel free to modify and expand this README as needed to provide more detailed instructions, troubleshooting tips, and any additional information relevant to your project.
