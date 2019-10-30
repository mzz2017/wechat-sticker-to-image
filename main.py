# encoding=utf-8
import itchat
import time
from itchat.content import *
import os
import io
import hashlib
import redis


global pool


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


@itchat.msg_register(PICTURE)
def download_files(msg):
    msg.download(msg.fileName)
    md5 = GetFileMd5(msg.fileName)
    print("MD5 of the file sending:", md5)
    R = redis.Redis(connection_pool=pool)
    media = R.get(md5)
    if media is None:
        with open(msg.fileName, 'rb') as f:
            file_ = f.read()
            prepared_file = {"fileSize": len(
                file_), "fileMd5": md5, "file_": io.BytesIO(file_)}
            res = itchat.upload_file(
                msg.fileName, preparedFile=prepared_file)
            media = res["MediaId"]
            R.set(md5, media)
            print("新文件，MediaId: %s..." %
                  media[:50 if len(media) >= 50 else len(media)])
    else:
        print("已从redis获得文件的MediaId: %s..." %
              media[:50 if len(media) >= 50 else len(media)])
    res = itchat.send_file(msg.fileName, msg['FromUserName'], mediaId=media)
    os.remove(msg.fileName)
    R.close()


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('你好! 向我发送表情包吧, 我会把原图发送给你!')


if __name__ == "__main__":
    global pool
    host = ""
    if "REDIS_HOST" in os.environ:
        host = os.environ["REDIS_HOST"]
    pool = redis.ConnectionPool(
        host="localhost"if host == ""else host, port=6379, decode_responses=True)
    print(pool)
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run(True)
