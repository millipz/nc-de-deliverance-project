{
  "Comment": "NC-totesys-stepfunction",
  "StartAt": "Ingestion Lambda",
  "States": {
    "Ingestion Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:eu-west-2:471112858444:function:${env}-ingestion-function:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 20,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Next": "New Data to Process",
      "OutputPath": "$.Payload"
    },
    "New Data to Process": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.newData",
          "BooleanEquals": false,
          "Next": "Ingestion Pass"
        }
      ],
      "Default": "Processing Lambda"
    },
    "Ingestion Pass": {
      "Type": "Pass",
      "End": true,
      "ResultPath": null
    },
    "Processing Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:eu-west-2:471112858444:function:${env}-processing-function:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 20,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Next": "Loading Lambda"
    },
    "Loading Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:eu-west-2:471112858444:function:${env}-loading-function:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 20,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Next": "Choice"
    },
    "Choice": {
      "Type": "Choice",
      "Choices": [
        {
          "Not": {
            "Variable": "$.statusCode",
            "NumericEquals": 200
          },
          "Next": "Fail"
        }
      ],
      "Default": "Loading Pass"
    },
    "Fail": {
      "Type": "Fail"
    },
    "Loading Pass": {
      "Type": "Pass",
      "End": true
    }
  }
}