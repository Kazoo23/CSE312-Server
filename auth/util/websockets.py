import hashlib
import base64
import json

import requests

from util.frame import Frame
from util.response import Response
from util.database import drawing_collection
from util.database import token_collection
from util.database import call_collection

userList = []
socketsList = {}

def compute_accept(key):
    key = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode())
    key = base64.b64encode(key.digest()).decode()
    return key


def parse_ws_frame(raw_frame):
    frame = Frame()
    frame.fin_bit = int((raw_frame[0] & 128) >> 7)
    frame.opcode = int(raw_frame[0] & 15)
    #print(raw_frame[1] & 128)
    mask = int((raw_frame[1] & 128) >> 7)
    length = int(raw_frame[1] & 127)
    #print(length)
    if length == 126:
        frame.payload_length = int.from_bytes(raw_frame[2:4],'big')
        if mask:
            mask = raw_frame[4:8]
            payload = raw_frame[8:]
            for byte in range(0, len(payload)):
                #print(bytes([payload[byte] ^ mask[byte % 4]]))
                frame.payload += bytes([payload[byte] ^ mask[byte % 4]])
        else:
            frame.payload = raw_frame[4:]
    elif length == 127:
        frame.payload_length = int.from_bytes(raw_frame[2:10],'big')
        if mask:
            mask = raw_frame[10:14]
            payload = raw_frame[14:]
            for byte in range(0, len(payload)):
                #print(bytes([payload[byte] ^ mask[byte % 4]]))
                frame.payload += bytes([payload[byte] ^ mask[byte % 4]])
        else:
            frame.payload = raw_frame[18:]
    else:
        frame.payload_length = length
        #print(mask)
        if mask:
            mask = raw_frame[2:6]
            payload = raw_frame[6: 6+length]
            for byte in range(0, len(payload)):
                #print(bytes([payload[byte] ^ mask[byte % 4]]))
                frame.payload += bytes([payload[byte] ^ mask[byte % 4]])
        else:
            frame.payload = raw_frame[2:]
    return frame


def generate_ws_frame(body):
    frame = bytes([0b10000001])
    length = len(body)
    if 126 <= length < 65536:
        frame += (126).to_bytes(1,'big')
        #print(length.to_bytes(2, 'big'))
        frame += length.to_bytes(2, 'big')
        frame += body
    elif length >= 65536:
        frame += (127).to_bytes(1,'big')
        #print(length)
        #print(length.to_bytes(8, 'big'))
        frame += length.to_bytes(8, 'big')
        frame += body
    else:
        #print(length.to_bytes(1, 'big'))
        frame += length.to_bytes(1, 'big')
        frame += body
    return frame

def websocketConnect(request,handler):
    partialData = b""
    fullpayload = b""
    res = Response()
    res.set_status(101, " Switching Protocols")
    key = request.headers.get('Sec-WebSocket-Key')
    res.headers({'Connection': 'Upgrade', 'Upgrade': 'WebSocket',"Sec-WebSocket-Accept": compute_accept(key)})
    handler.request.sendall(res.to_data())
    raw_strokes = drawing_collection.find({})
    strokes = []
    for stroke in raw_strokes:
        strokes.append({
            'startX': stroke['startX'],
            'startY': stroke['startY'],
            'endX': stroke['endX'],
            'endY': stroke['endY'],
            'color': stroke['color'],
        })
    handler.request.sendall(generate_ws_frame(json.dumps({'messageType' : 'init_strokes', 'strokes' : strokes}).encode()))

    if 'auth_token' in request.cookies:
        auth = request.cookies.get('auth_token')
        username = token_collection.find_one({'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
    if not any(user['username'] == username for user in userList):
        userList.append({'username': username, 'connection':handler.request})
    userlist = []
    for user in userList:
        userlist.append({'username': user.get('username')})
    handler.request.sendall(generate_ws_frame(json.dumps({'messageType': 'active_users_list', 'users': userlist}).encode()))
    for user in userList:
        if user['username'] != username:
            user['connection'].sendall(generate_ws_frame(json.dumps({'messageType': 'active_users_list', 'users': userlist}).encode()))

    while True:
        received_data = handler.request.recv(2048)

        if partialData:
            received_data = partialData + received_data
            partialData = b""

        temp_frame = parse_ws_frame(received_data)

        while temp_frame.payload_length > len(temp_frame.payload):
            received_data += handler.request.recv(2048)
            temp_frame = parse_ws_frame(received_data)

        if temp_frame.payload_length < len(temp_frame.payload):
            firstlength = temp_frame.payload_length + 2
            if 126 <= temp_frame.payload_length < 65536:
                firstlength += 2
            elif temp_frame.payload_length >= 65536:
                firstlength += 8
            if int((received_data[1] & 128) >> 7):
                firstlength += 4
            temp_frame = parse_ws_frame(received_data[:firstlength])
            partialData = received_data[firstlength:]

        if temp_frame.fin_bit == 0:
            fullpayload += temp_frame.payload
            continue

        if fullpayload:
            fullpayload += temp_frame.payload
            payload = fullpayload
            fullpayload = b""
        else:
            payload = temp_frame.payload

        if temp_frame.opcode == 8:
            for user in userList:
                if user['username'] == username:
                    userList.remove(user)
            calls = getCalls()
            callId = getCallId(username)
            if callId != -1:
                call = 0
                for tempcall in calls:
                    if tempcall['id'] == callId:
                        call = tempcall
                newusers = call['users']
                newusers = [user for users in newusers if user['username'] != username]
                call_collection.update_one({'id': callId}, {'$set': {'users': newusers}})
                for user in newusers:
                    try:
                        socketsList[user['socketId']].sendall(generate_ws_frame(json.dumps({'messageType': 'user_left', 'socketId': user['socketId']}).encode()))
                    except:
                        socketsList.pop(user['socketId'])

            userlist = []
            for user in userList:
                userlist.append({'username': user.get('username')})
            for user in userList:
                if user['username'] != username:
                    user['connection'].sendall(generate_ws_frame(json.dumps({'messageType': 'active_users_list', 'users': userlist}).encode()))
            return
        if temp_frame.opcode == 1:
            payload = json.loads(payload.decode())
            if payload['messageType'] == "echo_client":
                message = {'messageType': 'echo_server', 'text': payload['text']}
                handler.request.sendall(generate_ws_frame(json.dumps(message).encode()))
            if payload['messageType'] == "drawing":
                stroke = {'startX' : payload['startX'],'startY' : payload['startY'],'endX' : payload['endX'],'endY' : payload['endY'], 'color': payload['color']}
                handler.request.sendall(generate_ws_frame(json.dumps({'messageType':'drawing', **stroke}).encode()))
                userlist = []
                for user in userList:
                    userlist.append({'username': user.get('username')})
                for user in userList:
                    if user['username'] != username:
                        user['connection'].sendall(generate_ws_frame(json.dumps({'messageType':'drawing', **stroke}).encode()))
                drawing_collection.insert_one(stroke)
            if payload['messageType'] == "get_calls":
                calls = getCalls()
                handler.request.sendall(generate_ws_frame(json.dumps({'messageType': 'call_list','calls': calls}).encode()))
            if payload['messageType'] == "join_call":
                username = token_collection.find_one(
                    {'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
                joinCall(payload,handler.request, username)
            if payload['messageType'] == "offer" or payload['messageType'] == "ice_candidate" or payload['messageType'] == "answer":
                username = token_collection.find_one(
                    {'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
                socketId = ""
                senderSocketid = payload['socketId']
                for socketid,socket in socketsList.items():
                    if socket == handler.request:
                        socketId = socketid
                payload['username'] = username
                payload['socketId'] = socketId
                socketsList[int(senderSocketid)].sendall(generate_ws_frame(json.dumps(payload).encode()))
        pass

def getCalls():
    raw_calls = call_collection.find({})
    calls = []
    for call in raw_calls:
        calls.append({
            'id': call['id'],
            'name' : call['name'],
            'users' : call['users'],
        })
    return calls
def getCall(calls, id):
    for call in calls:
        if call['id'] == id:
            return call

def createCall(request,handler):
    res = Response()
    id = str(call_collection.count_documents({}) + 1)
    call = {'id': id, 'name': json.loads(request.body)['name'], 'users': []}
    call_collection.insert_one(call)
    res.json({'id': id})
    handler.request.sendall(res.to_data())

def getCallId(username):
    calls = getCalls()
    callId = -1
    for call in calls:
        for user in call['users']:
            if user['username'] == username:
                callId = call['id']
                break
            if callId != -1:
                break
    return callId

def joinCall(payload, handler,username):
    callId = payload['callId']
    callList = getCalls()
    call = getCall(callList, callId)
    handler.sendall(generate_ws_frame(json.dumps({'messageType': 'call_info', 'name': call.get('name')}).encode()))
    socketId = len(socketsList) + 1
    socketsList[socketId] = handler

    user = {'socketId': socketId, 'username': username}
    otherUsers = call_collection.find_one({'id': callId}).get('users')
    call_collection.update_one({'id': call['id']}, {'$push': {'users': user}})

    mess = {"messageType": "existing_participants",
            "participants": otherUsers}

    handler.sendall(generate_ws_frame(json.dumps(mess).encode()))

    mess = {"messageType": "user_joined", "socketId": socketId, "username": username}

    for user in call_collection.find_one({'id': callId}).get('users'):
        if user['username'] != username:
            socketsList[user['socketId']].sendall(generate_ws_frame(json.dumps(mess).encode()))