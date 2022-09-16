import psycopg2

user_name="yourUsername"

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

#delete user
print("Deleting user")
try:
    db_cursor.execute(f"DROP USER {user_name};")
    print("User have been deleted")
except psycopg2.Error as e:
    print(e)

db_cursor.close()
db_conn.close()