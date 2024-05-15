from db.seed import seed
from db.connection import db
from db.data.index import index as data

try:
    with open("db/schema.sql", 'r') as schema:
        sql_schema = schema.read()
    db.run(sql_schema)    
    seed(**data)
except Exception as e:
    print(e)
finally:
    db.close()