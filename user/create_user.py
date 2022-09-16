import psycopg2
import random

#variable input for database and for determine which connection will used
in_role = "yourUsername"
in_env = "yourEnvironment"
in_membership = "yourMembership"
max_connection = "-1"

#variable for connection string and assingning membership
RDS_HOST="yourHost"
RDS_USER="yourUsername"
RDS_PASS="yourPSWD"
RDS_DB_INIT="postgres"
RDS_PORT="5432"

#variable for password generator
list_string = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
pass_len = 16
role_pass = "".join(random.sample(list_string,pass_len))

#init db connection        
db_conn = psycopg2.connect(
    host="yourHost",
    user="yourUsername",
    password="yourPSWD",
    dbname="postgres",
    port="5432"
)
db_cursor = db_conn.cursor()
db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

#create new user or service
print(f"Create ROLE {in_role}")
db_cursor.execute(f"""CREATE ROLE {in_role} WITH 
    LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	CONNECTION LIMIT {max_connection}
    PASSWORD '{role_pass}';
""")
print(f"ROLE {in_role} created with password: {role_pass} in {in_env} environment")

#set membership
print(f"ROLE {in_role} set membership")
db_cursor.execute(f"""GRANT {in_membership} TO {in_role};""")
print(f"Finish set membership for ROLE {in_role} to {in_membership}")

db_cursor.close()
db_conn.close()