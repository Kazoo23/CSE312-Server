import os
import jwt
from util.response import Response
from util.database import chat_collection
from util.database import user_collection
from util.database import token_collection
import uuid
import json
import hashlib

def createChat(request,handler):
    res =  Response()
    if not request.body:
        res.set_status("404", "Not Found")
        res.text("Empty Body")
        handler.request.sendall(res.to_data())
        return
    if 'auth_token' in request.cookies:
        auth = request.cookies.get('auth_token')
        username = token_collection.find_one({'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
    if 'jwt' in request.cookies:
        publicjwt = request.cookies.get('jwt')
        with open(os.path.join("public.key"), 'rb') as f:
            public = f.read()
        publicjwt = jwt.decode(publicjwt, public, algorithms=["RS256"])
        username = publicjwt['username']
    else:
        if 'session' not in request.cookies:
            userid = str(user_collection.count_documents({}) + 1)
            username = 'user' + str(uuid.uuid4())[:4]
            user_collection.insert_one({'userid': userid, 'name': username})
            res.cookies({'session': str(userid)})
        else:
            userid = request.cookies['session']
            username = user_collection.find_one({'userid': userid})['name']
    res.text('message sent')
    message = json.loads(request.body)['content']
    message = message.replace('&', '&amp;')
    message = message.replace('<', '&lt;')
    message = message.replace('>', '&gt;')
    handler.request.sendall(res.to_data())
    currentID = chat_collection.count_documents({})
    if user_collection.find_one({'username':username}).get('imageURL') is not None:
        imageurl = user_collection.find_one({'username':username})['imageURL']
        chat_collection.insert_one({'author':username, 'id': str(currentID + 1),'content': message, 'updated' : False, 'imageURL': imageurl})
    else:
        chat_collection.insert_one({'author': username, 'id': str(currentID + 1), 'content': message, 'updated': False})

def getChats(request,handler):
    res = Response()
    raw_messages = chat_collection.find({})
    messages = []
    for mess in raw_messages:
        newmess = ({
            'author' : mess['author'],
            'id' : mess['id'],
            'content' : mess['content'],
            'updated' : mess['updated']
        })
        if mess.get('imageURL') is not None:
            newmess.update({'imageURL': mess['imageURL']})
        messages.append(newmess)
    messages = {'messages':messages}
    res.json(messages)
    handler.request.sendall(res.to_data())

def updateChat(request,handler):
    res = Response()
    messageid = request.path.split('/')[-1]
    message = chat_collection.find_one({'id': messageid})
    if 'auth_token' in request.cookies:
        authtoken = request.cookies['auth_token']
        username = token_collection.find_one({'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
        if not username:
            res.set_status(404, 'Not Found')
            res.text('Message not found')
        if username != message['author']:
            res.set_status(403, 'forbidden')
            res.text('Forbidden')
        else:
            message = json.loads(request.body)['content']
            message = message.replace('&', '&amp;')
            message = message.replace('<', '&lt;')
            message = message.replace('>', '&gt;')
            chat_collection.update_one({'id': messageid}, {'$set': {'updated': True, 'content': message}})
            res.text('Message updated')
    elif "jwt" in request.cookies:
        publicjwt = request.cookies.get('jwt')
        with open(os.path.join("public.key"), 'rb') as f:
            public = f.read()
        publicjwt = jwt.decode(publicjwt, public, algorithms=["RS256"])
        username = publicjwt['username']
        if not username:
            res.set_status(404, 'Not Found')
            res.text('Message not found')
        if username != message['author']:
            res.set_status(403, 'forbidden')
            res.text('Forbidden')
        else:
            message = json.loads(request.body)['content']
            message = message.replace('&', '&amp;')
            message = message.replace('<', '&lt;')
            message = message.replace('>', '&gt;')
            chat_collection.update_one({'id': messageid}, {'$set': {'updated': True, 'content': message}})
            res.text('Message updated')
    elif 'session' in request.cookies:
        userid = request.cookies['session']
        username = user_collection.find_one({'userid': userid})['name']
        if not username:
            res.set_status(404, 'Not Found')
            res.text('Message not found')
        if username != message['author']:
            res.set_status(403, 'forbidden')
            res.text('Forbidden')
        else:
            message = json.loads(request.body)['content']
            message = message.replace('&', '&amp;')
            message = message.replace('<', '&lt;')
            message = message.replace('>', '&gt;')
            chat_collection.update_one({'id': messageid}, {'$set': {'updated' : True, 'content' : message}})
            res.text('Message updated')
    else:
        res.set_status(403, 'Not Found')
        res.text('Forbidden')
    handler.request.sendall(res.to_data())

def deleteChat(request,handler):
    res = Response()
    messageid = request.path.split('/')[-1]
    message = chat_collection.find_one({'id': messageid})
    if 'auth_token' in request.cookies:
        authtoken = request.cookies['auth_token']
        username = token_collection.find_one({'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
        if not username:
            res.set_status(404, 'Not Found')
            res.text('Message not found')
        if username != message['author']:
            res.set_status(403, 'forbidden')
            res.text('Forbidden')
        else:
            chat_collection.delete_one({'id': messageid})
            res.text('Message deleted')
    elif 'jwt' in request.cookies:
        publicjwt = request.cookies.get('jwt')
        with open(os.path.join("public.key"), 'rb') as f:
            public = f.read()
        publicjwt = jwt.decode(publicjwt, public, algorithms=["RS256"])
        username = publicjwt['username']
        if not username:
            res.set_status(404, 'Not Found')
            res.text('Message not found')
        if username != message['author']:
            res.set_status(403, 'forbidden')
            res.text('Forbidden')
        else:
            chat_collection.delete_one({'id': messageid})
            res.text('Message deleted')
    elif 'session' in request.cookies:
        userid = request.cookies['session']
        username = user_collection.find_one({'userid': userid})['name']
        if not username:
            res.set_status(404, 'Not Found')
            res.text('Message not found')
        if username != message['author']:
            res.set_status(403, 'forbidden')
            res.text('Forbidden')
        else:
            chat_collection.delete_one({'id': messageid})
            res.text('Message deleted')
    else:
        res.set_status(403, 'Not Found')
        res.text('Forbidden')
    handler.request.sendall(res.to_data())