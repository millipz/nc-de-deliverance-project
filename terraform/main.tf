terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "nc-de-deliverance-terraform-state"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName = "Deliverance Project"
      Team = "Deliverance"
      DeployedFrom = "Terraform"
      Repository = "https://github.com/millipz/nc-de-deliverance-project"
      CostCentre = "DE"
      Environment = "${var.env_name}"
      RetentionDate = "2024-05-31"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}