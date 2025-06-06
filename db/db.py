import pymysql
import os
from dotenv import load_dotenv
import pymysql.cursors

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database="db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )