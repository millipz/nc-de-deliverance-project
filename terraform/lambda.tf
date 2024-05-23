resource "aws_lambda_function" "ingestion_function" {
    function_name = "${var.env_name}-ingestion-function"
    role = aws_iam_role.lambda_exec_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = data.archive_file.ingestion_lambda_package.output_path
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 180
    source_code_hash = "${filebase64sha256(data.archive_file.ingestion_lambda_package.output_path)}"
    environment {
        variables = {
            S3_BUCKET = aws_s3_bucket.ingestion_bucket.bucket
            ENVIRONMENT = "${var.env_name}"
        }
    }
}

resource "aws_lambda_function" "processing_function" {
    function_name = "${var.env_name}-processing-function"
    role = aws_iam_role.lambda_exec_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.11"
    filename = data.archive_file.processing_lambda_package.output_path
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 180
    source_code_hash = data.archive_file.processing_lambda_package.output_sha256
    environment {
        variables = {
            S3_INGESTION_BUCKET = aws_s3_bucket.ingestion_bucket.bucket
            S3_PROCESSED_BUCKET = aws_s3_bucket.processed_bucket.bucket
            ENVIRONMENT = "${var.env_name}"
        }
    }
}

resource "aws_lambda_layer_version" "lambda_layer" {
    layer_name = "totesys-${var.env_name}-lambda-layer"
    filename = data.archive_file.lambda_layer_package.output_path
    compatible_runtimes = ["python3.11"]
    compatible_architectures = ["x86_64"]
    source_code_hash = "${filebase64sha256(data.archive_file.lambda_layer_package.output_path)}"
}