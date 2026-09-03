from flask import Flask, render_template, request, session, redirect, url_for
import os
import database.db as db
import re
app = Flask(__name__)
app.secret_key = "dev-secret-key"


def validate_employee_data(data):
    required_fields = ["name", "email", "contact_number"]

    for field in required_fields:
        if field not in data:
            return {"error": f"{field} is required"}

        if not isinstance(data[field], str):
            return {"error": f"{field} must be a string"}

        if not data[field].strip():
            return {"error": f"{field} cannot be empty"}

    email = data["email"]
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return {"error": "invalid email format"}

    contact_number = data["contact_number"]

    if not contact_number.isdigit():
        return {"error": "contact_number must contain only digits"}

    if len(contact_number) != 10:
        return {"error": "contact_number must be 10 digits"}

    return None


def validate_employee_patch_data(data):

    allowed_fields = ["name", "email", "contact_number"]

    for field in data:

        if field not in allowed_fields:
            return {"error": f"{field} is not allowed"}, 400

        if not isinstance(data[field], str):
            return {"error": f"{field} must be a string"}, 400

        if not data[field].strip():
            return {"error": f"{field} cannot be empty"}, 400

    if "email" in data:
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(email_pattern, data["email"]):
            return {"error": "invalid email format"}, 400

    if "contact_number" in data:

        if not data["contact_number"].isdigit():
            return {"error": "contact_number must contain only digits"}, 400

        if len(data["contact_number"]) != 10:
            return {"error": "contact_number must be 10 digits"}, 400

    return None



@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "admin123":
        session["logged_in"] = True
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Invalid credentials")


@app.route("/dashboard")
def dashboard():
    if session.get("logged_in"):
        return render_template("dashboard.html")

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/employees")
def employees():
    employees = db.get_employees()

    return {
        "employees": employees
    }                    

@app.route("/employees/<int:employee_id>")
def employee(employee_id):
    employee = db.get_employee_by_id(employee_id)

    if employee is None:
        return {"error": "Employee not found"}, 404

    return employee


@app.route("/employees", methods=["POST"])
def create_employee_api():
    data = request.get_json()

    validation_error = validate_employee_data(data)

    if validation_error:
        return validation_error, 400

    name = data["name"]
    email = data["email"]
    contact_number = data["contact_number"]

    employee = db.create_employee(
        name,
        email,
        contact_number
    )

    return employee, 201


@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee_api(employee_id):
    data = request.get_json()

    validation_error = validate_employee_data(data)

    if validation_error:
        return validation_error, 400

    name = data["name"]
    email = data["email"]
    contact_number = data["contact_number"]

    employee = db.update_employee(
        employee_id,
        name,
        email,
        contact_number
    )

    if employee is None:
        return {"error": "Employee not found"}, 404

    return employee, 200


@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee_api(employee_id):

    employee = db.delete_employee(employee_id)

    if employee is None:
        return {"error": "Employee not found"}, 404

    return {"message": "Employee deleted successfully"}, 200


@app.route("/employees/<int:employee_id>", methods=["PATCH"])
def patch_employee_api(employee_id):

    data = request.get_json()

    if not data:
        return {"error": "No fields to update"}, 400

    validation_error = validate_employee_patch_data(data)

    if validation_error:
        return validation_error, 400

    employee = db.update_employee_partial(
        employee_id,
        data
    )

    if employee is None:
        return {"error": "Employee not found"}, 404

    return employee, 200


@app.route("/employee-management")
def employee_management():
    return render_template("employees.html")

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", "5000"))
    app.run(host="0.0.0.0", debug=True, port=port)