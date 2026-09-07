import subprocess

from util.response import Response
from util.request import Request
from util.multipart import parse_multipart
from util.database import video_collection
from util.database import token_collection
from util.database import user_collection
import datetime
import os
import hashlib
import ffmpeg
import json

def upload(request,handler):
    res = Response()
    mult = parse_multipart(request)
    id = str(video_collection.count_documents({}) + 1)
    filename = "file" + id
    path = os.path.join("public", "videos",filename + ".mp4")
    with open(path, "wb") as image:
        image.write(mult.parts[2].content)
    username = token_collection.find_one({'auth_token':hashlib.sha256(request.cookies.get('auth_token').encode()).hexdigest()})['username']
    authorid = user_collection.find_one({'username':username})['userid']
    title = mult.parts[0].content.decode()
    description = mult.parts[1].content.decode()

    filepath = "public/videos/" + filename + ".mp4"
    probe = ffmpeg.probe(filepath)
    duration = float(probe["format"]["duration"])

    times = [0,0.25,0.5,0.75]
    for i in range(len(times)):
        times[i] = float(times[i] * duration)
    count = 0
    thumbnails = []
    for time in times:
        temppath = "public/imgs/thumbnails/" + filename + "_" + str(count) + ".jpg"
        thumbnails.append(temppath)
        ffmpeg.input(filepath, ss=time).output(temppath, vframes=1).run(overwrite_output=True)
        count += 1
    temppath = "public/imgs/thumbnails/" + filename + "_" + str(count) + ".jpg"
    thumbnails.append(temppath)
    ffmpeg.input(filepath, ss='-1').output(temppath, vframes=1).run(overwrite_output=True)

    mainfilename = "main" + id + ".m3u8"
    outputfile = "public/videos/" + filename

    subprocess.run(
        [
            'ffmpeg',
            '-i',
            filepath,
            '-filter_complex', '[0:v]split=2[v1][v2];[v1]scale=1280:720[720out];[v2]scale=426:240[240out]',
            '-map', '[720out]', '-map', '0:a',
            '-map', '[240out]', '-map', '0:a',
            '-hls_segment_filename' , outputfile + '_%v_%d.ts',
            '-f','hls',
            '-master_pl_name' , mainfilename,
            '-var_stream_map', 'v:0,a:0 v:1,a:1',
            outputfile + '_%v.m3u8'
        ]
    )

    video_collection.insert_one({"author_id" : authorid, "title": title, "description" : description , "video_path" : "public/videos/" + filename + '.mp4' , 'id' : id, "created_at": str(datetime.datetime.now()), "thumbnails" : thumbnails , "hls_path" : "public/videos/" + mainfilename})
    res.json({"id" : id})
    handler.request.sendall(res.to_data())
    return


def getallvideos(request,handler):
    res = Response()
    raw_videos = video_collection.find({})
    videos = []
    for video in raw_videos:
        newvideo = ({
            'author_id': video['author_id'],
            'title': video['title'],
            'description': video['description'],
            'video_path': video['video_path'],
            'created_at': video['created_at'],
            'id': video['id'],
            'thumbnails': video['thumbnails'],
            'hls_path': video['hls_path'],
        })
        if video.get('thumbnailURL') is not None:
            newvideo.update({'thumbnailURL': video['thumbnailURL']})
        videos.append(newvideo)
    allvids = {'videos': videos}
    res.json(allvids)
    handler.request.sendall(res.to_data())
    return
def getsinglevideo(request,handler):
    res = Response()
    video_id = request.path.split('/')[-1]
    raw_video = video_collection.find_one({'id':video_id})
    video = ({
            'author_id': raw_video['author_id'],
            'title': raw_video['title'],
            'description': raw_video['description'],
            'video_path': raw_video['video_path'],
            'created_at': raw_video['created_at'],
            'id': raw_video['id'],
            'thumbnails': raw_video['thumbnails'],
            'hls_path': raw_video['hls_path'],
        })
    if raw_video.get('thumbnailURL') is not None:
        video.update({'thumbnailURL': raw_video['thumbnailURL']})
    allvids = {'video': video}
    res.json(allvids)
    handler.request.sendall(res.to_data())
    return
def updatethumbnail(request,handler):
    res = Response()
    thumbnail = json.loads(request.body.decode())["thumbnailURL"]
    video_id = request.path.split('/')[-1].split('=')[-1]
    video_collection.update_one({'id':video_id}, {'$set':{'thumbnailURL': thumbnail}})
    res.json({"message": "Thumbnail updated successfully"})
    handler.request.sendall(res.to_data())
    return