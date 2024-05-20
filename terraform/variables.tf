variable "db_username" {
  description = "Database administrator username"
  type        = string
  sensitive   = true
}
 
variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

variable "totesys_username" {
  description = "Database read-only username"
  type        = string
  sensitive   = true
}

variable "totesys_password" {
  description = "totesys Database read-only password"
  type        = string
  sensitive   = true
}

variable "totesys_database" {
  description = "Database name"
  type        = string
  sensitive   = true
}

variable "totesys_hostname" {
  description = "totesys Database hostname"
  type        = string
  sensitive   = true
}

variable "totesys_port" {
  description = "totesys Database port"
  type        = string
  sensitive   = true
}

variable "ingestion_lambda_handler" {
  description = "Path to the Ingestion Lambda handler"
  type = string
  default = "lambda_function.lambda_handler"
}