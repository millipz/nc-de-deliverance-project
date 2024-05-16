data "archive_file" "lambda_package" {
  type        = "zip"
  source_file = "${path.module}/../src/ingestion_function/lambda_function.py"
  output_path = "${path.module}/../src/ingestion_function/lambda_function.zip"
  output_file_mode = "0666"
}

data "archive_file" "layer_package" {
  type        = "zip"
  source_dir = "${path.module}/../layer/"
  output_path = "${path.module}/../src/ingestion_function/layer.zip"
  output_file_mode = "0666"
}