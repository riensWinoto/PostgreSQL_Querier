import psycopg2
from decouple import config

#init db connection        
db_conn = psycopg2.connect(
    host="yourHost",
    user="yourUsername",
    password="yourPSWD",
    dbname="postgres",
    port=5432
)
db_cursor = db_conn.cursor()
db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

#list all user
db_cursor.execute(f"""SELECT usename
FROM pg_catalog.pg_user
ORDER BY pg_user asc;
""")
username_list = db_cursor.fetchall()
for each_username_list in username_list:
    for user in each_username_list:
        print(user)

db_cursor.close()
db_conn.close()