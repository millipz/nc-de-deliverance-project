data "aws_iam_policy_document" "step_function_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
  }
}


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
          aws_s3_bucket.processed_bucket.arn,
          "${aws_s3_bucket.processed_bucket.arn}/*"
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

resource "aws_iam_role" "eventbridge_schedule_policy_exec_role" {
  name = "${var.env_name}-eventbridge_schedule_policy_exec_role"

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
resource "aws_iam_role_policy" "eventbridge_schedule_policy"{
    name = "${var.env_name}-eventbridge_schedule_policy"
    role = aws_iam_role.eventbridge_schedule_policy_exec_role.id
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
              Effect  = "Allow",
              Action = [
                "states:StartExecution"
            ],
            Resource = "*"            
        }
    ]
    })
}

resource "aws_iam_role" "step_function_policy_exec_role" {
  name = "${var.env_name}-step_function_policy_exec_role"
  assume_role_policy = data.aws_iam_policy_document.step_function_assume_role_policy.json
}

resource "aws_iam_role_policy" "step_function_policy"{
    name = "${var.env_name}-step_function_policy"
    role = aws_iam_role.step_function_policy_exec_role.id
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
              Effect  = "Allow",
              Action = [
                "states:StartExecution",
                "Lambda:InvokeFunction"
            ],
            Resource = "*"            
        }
    ]
    })
}
