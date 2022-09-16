import psycopg2

# variables
datname = "yourDBname"
db_env = "yourEnvironment"

RDS_HOST="yourHost"
RDS_USER="yourUsername"
RDS_PASS="yourPSWD"
RDS_DB_INIT="postgres"
RDS_PORT="5432"

# initialize connection
db_conn = psycopg2.connect(host=f"{RDS_HOST}",
    user=f"{RDS_USER}",
    password=f"{RDS_PASS}",
    dbname=f"{RDS_DB_INIT}",
    port=f"{RDS_PORT}"
    )

db_cursor = db_conn.cursor()
db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

# get pid number
db_cursor.execute(f"""SELECT pid
    FROM pg_stat_activity
    WHERE datname = '{datname}';
    """)

res_pid = db_cursor.fetchall() # return type list

# kill pid number if anyone access
if len(res_pid) != 0:
    for pidx in res_pid:
        db_cursor.execute(f"""SELECT pg_terminate_backend({pidx[0]})
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{datname}';
            """)
        print(f"""Kill process pid number: {pidx[0]}""")
else:
    print (f"No one access db {datname}")

# drop db process
print(f"Drop db {datname}")
db_cursor.execute(f"""DROP DATABASE {datname};""")

# recreate db process
print(f"Recreate db {datname}")
db_cursor.execute(f"""CREATE DATABASE {datname}
    WITH 
    OWNER = {RDS_USER}
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    CONNECTION LIMIT = -1;
""")
db_cursor.execute(f"""GRANT TEMPORARY ON DATABASE {datname} TO pg_read_all_settings;
GRANT ALL ON DATABASE {datname} TO {RDS_USER};
GRANT TEMPORARY, CONNECT ON DATABASE {datname} TO PUBLIC;
GRANT TEMPORARY ON DATABASE {datname} TO yourGroup;
""")
print(f"Successful recreate db {datname} in {db_env} environment")

# close all connection
db_cursor.close()
db_conn.close()