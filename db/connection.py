from pg8000.native import Connection

database = 'sample_data'
user = 'oliver'
password = 'letmein'

db = Connection(
    database=database,
    user=user,
    password=password
)
