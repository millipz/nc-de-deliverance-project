from db.connection import db

with open("db/schema.sql", 'r') as schema:
    schema_string = schema.read()
    print(schema_string)
try:
    db.run(schema_string)
except Exception as e:
    print(f"Error has occured executing the SQL file: {e}")

