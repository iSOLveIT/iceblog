import os
import pytest
from content import app


@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_paths(client):
    """Start with a blank database."""

    rv = client.get('/category/Lifestyle')
    assert b'Lifestyle' in rv.data


def login(client, username, password):
    app.config['SECRET_KEY'] = os.urandom(75)
    return client.post('/admin', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    app.config['SECRET_KEY'] = os.urandom(75)
    return client.get('/admin_dashboard/logout', follow_redirects=True)


def test_login(client):
    """Make sure login and logout works."""
    rv = login(client, "iSOLveIT20", "gigantic")
    assert b'Welcome Mr. Duodu' in rv.data
    assert b'Dashboard' in rv.data
    assert b'iSOLveIT20' in rv.data

    fv = logout(client)
    assert b'Admin Login' in fv.data

