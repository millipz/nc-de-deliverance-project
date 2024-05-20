import pandas as pd
import pyarrow as pa
import json

def retrieve_data(bucket_name: str, object_key: str, s3_client):
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        # data = json.loads(response["Body"].read().decode('utf-8'))
        # dataFrame = pd.read_json(data)
        df = pd.DataFrame(response["Body"])
        return df
    
    except s3_client.exceptions.NoSuchKey:
        raise KeyError(f"The key '{object_key}' does not exist.")