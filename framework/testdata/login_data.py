import pytest

def valid_admin_user():
    return {
        "username": "admin",
        "password": "admin123"
    }

def invalid_password_user():
    return {
        "username": "admin",
        "password": "wrong123"
    }

def unknown_user():
    return {
        "username": "wronguser",
        "password": "admin123"
    }


INVALID_LOGIN_DATA = [
    pytest.param(
        invalid_password_user(),
        "Invalid credentials",
        id="wrong-password",
        marks=pytest.mark.smoke
    ),

    pytest.param(
        {
            "username": "admin",
            "password": "test123"
        },
        "Invalid credentials",
        id="invalid-password"
    ),

    pytest.param(
        unknown_user(),
        "Invalid credentials",
        id="unknown-user"
    )
]

