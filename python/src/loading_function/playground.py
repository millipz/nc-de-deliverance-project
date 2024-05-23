import pandas as pd
from lambda_utils import write_table_data_to_warehouse

df = pd.DataFrame({'col1': [1, 2], 'col2': ["cheese", "bread"]})

write_table_data_to_warehouse(df,"table_name",None)