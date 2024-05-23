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
  output_path = "${path.module}/../${var.env_name}_layer.zip"
  output_file_mode = "0666"
}

data "aws_secretsmanager_secret" "db_username" {
  name = "totesys_${var.env_name}_db_username"
}

data "aws_secretsmanager_secret_version" "db_username_version" {
  secret_id = data.aws_secretsmanager_secret.db_username.id
}

data "aws_secretsmanager_secret" "db_name" {
  name = "totesys_${var.env_name}_db_name"
}

data "aws_secretsmanager_secret_version" "db_name_version" {
  secret_id = data.aws_secretsmanager_secret.db_name.id
}

data "aws_secretsmanager_secret" "db_password" {
  name = "totesys_${var.env_name}_db_password"
}

data "aws_secretsmanager_secret_version" "db_password_version" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}