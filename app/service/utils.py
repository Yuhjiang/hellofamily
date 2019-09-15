import requests
import os
import base64
from .service_config import Mongodb_uri
import pymongo
from app.tasks import send_async
from jinja2 import Environment, PackageLoader
import secret
from datetime import datetime
from .service_config import API_KEY, APP_ID, SECRET_KEY
from aip import AipFace


env = Environment(loader=PackageLoader('app', 'templates'))
client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def valid_image(image):
    """
    判断是否成功下载了image
    :param image: request.get()的对象
    """
    return image.history == []


def download_picture(url, path, name, **kwargs):
    """
    下载图片
    :param url: 图片链接
    :param path: 保存位置
    :param name: 图片名
    :param kwargs: headers信息
    """
    image = requests.get(url, **kwargs)
    if not valid_image(image):
        raise Exception('Failed to download the picture', url)
    if not os.path.exists(path):
        os.mkdir(path)

    image_path = os.path.join(path, name)
    with open(image_path, 'ab') as f:
        f.write(image.content)


def image_to_base64(image_path):
    """
    图片的base64值
    :param image_path: 图片位置
    :return: base64值
    """
    with open(image_path, 'rb') as image:
        image_base64 = base64.b64encode(image.read())

    return image_base64.decode('utf-8')


def get_cookies():
    db = pymongo.MongoClient(Mongodb_uri)
    client = db['helloproject']
    cookies = client['cookies']

    return cookies.find().sort('update_time', -1).limit(1)[0]


def update_cookies(cookie):
    db = pymongo.MongoClient(Mongodb_uri)
    client = db['helloproject']
    cookies = client['cookies']

    return cookies.insert_one({'cookie': cookie, 'update_time': datetime.now()})


def update_face(image, member):
    image_base64 = base64.b64encode(image).decode('utf-8')
    result = client.addUser(image_base64, 'BASE64', 'Hello_Project', member)

    return result


def send_mail(to='jiang.yuhao0809@gmail.com', subject='运行报错', path='mail/error_notification', **kwargs):
    template = env.get_template(path + '.html')
    html_body = template.render(**kwargs)

    send_async.delay(subject=subject,
                     author=secret.mail_username,
                     to=to,
                     plain=html_body,
                     rich=html_body)
