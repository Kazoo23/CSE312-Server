import os
import uuid
import pyotp
import dotenv
import bcrypt
import hashlib
import requests
import jwt
from util.database import user_collection
from util.database import token_collection
from util.response import Response
from util.auth import extract_credentials
from util.auth import validate_password

def register(request,handler):
    res = Response()
    [username,password] = extract_credentials(request)
    if not validate_password(password):
        res.set_status(400, '')
        res.text('Invalid password, too weak')
        handler.request.sendall(res.to_data())
        return
    if user_collection.find_one({'username':username}):
        res.set_status(400, '')
        res.text('Username already exists')
        handler.request.sendall(res.to_data())
        return
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    userid = str(user_collection.count_documents({}) + 1)
    user_collection.insert_one({'userid':userid,'password':password,'username':username})
    res.text('User registered successfully')
    handler.request.sendall(res.to_data())
def login(request,handler):
    res = Response()
    credentials = extract_credentials(request)
    if len(credentials) == 3:
        [username, password,totpcode] = credentials
    else:
        totpcode = None
        [username, password] = credentials
    if not user_collection.find_one({'username':username}):
        res.set_status(400, '')
        res.text('User does not exist')
        handler.request.sendall(res.to_data())
        return
    userpassword = user_collection.find_one({'username':username})['password']
    if not bcrypt.checkpw(password.encode(), userpassword.encode()):
        res.set_status(400, '')
        res.text('Incorrect password')
        handler.request.sendall(res.to_data())
        return
    if 'secret' in user_collection.find_one({'username':username}):
        if not totpcode:
            res.set_status(401, 'Unauthorized')
            res.text('2FA is enabled for this account')
            handler.request.sendall(res.to_data())
            return
        else:
            secret = user_collection.find_one({'username':username})['secret']
            totp = pyotp.TOTP(secret)
            if not totp.verify(totpcode):
                res.set_status(401, 'Unauthorized')
                res.text('Incorrect code')
                handler.request.sendall(res.to_data())
                return

    """
    auth = str(uuid.uuid4())
    auth_token = hashlib.sha256(auth.encode()).hexdigest()
    token_collection.insert_one({'username':username,'auth_token':auth_token})
    res.cookies({'auth_token':auth + '; HttpOnly; Secure;'})
    """

    secret = open(os.path.join("jwt","private.key"), 'rb').read()

    payload = {"username": username}

    userjwt = jwt.encode(payload,secret,algorithm="RS256")

    res.cookies({'jwt':userjwt + '; HttpOnly; Secure;'})

    res.text('Login successful')
    handler.request.sendall(res.to_data())
def logout(request,handler):
    res = Response()
    if 'auth_token' not in request.cookies:
        res.set_status(404, 'Not Found')
        res.text('Not logged in')
        handler.request.sendall(res.to_data())
        return
    auth = request.cookies.get('auth_token')
    token_collection.delete_one({'auth_token':hashlib.sha256(auth.encode()).hexdigest()})
    res.cookies({'auth_token':auth + '; HttpOnly; Max-Age=0'})
    res.text('Logout successful')
    res.headers({'Location':'http://localhost:8080'})
    res.set_status(302,'')
    handler.request.sendall(res.to_data())
def user(request,handler):
    res = Response()
    if 'jwt' in request.cookies:
        publicjwt = request.cookies.get('jwt')
        with open(os.path.join("public.key"), 'rb') as f:
            public = f.read()
        print(publicjwt)
        print(public)
        publicjwt = jwt.decode(publicjwt, public, algorithms=["RS256"])
        username = publicjwt['username']
        userid = user_collection.find_one({'username': username})['userid']
        if user_collection.find_one({'username': username}).get('imageURL') is not None:
            imageurl = user_collection.find_one({'username': username})['imageURL']
            res.json({'username': username, 'id': userid, 'imageURL': imageurl})
        else:
            res.json({'username': username, 'id': userid})
        handler.request.sendall(res.to_data())
        return
    res.set_status(401, 'Unauthorized')
    res.json({})
    handler.request.sendall(res.to_data())
    return
def update(request,handler):
    res = Response()
    if 'auth_token' not in request.cookies:
        res.set_status(401, '')
        res.text('Not logged in')
        handler.request.sendall(res.to_data())
        return
    [newusername,newpassword] = extract_credentials(request)
    username = token_collection.find_one({'auth_token':hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
    if username != newusername and user_collection.find_one({'username':newusername}):
        res.set_status(400, '')
        res.text('Invalid username')
        handler.request.sendall(res.to_data())
        return
    userid = user_collection.find_one({'username':username})['userid']
    if newpassword:
        if not validate_password(newpassword):
            res.set_status(400, '')
            res.text('Invalid password')
            handler.request.sendall(res.to_data())
            return
        else:
            newpassword = bcrypt.hashpw(newpassword.encode(), bcrypt.gensalt()).decode()
            user_collection.update_one({'userid': userid}, {'$set':{'password': newpassword}})
    else:
        user_collection.update_one({'userid': userid}, {'$set':{'username': newusername}})
    token_collection.update_one({'username':username},{'$set':{'username': newusername}})
    res.text('User updated successfully')
    handler.request.sendall(res.to_data())
def search(request,handler):
    res = Response()
    username = request.path.split('?')[1]
    username = username.split('=')[1]
    if username == '':
        accounts = []
        accounts = {'users': accounts}
        res.json(accounts)
        handler.request.sendall(res.to_data())
        return
    raw_accounts = user_collection.find({'username':{'$regex':username}})
    accounts = []
    for acc in raw_accounts:
        accounts.append({
            'id': acc['userid'],
            'username': acc['username'],
        })
    accounts = {'users' : accounts}
    res.json(accounts)
    handler.request.sendall(res.to_data())
def generatetwofa(request,handler):
    res = Response()
    if 'auth_token' in request.cookies:
        secret = pyotp.random_base32()
        username = token_collection.find_one({'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
        user_collection.update_one({'username': username}, {'$set': {'secret': secret}})
        res.json({'secret': secret})
        handler.request.sendall(res.to_data())
        return
    res.set_status(401,'unauthorized')
    res.text('not signed in')
    handler.request.sendall(res.to_data())
    return
def githubauthcode(request,handler):
    res = Response()
    config = dotenv.dotenv_values(".env")
    location = "https://github.com/login/oauth/authorize?client_id=" + config['GITHUB_CLIENT_ID'] + "&redirect_uri=" + config['REDIRECT_URI'] + '&scope=user:email&scope=repo'
    res.text("request sent")
    res.headers({'Location':location})
    res.set_status(302,'')
    handler.request.sendall(res.to_data())
    return
def githubauth(request,handler):
    res = Response()
    config = dotenv.dotenv_values(".env")
    code = request.path.split('?')[1].split('=')[1]
    params = {"client_id": config['GITHUB_CLIENT_ID'], "client_secret": config['GITHUB_CLIENT_SECRET'], "code": code}
    response = requests.post('https://github.com/login/oauth/access_token', headers= {'Accept': 'application/json'}, params=params)
    access_token = response.json()['access_token']
    userinfo = requests.get('https://api.github.com/user', headers={'Authorization': 'Bearer ' + access_token}).json()
    username = userinfo['login']

    if not user_collection.find_one({'username': username}):
        password = bcrypt.hashpw(uuid.uuid4().hex.encode(), bcrypt.gensalt()).decode()
        userid = str(user_collection.count_documents({}) + 1)
        user_collection.insert_one({'userid': userid, 'password': password, 'username': username})
    auth = str(uuid.uuid4())
    auth_token = hashlib.sha256(auth.encode()).hexdigest()
    token_collection.insert_one({'username': username, 'auth_token': auth_token})
    res.cookies({'auth_token': auth + '; HttpOnly'})
    res.text('Login successful')
    res.headers({'Location':'http://localhost:8080'})
    res.set_status(302,'')
    handler.request.sendall(res.to_data())
