from db.seed import seed
from db.connection import db
from db.data.index import index as data

try:
    print("seeding the database...")
    seed(**data)
except Exception as e:
    print(e)
finally:
    print("closing database connection...")
    db.close()
