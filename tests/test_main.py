import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.database import get_db,Base

# Test database in memory
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}).connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create database prior to any test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=test_engine)
    print(f"\nSetting up")
    yield
    print(f"\nTearing down")
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)

def test_create_user ():
    payload = {
        "username": "osama",
        "email": "osama@gmail.com",
        "password": "Osama123!",
    }
    response = client.post("/users/new", data= payload)
    assert response.status_code == 200
    data =response.json()
    assert data['username'] == 'osama'
    assert data['email'] == 'osama@gmail.com'
    assert "password" not in data

def test_incorrect_username():
    payload = {
        'username': 'o$ama',
        'email': 'osama@gmail.com',
        'password': 'Osama123!'}
    response = client.post("/users/new", data=payload)
    assert response.status_code == 400

def test_incorrect_email():
    payload = {
        'username': 'osama',
        'email': 'osamagmail',
        'password': 'Osama123!'
    }
    response = client.post("/users/new", data=payload)
    assert response.status_code == 400

def test_short_password():
    payload = {
        'username': 'osama',
        'email': 'osama@gmail.com',
        'password': 'Osama1!'
    }
    response = client.post("/users/new", data=payload)
    assert response.status_code == 400

def test_password_missing_uppercase():
    payload = {
        'username': 'osama',
        'email': 'osama@gmail.com',
        'password': 'osama123!'
    }
    response = client.post("/users/new", data=payload)
    assert response.status_code == 400

def test_password_missing_lowercase():
    payload = {
        'username': 'osama',
        'email': 'osama@gmail.com',
        'password': 'OSAMA123!'
    }
    response = client.post("/users/new", data=payload)
    assert response.status_code == 400

def test_password_missing_digit():
    payload = {
        'username': 'osama',
        'email': 'osama@gmail.com',
        'password': 'Osamaaa!'
    }
    response = client.post("/users/new", data=payload)
    assert response.status_code == 400

def test_password_missing_special_character():
    payload = {
        'username': 'osama',
        'email': 'osama@gmail.com',
        'password': 'Osama123'
    }
    response = client.post("/users/new", data=payload)
    assert response.status_code == 400

def test_get_advertisements():
    advertisement1 = {
        'title': 'laptop',
        'description': 'used laptop',
        'category': 'electronics',
        'price': 1000,
        'location': 'Amsterdam'
    }
    advertisement2 = {
        'title': 'car',
        'description': 'used car',
        'category': 'car',
        'price': 2000,
        'location': 'Lelystad'
    }

    payload = {
        "username": "osama",
        "email": "osama@gmail.com",
        "password": "Osama123!",
    }

    response1 = client.post("/users/new", data= payload)
    assert response1.status_code == 200
    login = client.post("/token", data={"username": "osama", "password": "Osama123!"})
    assert login.status_code == 200
    response_token = login.json()
    token = response_token["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    create1_response = client.post("/advertisements/new",data= advertisement1, headers = headers )
    create2_response = client.post("/advertisements/new", data= advertisement2, headers = headers )
    assert create1_response.status_code == 201
    assert create2_response.status_code == 201
    response2 = client.get("/advertisements")
    assert response2.status_code == 200
    data = response2.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "laptop"


if __name__ == "__main__":
    exit_code = pytest.main(["tests/", "-v"])
    print(f"Tests completed with exit code {exit_code}")