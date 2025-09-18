import json
def extract_credentials(request):
    characters = {
        '!': '%21',
        '@': '%40',
        '#': '%23',
        '$': '%24',
        '%': '%25',
        '^': '%5E',
        '&': '%26',
        '(': '%28',
        ')': '%29',
        '-': '%2D',
        '=': '%3D'
    }
    message = json.loads(request.body)
    message = message.split('&')
    username = message[0].split('=')[1]
    password = message[1].split('=')[1]
    for char in characters:
        password = password.replace(char, characters[char])
    return [username, password]

def validate_password(password):
    valid = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&()-_='
    characters = {
        '!': '%21',
        '@': '%40',
        '#': '%23',
        '$': '%24',
        '%': '%25',
        '^': '%5E',
        '&': '%26',
        '(': '%28',
        ')': '%29',
        '-': '%2D',
        '=': '%3D'
    }
    if len(password) >= 8:
        if password.upper() != password:
            if password.lower() != password:
                numberReq = False
                specialReq = False
                for char in password:
                    if char.isdigit():
                        numberReq = True
                    if char in characters:
                        specialReq = True
                    if char not in valid:
                        return False
                return numberReq and specialReq
    return False