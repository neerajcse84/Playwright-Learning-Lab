import requests
import pytest
from app.web.app import app
from unittest.mock import patch
from database.db import get_employee_by_id


# ============================================================
# Positive Test - Create employee and validate API + DB data
# ============================================================
def test_create_employee(created_employee):
    url = "http://localhost:5000/employees"

    payload = {
        "name": "Rahul",
        "email": "rahul_test@gmail.com",
        "contact_number": "9876543210"
    }

    response = requests.post(url, json=payload)

    # API validation
    assert response.status_code == 201

    response_data = response.json()

    assert "employee_id" in response_data
    assert response_data["name"] == payload["name"]
    assert response_data["email"] == payload["email"]
    assert response_data["contact_number"] == payload["contact_number"]

    employee_id = response_data["employee_id"]

    # Give the ID to the fixture for cleanup
    created_employee["employee_id"] = employee_id

    print(f"Created employee ID: {employee_id}")

    # DB validation
    db_employee = get_employee_by_id(employee_id)

    assert db_employee is not None
    assert db_employee["employee_id"] == employee_id
    assert db_employee["name"] == payload["name"]
    assert db_employee["email"] == payload["email"]
    assert db_employee["contact_number"] == payload["contact_number"]


# ============================================================
# Validation Test - Contact number length and format
# ============================================================
@pytest.mark.parametrize("contact_number, expected_status", [
    ("987654321", 400),      # Less than 10 digits
    ("9876543210", 201),     # Exactly 10 digits - valid
    ("98765432101", 400),    # More than 10 digits
    ("98765ABCDE", 400),     # Alphanumeric value
])
def test_contact_number_validation(
    contact_number,
    expected_status,
    created_employee
):

    payload = {
        "name": "Rahul",
        "email": "rahul_test@gmail.com",
        "contact_number": contact_number
    }

    response = requests.post(
        "http://localhost:5000/employees",
        json=payload
    )

    assert response.status_code == expected_status

    # Cleanup employee when valid data creates a record
    if response.status_code == 201:
        created_employee["employee_id"] = response.json()["employee_id"]


# ============================================================
# Negative Test - Missing mandatory fields
# ============================================================
@pytest.mark.parametrize("missing_field", [
    "name",
    "email",
    "contact_number",
])
def test_required_fields(missing_field, created_employee):

    payload = {
        "name": "Rahul",
        "email": "rahul_test@gmail.com",
        "contact_number": "9876543210"
    }

    # Remove one mandatory field
    payload.pop(missing_field)

    response = requests.post(
        "http://localhost:5000/employees",
        json=payload
    )

    assert response.status_code == 400


# ============================================================
# Negative Test - Empty field values
# ============================================================
@pytest.mark.parametrize("field", [
    "name",
    "email",
    "contact_number",
])
def test_empty_fields(field):

    payload = {
        "name": "Rahul",
        "email": "rahul_test@gmail.com",
        "contact_number": "9876543210"
    }

    # Set selected field to an empty string
    payload[field] = ""

    response = requests.post(
        "http://localhost:5000/employees",
        json=payload
    )

    assert response.status_code == 400


# ============================================================
# Negative Test - Blank/whitespace field values
# ============================================================
@pytest.mark.parametrize("field", [
    "name",
    "email",
    "contact_number",
])
def test_blank_fields(field):

    payload = {
        "name": "Rahul",
        "email": "rahul_test@gmail.com",
        "contact_number": "9876543210"
    }

    # Set selected field to whitespace
    payload[field] = "   "

    response = requests.post(
        "http://localhost:5000/employees",
        json=payload
    )

    assert response.status_code == 400


# ============================================================
# Negative Test - Incorrect data types
# ============================================================
@pytest.mark.parametrize("field, value", [
    ("name", 12345),
    ("email", 12345),
    ("contact_number", 12345),
])
def test_wrong_data_type(field, value):

    payload = {
        "name": "Rahul",
        "email": "rahul_test@gmail.com",
        "contact_number": "9876543210"
    }

    # Replace selected field with an incorrect data type
    payload[field] = value

    response = requests.post(
        "http://localhost:5000/employees",
        json=payload
    )

    assert response.status_code == 400


# ============================================================
# Validation Test - Email format
# ============================================================
@pytest.mark.parametrize("email, expected_status", [
    ("rahul@", 400),
    ("rahul.com", 400),
    ("@gmail.com", 400),
    ("rahul@gmail", 400),
    ("rahul_email_test@gmail.com", 201),
])
def test_email_validation(
    email,
    expected_status,
    created_employee
):

    payload = {
        "name": "Rahul",
        "email": email,
        "contact_number": "9876543210"
    }

    response = requests.post(
        "http://localhost:5000/employees",
        json=payload
    )

    assert response.status_code == expected_status

    # Cleanup employee when valid email creates a record
    if response.status_code == 201:
        created_employee["employee_id"] = response.json()["employee_id"]


# ============================================================
# Negative Test - Malformed JSON request body
# ============================================================
def test_malformed_json():

    url = "http://localhost:5000/employees"

    # Missing closing brace makes the JSON invalid
    malformed_payload = '{"name": "Rahul", "email": "rahul@gmail.com"'

    response = requests.post(
        url,
        data=malformed_payload,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400


# ============================================================
# Validation Test - Unknown fields are accepted/ignored
# ============================================================
@pytest.mark.parametrize("unknown_field, value, expected_status", [
    ("salary", 50000, 201),
    ("department", "QA", 201),
    ("address", "Pune", 201),
])
def test_unknown_fields(
    unknown_field,
    value,
    expected_status,
    created_employee
):

    payload = {
        "name": "Rahul",
        "email": "rahul_unknown_field@gmail.com",
        "contact_number": "9876543210"
    }

    # Add an additional field not required by the API
    payload[unknown_field] = value

    response = requests.post(
        "http://localhost:5000/employees",
        json=payload
    )

    assert response.status_code == expected_status

    # Cleanup employee when unknown field is accepted
    if response.status_code == 201:
        employee_id = response.json()["employee_id"]
        created_employee["employee_id"] = employee_id



# Server Error Test - Use Flask test client to simulate DB failure and verify 500 response

def test_create_employee_server_error():

    payload = {
        "name": "Rahul",
        "email": "rahul_500_test@gmail.com",
        "contact_number": "9876543210"
    }

    with patch(
        "app.web.app.db.create_employee",
        side_effect=Exception("Database failure")
    ):
        response = app.test_client().post(
            "/employees",
            json=payload
        )

    assert response.status_code == 500