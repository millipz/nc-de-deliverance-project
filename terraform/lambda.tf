resource "aws_lambda_function" "ingestion_function" {
    function_name = "ingestion_function"
    role = aws_iam_role.lambda_exec_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = "lambda_function.zip"

    environment {
        variables = {
            S3_BUCKET = aws_s3_bucket.ingestion_bucket.bucket
            # DB_HOST   = 
            DB_USER   = var.db_username
            DB_PASSWORD = var.db_password
            DB_NAME   = "totesys_sample_data"
        }
    }

    source_code_hash = data.archive_file.lambda_package.output_sha256
}