resource "aws_security_group" "dev_rds_sg" {
  name        = "dev_rds_sg"
  description = "Allow incoming requests"
  ingress {
    description = "PostgreSQL ingress"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_db_instance" "totesys_dev_db" {
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  storage_type           = "gp2"
  engine_version         = "14.9"
  db_name                = aws_secretsmanager_secret_version.dev_db_name_version.secret_string
  username               = aws_secretsmanager_secret_version.dev_db_username_version.secret_string
  password               = aws_secretsmanager_secret_version.dev_db_password_version.secret_string
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.dev_rds_sg.id]
}

resource "local_sensitive_file" "db_credentials" {
  content  = <<EOF
TEST_DB_ENDPOINT="${aws_db_instance.totesys_dev_db.endpoint}"
TEST_DB_NAME="${aws_db_instance.totesys_dev_db.db_name}"
TEST_DB_USERNAME="${aws_db_instance.totesys_dev_db.username}"
TEST_DB_PASSWORD="${aws_db_instance.totesys_dev_db.password}"
EOF
  filename = "${path.module}/../.secrets/db_credentials.env"
}

