data "archive_file" "lambda_package" {
  type        = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function.zip"
}