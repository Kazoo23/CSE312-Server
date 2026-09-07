from util.request import Request
def extract_credentials(request):
    characters = {
        "%21": "!",
        "%40": "@",
        "%23": "#",
        "%24": "$",
        "%5E": "^",
        "%26": "&",
        "%28": "(",
        "%29": ")",
        "%2D": "-",
        "%5F": "_",
        "%3D": "=",
    }
    message = request.body.decode()
    message = message.split('&')
    username = message[0].split('=')[1]
    password = message[1].split('=')[1]
    for char in characters:
        password = password.replace(char, characters[char])
    password = password.replace('%25', '%')
    if len(message) == 3:
        totpcode = message[2].split('=')[1]
        return [username,password,totpcode]
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

def test1():
    request = Request(b'GET /sample_page.html HTTP/2.0\r\nContent-Length: 56\r\n\r\nusername=testuser256&password=askjofbjngaASDJASDFBJ1123I%21%40%24%23%25%5E%26%28%29_-')
    valid = extract_credentials(request)
    print(valid)

if __name__ == '__main__':
    test1()
