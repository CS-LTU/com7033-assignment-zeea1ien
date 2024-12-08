import pytest
from bcrypt import hashpw, gensalt, checkpw
from app import app, create_user,user_exists,users


users = {}  #mock user for testing

#setup for FLASK Test Client Testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client



#test1: check password hashing works

def test_password_hashing():
    password = "simplepassword"
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
#checking password matches 
    assert checkpw(password.encode('utf-8'), hashed_password)
#check incorrect password does not match
    assert not checkpw("wrongpassword".encode('utf-8'), hashed_password)


# test 2: Register/store hashed passwords

def test_register_user(client):
    # Register a user
    client.post('/add_user', data={
        'username': 'testuser1',
        'password': 'simplepassword1'
    })

    users = {"testuser": "bob1689"}
    # Check if user was added to the users dictionary
    users = {"testuser": "bob1689"}
    users.get('testuser')
    


#Test 3: testing logging in with correct/incorrect passwords
def test_login_user(client):
    username = 'testuser'
    password = 'simplepassword'
    users[username] = hashpw(password.encode('utf-8'), gensalt())  # Store hashed password

    #Login with correct password
    client.post('/loggingIn', data={
        'username': username,
        'password': password
    })
    

    #Login with incorrect password
    client.post('/loggingIn', data={
        'username': username,
        'password': 'wrongpassword'
    })
   