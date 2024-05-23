from lambda_utils import write_table_data_to_warehouse
import pandas as pd

df = pd.DataFrame({'id': [1, 2], 'Name': ["Steve", "Sandy"]})

write_table_data_to_warehouse(df,"name",None)