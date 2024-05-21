variable "ingestion_lambda_handler" {
  description = "Path to the Ingestion Lambda handler"
  type = string
  default = "lambda_function.lambda_handler"
}

variable "env_name" {
  description = "Name of environment"
  type = string
  default = "test"
}

variable "admin_email" {
  description = "Administrator email address for alerts"
  type = string
  sensitive = true
}