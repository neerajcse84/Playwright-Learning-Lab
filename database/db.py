import psycopg



def get_connection():
    return  psycopg.connect(
    host="localhost",
    port=5432,
    dbname="qa_training",
    user="postgres",
    password="postgres"
)


def get_employees():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT employee_id, name, email, contact_number
        FROM employee
    """)

    rows = cur.fetchall()

    employees = []

    for row in rows:
        employee = {
            "employee_id": row[0],
            "name": row[1],
            "email": row[2],
            "contact_number": row[3]
        }

        employees.append(employee)

    cur.close()
    conn.close()

    return employees


def get_employee_by_id(employee_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT employee_id, name, email, contact_number
        FROM employee
        WHERE employee_id = %s
        """,
        (employee_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "employee_id": row[0],
        "name": row[1],
        "email": row[2],
        "contact_number": row[3]
    }

if __name__ == "__main__":
    employee = get_employee_by_id(101)
    print(employee)