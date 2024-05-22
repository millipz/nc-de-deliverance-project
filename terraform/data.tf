data "archive_file" "ingestion_lambda_package" {
  type        = "zip"
  source_dir = "${path.module}/../python/src/ingestion_function"
  output_path = "${path.module}/../ingestion_function.zip"
  output_file_mode = "0666"
}

data "archive_file" "processing_lambda_package" {
  type        = "zip"
  source_dir = "${path.module}/../python/src/processing_function"
  output_path = "${path.module}/../processing_function.zip"
  output_file_mode = "0666"
}

data "archive_file" "lambda_layer_package" {
  type        = "zip"
  source_dir = "${path.module}/../layer"
  output_path = "${path.module}/../layer.zip"
  output_file_mode = "0666"
}