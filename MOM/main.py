import hashlib, json
from bottle import run, post, request
from models.User import User

def check_login(username, password):
    User.read()
    success = False
    for key in User.users:
        user = User.users[key]
        #print("[ UserName: "+ user.name + ", PASSWORD: " + user.password.encode('ascii') + "]")
        if user.name == username:
            if user.password == password: #hashlib.sha256(password.encode('ascii')).hexdigest():
                success = True
                break
            else:
                break
    return success

@post('/login')
def do_login():
    payload = json.load(request.body)
    username = payload['username']
    password = payload['password']
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

run(host='localhost', port=8080)