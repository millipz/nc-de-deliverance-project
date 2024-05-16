from pg8000.native import Connection
from dotenv import load_dotenv
import os

load_dotenv(".secrets/db_credentials.env")

db_endpoint = os.getenv("TEST_DB_ENDPOINT")
db_name = os.getenv("TEST_DB_NAME")
db_username = os.getenv("TEST_DB_USERNAME")
db_password = os.getenv("TEST_DB_PASSWORD")

db_host, db_port = db_endpoint.split(":")

db = Connection(
    host=db_host,
    database=db_name,
    user=db_username,
    password=db_password,
    port=int(db_port),
)
