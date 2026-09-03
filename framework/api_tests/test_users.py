import requests


def test_get_user():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users/1"
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = response.json()

    assert data["id"] == 1
    assert data["username"] == "Bret"

def test_get_non_existing_user():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users/9999"
    )

    assert response.status_code == 404

def test_get_user_by_query_parameter():
    params = {"id": 1}

    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        params=params
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 1

def test_create_user():
    payload = {
    "name": "Neeraj",
    "username": "neeraj",
    "email": "neeraj@example.com"
            }
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
            }
    response = requests.post(
    "https://jsonplaceholder.typicode.com/users",
    json=payload,headers=headers
)
    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Neeraj"
    assert data["username"] == "neeraj"
    assert data["email"] == "neeraj@example.com"
    assert "id" in data
    print(response.request.headers)