data "archive_file" "lambda_package" {
  type        = "zip"
  source_file = "${path.module}/../src/lambda_function.py"
  output_path = "${path.module}/../src/lambda_function.zip"
  output_file_mode = "0666"
}

data "archive_file" "layer_package" {
  type        = "zip"
  source_dir = "${path.module}/../layer/"
  output_path = "${path.module}/../src/layer.zip"
  output_file_mode = "0666"
}