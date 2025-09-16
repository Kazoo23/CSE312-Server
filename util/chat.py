from util.response import Response
from util.database import chat_collection
from util.database import user_collection
import uuid
import json

def createChat(request,handler):
    res =  Response()
    if not request.body:
        res.set_status("404", "Not Found")
        res.text("Empty Body")
        handler.request.sendall(res.to_data())
        return
    if 'session' not in request.cookies:
        userid = str(user_collection.count_documents({}) + 1)
        username = 'user' + str(uuid.uuid4())[:4]
        user_collection.insert_one({'userid': userid, 'name': username})
        res.cookies({'session' : str(userid)})
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
    chat_collection.insert_one({'author':username, 'id': str(currentID + 1),'content': message, 'updated' : False})

def getChats(request,handler):
    res = Response()
    raw_messages = chat_collection.find({})
    messages = []
    for mess in raw_messages:
        messages.append({
            'author' : mess['author'],
            'id' : mess['id'],
            'content' : mess['content'],
            'updated' : mess['updated']
        })
    messages = {'messages':messages}
    res.json(messages)
    handler.request.sendall(res.to_data())

def updateChat(request,handler):
    res = Response()
    messageid = request.path.split('/')[-1]
    message = chat_collection.find_one({'id': messageid})
    if 'session' in request.cookies:
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
    if 'session' in request.cookies:
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