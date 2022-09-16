import psycopg2
import sys

# DB variables
rds_host = "yourHost"
rds_user = "yourUsername"
rds_pass = "yourPSWD"
rds_db_init = "postgres"
rds_port = "5432"

# input username
try:
    in_usename = input("Username need to disconnected: ")
except KeyboardInterrupt:
    sys.exit(0)
    
# initialize connection
db_conn = psycopg2.connect(
    host=rds_host,
    user=rds_user,
    password=rds_pass,
    dbname=rds_db_init,
    port=rds_port
)

db_cursor = db_conn.cursor()
db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

# get PID number
try:
    db_cursor.execute(f"""SELECT pid
                      FROM pg_stat_activity
                      WHERE usename = '{in_usename}';
                      """)
except psycopg2.OperationalError as e:
    print(f"No {in_usename} connected to DB")
    db_cursor.close()
    db_conn.close()
    print("Connection to DB disconnected")
    sys.exit(0)

res_pid = db_cursor.fetchall()
    
# disconnect user by kill its pid number
if len(res_pid) != 0:
    for pidx in res_pid:
        db_cursor.execute(f"""SELECT pg_terminate_backend({pidx[0]})
            FROM pg_stat_activity
            WHERE pg_stat_activity.usename = '{in_usename}';
            """)
        print(f"""kill process pid number: {pidx[0]}""")
else:
    print (f"No connection from {in_usename}")

# close all connection
db_cursor.close()
db_conn.close()
print("Connection to DB disconnected")