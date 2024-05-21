resource "aws_secretsmanager_secret" "dev_db_username" {
  name = "totesys_dev_db_username"
}

resource "aws_secretsmanager_secret_version" "dev_db_username_version" {
  secret_id     = aws_secretsmanager_secret.dev_db_username.id
  secret_string = var.db_username
}

resource "aws_secretsmanager_secret" "dev_db_password" {
  name = "totesys_dev_db_password"
}

resource "aws_secretsmanager_secret_version" "dev_db_password_version" {
  secret_id     = aws_secretsmanager_secret.dev_db_password.id
  secret_string = var.db_password
}

resource "aws_secretsmanager_secret" "dev_db_name" {
  name = "totesys_dev_db_name"
}

resource "aws_secretsmanager_secret_version" "dev_db_name_version" {
  secret_id     = aws_secretsmanager_secret.dev_db_name.id
  secret_string = var.db_name
}

resource "aws_secretsmanager_secret" "dev_db_endpoint" {
  name = "totesys_dev_db_endpoint"
}

resource "aws_secretsmanager_secret_version" "dev_db_endpoint_version" {
  depends_on = [ aws_db_instance.totesys_dev_db ]
  secret_id     = aws_secretsmanager_secret.dev_db_endpoint.id
  secret_string = "${aws_db_instance.totesys_dev_db.endpoint}"
}