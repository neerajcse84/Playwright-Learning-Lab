import psycopg
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="qa_training",
    user="postgres",
    password="postgres"
)


cur = conn.cursor()

cur.execute("SELECT * FROM employee")
results = cur.fetchall()
print(results)
