import boto3

def retrieve_timestamps(table_name):
    try:
        ssm_client = boto3.client('ssm')
        
        response = ssm_client.get_parameter(Name=table_name)
        
        timestamp = response['Parameter']['Value']
        return timestamp
    
    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError(f"Table name '{table_name}' does not exist.")
    
    #TODO connection errors should be checked when connecting with credentials so this might not be needed here
    # except (ssm_client.exceptions.ConnectionError):
    #     raise ConnectionError("Connection issue to Parameter Store.")
