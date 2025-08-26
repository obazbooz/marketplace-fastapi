from fastapi.testclient import TestClient
from main import app

clinet = TestClient(app)

def test_correct_input ():
    response = clinet.post("/users/new",
                           data={
                               'username':'osama',
                               'email':'osama@gmail.com',
                               'password':'Osama123!'})
    assert response.status_code == 200

def test_incorrect_username():
    response = clinet.post("/users/new",
                           data={
                               'username':'o$ama',
                               'email':'osama@gmail.com',
                               'password':'Osama123!'})
    assert response.status_code == 400

def test_incorrect_email():
    response = clinet.post("/users/new",
                           data={
                               'username':'osama',
                               'email':'osamagmail',
                               'password':'Osama123!'})
    assert response.status_code == 400

def test_short_password ():
    response = clinet.post("/users/new",
                           data={
                               'username':'osama',
                               'email':'osama@gmail.com',
                               'password':'Osama1!'})
    assert response.status_code == 400

def test_password_missing_uppercase ():
    response = clinet.post("/users/new",
                           data={
                               'username':'osama',
                               'email':'osama@gmail.com',
                               'password':'osama123!'})
    assert response.status_code == 400

def test_password_missing_lowercase ():
    response = clinet.post("/users/new",
                           data={
                               'username':'osama',
                               'email':'osama@gmail.com',
                               'password':'OSAMA123!'})
    assert response.status_code == 400

def test_password_missing_digit ():
    response = clinet.post("/users/new",
                           data={
                               'username':'osama',
                               'email':'osama@gmail.com',
                               'password':'Osamaaa!'})
    assert response.status_code == 400

def test_password_missing_special_character():
    response = clinet.post("/users/new",
                           data={
                               'username': 'osama',
                               'email': 'osama@gmail.com',
                               'password': 'Osama123'})
    assert response.status_code == 400

