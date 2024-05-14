from db.seed import seed
from db.connection import db
from db.data.index import index as data

'''
First run the following commands to create the sample_data database and the tables
# psql -f db/sample_data.sql
# psql -f db/schema.sql
'''

try:
    seed(**data)
except Exception as e:
    print(e)
finally:
    db.close()