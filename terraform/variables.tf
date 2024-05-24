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