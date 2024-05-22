resource "aws_s3_bucket" "ingestion_bucket" {
    bucket = "nc-totesys-ingest"
}

resource "aws_s3_bucket_versioning" "versioning_example" {
    bucket = aws_s3_bucket.ingestion_bucket.id
    versioning_configuration {
        status = "Enabled"
        }
}

resource "aws_s3_bucket" "processing_bucket" {
    bucket = "nc-totesys-processed"
}

resource "aws_s3_bucket_versioning" "versioning_example" {
    bucket = aws_s3_bucket.processing_bucket.id
    versioning_configuration {
        status = "Enabled"
        }
}