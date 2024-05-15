from db.connection import db

with open("db/schema.sql", "r") as schema:
    print("initialising database schema...")
    schema_string = schema.read()
try:
    db.run(schema_string)
except Exception as e:
    print(f"Error has occured executing the SQL file: {e}")
