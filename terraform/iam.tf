resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.env_name}-lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Sid    = "",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      },
    ],
  })
}

resource "aws_iam_role_policy" "lambda_exec_policy" {
  name = "${var.env_name}-lambda_exec_policy"
  role = aws_iam_role.lambda_exec_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ],
        Resource = "arn:aws:logs:*:*:*",
      },
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
        ],
        Resource = [
          aws_s3_bucket.ingestion_bucket.arn,
          "${aws_s3_bucket.ingestion_bucket.arn}/*",
        ],
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "secretsmanager:GetSecretValue"
        ],
        "Resource" : "*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "ssm:GetParameter",
          "ssm:PutParameter"
        ],
        "Resource" : "*"
      }
    ],
  })
}
