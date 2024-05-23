resource "aws_s3_bucket" "ingestion_bucket" {
    bucket_prefix = "${var.env_name}-nc-totesys-ingest-"
}

resource "aws_s3_bucket_versioning" "ingestion_versioning" {
    bucket = aws_s3_bucket.ingestion_bucket.id
    versioning_configuration {
        status = "Enabled"
        }
}

resource "aws_s3_bucket" "processed_bucket" {
    bucket_prefix = "${var.env_name}-nc-totesys-processed-"
}

resource "aws_s3_bucket_versioning" "processed_versioning" {
    bucket = aws_s3_bucket.processed_bucket.id
    versioning_configuration {
        status = "Enabled"
        }
}