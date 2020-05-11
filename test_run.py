import os
import pytest
from content import app


@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.config['TESTING'] = True    # Sets app into testing mode

    with app.test_client() as client:
        yield client    # Creates a generator object


def test_paths(client):
    """Testing the Homepage

    Arguments:
        client {generator object}
    """
    rv = client.get('/')
    assert b'Lifestyle' in rv.data


def login(client, username, password):
    """Function for testing login

    Arguments:
        client {generator object}
        username {str} -- user login name
        password {str} -- user login password

    Returns:
        str -- returns the response received from request made
    """
    app.config['SECRET_KEY'] = os.urandom(20000)
    return client.post('/admin', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Function for testing logout

    Arguments:
        client {generator object}

    Returns:
        str -- returns the response received from request made
    """
    app.config['SECRET_KEY'] = os.urandom(2000)
    return client.get('/admin_dashboard/logout', follow_redirects=True)


def test_login(client):
    """ Function that checks the response received from the request made.
    Make sure there is some information which confirms either the user has logged in or out


    Arguments:
        client {generator object}
    """
    rv = login(client, "USERNAME", "PASSWORD")
    assert b'Welcome Mr. Duodu' in rv.data
    assert b'Dashboard' in rv.data
    assert b'iSOLveIT20' in rv.data

    fv = logout(client)
    assert b'Admin Login' in fv.data
