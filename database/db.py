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

def create_employee(name, email, contact_number):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO employee (name, email, contact_number)
        VALUES (%s, %s, %s)
        RETURNING employee_id
        """,
        (name, email, contact_number)
    )

    row = cur.fetchone()
    conn.commit()

    employee_id = row[0]

    return {
        "employee_id": employee_id,
        "name": name,
        "email": email,
        "contact_number": contact_number
    }
   

def update_employee(employee_id, name, email, contact_number):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE employee
        SET name = %s,
            email = %s,
            contact_number = %s
        WHERE employee_id = %s
        RETURNING employee_id, name, email, contact_number
        """,
        (name, email, contact_number, employee_id)
    )

    row = cur.fetchone()
    conn.commit()

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
    

def delete_employee(employee_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM employee
        WHERE employee_id = %s
        RETURNING employee_id
        """,
        (employee_id,)
    )

    row = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if row is None:
        return None

    return row[0]

def update_employee_partial(employee_id, data):
    conn = get_connection()
    cur = conn.cursor()

    allowed_fields = ["name", "email", "contact_number"]

    fields_to_update = []

    for field in allowed_fields:
        if field in data:
            fields_to_update.append(field)

    if not fields_to_update:
        cur.close()
        conn.close()
        return None

    set_clauses = []

    for field in fields_to_update:
        set_clauses.append(f"{field} = %s")

    set_clause = ", ".join(set_clauses)

    values = []

    for field in fields_to_update:
        values.append(data[field])

    values.append(employee_id)

    query = f"""
        UPDATE employee
        SET {set_clause}
        WHERE employee_id = %s
        RETURNING employee_id, name, email, contact_number
    """

    cur.execute(query, values)

    row = cur.fetchone()
    conn.commit()

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
    create_employee(
        "Amit Kumar",
        "amit@test.com",
        "9876501234"
    )

