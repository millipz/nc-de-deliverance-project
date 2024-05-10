resource "aws_iam_policy" "team_deliverance_policy" {
  name        = "team_deliverance_policy"
  description = "Policy for team_deliverance members"
  
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "team_deliverance_role" {
  name               = "team_deliverance_role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "*" }
      Action    = "sts:AssumeRole"
    }]
  })
}


resource "aws_iam_role_policy_attachment" "team_deliverance_policy_attachment" {
  count      = 5
  role       = aws_iam_role.team_deliverance_role[count.index].name
  policy_arn = aws_iam_policy.team_deliverance_policy.arn
}

resource "aws_iam_user" "team_deliverance_member" {
  count = 5
  name  = "team_deliverance_member_${element(["bhwood", "azmolmiah", "pbsingh96", "oliverboyd", "millipz"], count.index)}"
}

resource "aws_iam_user_policy_attachment" "team_deliverance_member_policy_attachment" {
  count      = 5
  user       = aws_iam_user.team_deliverance_member[count.index].name
  policy_arn = aws_iam_policy.team_deliverance_policy.arn
}
