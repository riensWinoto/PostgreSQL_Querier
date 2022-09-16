import psycopg2
import sys
from decouple import config

#variable input for database and for determine which connection will used
in_env = "yourEnvironment"
in_dbname = "newDBname"

#variable for connection string
RDS_HOST="yourHost"
RDS_USER="yourUsername"
RDS_PASS="yourPSWD"
RDS_DB_INIT="postgres"
RDS_PORT="5432"

#init db connection        
db_conn = psycopg2.connect(
    host=f"{RDS_HOST}",
    user=f"{RDS_USER}",
    password=f"{RDS_PASS}",
    dbname=f"{RDS_DB_INIT}",
    port=f"{RDS_PORT}"
)
db_cursor = db_conn.cursor()
db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

#create new database
print(f"Create {in_dbname} DB in {in_env} environment")
db_cursor.execute(f"""CREATE DATABASE {in_dbname}
    WITH 
    OWNER = {RDS_USER}
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
""")

#set security privileges
print(f"{in_dbname} DB set security privileges")
db_cursor.execute(f"""GRANT TEMPORARY ON DATABASE {in_dbname} TO yourGroup;
GRANT CONNECT, TEMPORARY ON DATABASE {in_dbname} TO PUBLIC;
GRANT CONNECT, TEMPORARY ON DATABASE {in_dbname} TO {RDS_USER};
GRANT ALL ON DATABASE {in_dbname} TO yourGroup;""")

print(f"Finish set security privileges for {in_dbname} DB in {in_env} environment")

db_cursor.close()
db_conn.close()