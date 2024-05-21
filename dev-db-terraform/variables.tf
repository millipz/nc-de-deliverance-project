variable "db_username" {
  description = "Dev database administrator username"
  type        = string
  sensitive   = true
}
 
variable "db_password" {
  description = "Dev database administrator password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Dev database name"
  type        = string
  sensitive   = true
}