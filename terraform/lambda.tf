resource "aws_lambda_function" "ingestion_function" {
    function_name = "ingestion-function"
    role = aws_iam_role.lambda_exec_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = data.archive_file.ingestion_lambda_package.output_path
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 180
    
    environment {
        variables = {
            S3_INGESTION_BUCKET = aws_s3_bucket.ingestion_bucket.bucket
        }
    }

    source_code_hash = data.archive_file.ingestion_lambda_package.output_sha256
}

resource "aws_lambda_function" "processing_function" {
    function_name = "processing-function"
    role = aws_iam_role.lambda_exec_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = data.archive_file.processing_lambda_package.output_path
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 180
    
    environment {
        variables = {
            S3_INGESTION_BUCKET = aws_s3_bucket.ingestion_bucket.bucket
            S3_PROCESSING_BUCKET = aws_s3_bucket.processing_bucket.bucket
        }
    }

    source_code_hash = data.archive_file.processing_lambda_package.output_sha256
}

resource "aws_lambda_layer_version" "lambda_layer" {
    layer_name = "lambda-layer"
    filename = data.archive_file.lambda_layer_package.output_path
    compatible_runtimes = ["python3.11"]

    source_code_hash = data.archive_file.lambda_layer_package.output_sha256
}