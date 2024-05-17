resource "aws_lambda_function" "ingestion_function" {
    function_name = "ingestion_function"
    role = aws_iam_role.lambda_exec_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = "${path.module}/../src/lambda_function.zip"
    layers = [aws_lambda_layer_version.ingestion_lambda_layer.arn]
    timeout = 180
    
    environment {
        variables = {
            S3_BUCKET = aws_s3_bucket.ingestion_bucket.bucket
        }
    }

    source_code_hash = data.archive_file.lambda_package.output_sha256
}

resource "aws_lambda_layer_version" "ingestion_lambda_layer" {
    layer_name = "ingestion-lambda"
    filename = "${path.module}/../src/layer.zip"
    compatible_runtimes = ["python3.11"]

    source_code_hash = data.archive_file.layer_package.output_sha256
}