resource "aws_secretsmanager_secret" "totesys_password" {
 name = "totesys-password"
}

resource "aws_secretsmanager_secret_version" "totesys_password_version" {
  secret_id     = aws_secretsmanager_secret.totesys_password.id
  secret_string = var.totesys_password
}

resource "aws_secretsmanager_secret" "totesys_username" {
 name = "totesys-username"
}

resource "aws_secretsmanager_secret_version" "totesys_username_version" {
  secret_id     = aws_secretsmanager_secret.totesys_username.id
  secret_string = var.totesys_username
}

resource "aws_secretsmanager_secret" "totesys_database" {
 name = "totesys-database"
}

resource "aws_secretsmanager_secret_version" "totesys_database_version" {
  secret_id     = aws_secretsmanager_secret.totesys_database.id
  secret_string = var.totesys_database
}

resource "aws_secretsmanager_secret" "totesys_hostname" {
 name = "totesys-hostname"
}

resource "aws_secretsmanager_secret_version" "totesys_hostname_version" {
  secret_id     = aws_secretsmanager_secret.totesys_hostname.id
  secret_string = var.totesys_hostname
}

resource "aws_secretsmanager_secret" "totesys_port" {
 name = "totesys-port"
}

resource "aws_secretsmanager_secret_version" "totesys_port_version" {
  secret_id     = aws_secretsmanager_secret.totesys_port.id
  secret_string = var.totesys_port
}