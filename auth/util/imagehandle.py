from util.database import user_collection
from util.database import image_collection
from util.database import token_collection
from util.response import Response
from util.multipart import parse_multipart
import hashlib
import os
def profileimgupdate(request,handler):
    res = Response()
    multipart = parse_multipart(request)
    if 'auth_token' in request.cookies:
        username = token_collection.find_one({'auth_token': hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
        filename = "file" + str(image_collection.count_documents({}) + 1)
        ext = multipart.parts[0].headers.get('Content-Disposition').split('filename="')[1].split('"')[0].split('.')[1]
        if ext != 'jpg' and ext != 'gif' and ext != 'png':
            res.status = 403
            res.text("Invalid file type")
            handler.request.sendall(res.to_data())
            return
        with open(os.path.join("public","imgs","profile-pics",(filename + "." + ext)), "wb") as image:
            image.write(multipart.parts[0].content)
        image_collection.insert_one({'username': username,'filename': filename, 'filepath': "/public/imgs/profile-pics/" + filename + "." + ext})
        user_collection.update_one({'username': username}, {'$set':{'imageURL': "/public/imgs/profile-pics/" + filename + "." + ext}})
        res.text("Image Updated")
        handler.request.sendall(res.to_data())
        return
    res.text("Image upload failed")
    res.set_status(400, "Image upload failed")
    handler.request.sendall(res.to_data())