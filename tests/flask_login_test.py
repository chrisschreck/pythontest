import pytest
from argon2 import PasswordHasher
from frontend.app import create_app
from flask import get_flashed_messages
from neomodel import db

app = create_app()
ph = PasswordHasher()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFlaskLogin:
    def test_login_success(self, client):
        # Define the user credentials for successful login
        user_email = "test4@docportal.com"
        user_password = "12341234"

        # Perform login request
        response = client.post("/login", data={'email': user_email, 'password': user_password}, follow_redirects=True)

        # Assert that login was successful
        assert response.status_code == 200

    def test_login_failure(self, client):
        # Define the user credentials for failed login
        user_email = "nonexistent@docportal.com"
        user_password = "wrongpassword"

        # Perform login request
        response = client.post("/login", data={'email': user_email, 'password': user_password}, follow_redirects=True)

        # Assert that login failed
        assert "['Ungültige E-Mail-Adresse.']" in str(get_flashed_messages(0))
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main()