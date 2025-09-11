from util.response import Response
from util.database import chat_collection
import json

def createChat(request,handler):
    res =  Response()
    if not request.body:
        res.set_status("404", "Not Found")
        res.text("Empty Body")
        handler.request.sendall(res.to_data())
        return
    res.text('message sent')
    message = json.loads(request.body)['content']
    message.replace('&', '&amp;')
    message.replace('<', '&lt;')
    message.replace('>', '&gt;')
    handler.request.sendall(res.to_data())
    currentID = chat_collection.count_documents({})
    chat_collection.insert_one({'author':'auth', 'id': str(currentID + 1),'content': message, 'updated' : False})

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