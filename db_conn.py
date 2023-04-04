import psycopg2

from config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cursor = conn.cursor()