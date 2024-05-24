import boto3

env = input("Please input the environment name for which to delete parameters: ")
c = boto3.client("ssm")
param_names = [
    param["Name"]
    for param in c.describe_parameters(
        ParameterFilters=[
            {
                "Key": "Name",
                "Option": "BeginsWith",
                "Values": [env],
            }
        ]
    )["Parameters"]
]

if len(param_names):
    print(f"About to delete {param_names}")
    confirm_delete = input("Are you sure you wish to delete these parameters (y/n): ")
    if confirm_delete == "y":
        for name in param_names:
            print(f"deleting {name} ...")
            c.delete_parameter(Name=name)
    else:
        print("exiting ...... ")
else:
    print(f"No parameters found for {env} environment")
