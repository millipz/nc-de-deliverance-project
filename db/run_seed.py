from db.seed import seed
from db.connection import db
from db.data.index import index as data

try:
    seed(**data)
except Exception as e:
    print(e)
finally:
    db.close()