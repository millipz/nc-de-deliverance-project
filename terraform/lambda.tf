resource "aws_lambda_function" "ingestion_function" {
    function_name = "ingestion-function"
    role = aws_iam_role.lambda_exec_role.arn
    handler = var.ingestion_lambda_handler
    runtime = "python3.11"
    filename = data.archive_file.ingestion_lambda_package.output_path
    layers = [aws_lambda_layer_version.ingestion_lambda_layer.arn]
    timeout = 180
    
    environment {
        variables = {
            S3_BUCKET = aws_s3_bucket.ingestion_bucket.bucket
        }
    }

    source_code_hash = data.archive_file.ingestion_lambda_package.output_sha256
}

resource "aws_lambda_layer_version" "ingestion_lambda_layer" {
    layer_name = "ingestion-lambda"
    filename = data.archive_file.ingestion_layer_package.output_path
    compatible_runtimes = ["python3.11"]

    source_code_hash = data.archive_file.ingestion_layer_package.output_sha256
}