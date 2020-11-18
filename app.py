import pyrebase
from flask import Flask, request
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import json
import os
import base64
import tempfile
import io
import torch
from torchvision import utils
import urllib
import random
from cp_viton.get_mask import get_mask
from cp_viton.test import viton
from face_crop.face_crop import image_divide, image_merge_process
from face_swap.face_swap import face_swap
from face_gen.generate import face_gen
from face_gen.mix import style_mixing
# from flask_login import LoginManager, current_user


config = {
    "apiKey": "AIzaSyBhFS2f6VdcpOXa3qu96xk76RxH4sSjP94",
    "authDomain": "opensource-2020.firebaseapp.com",
    "databaseURL": "https://opensource-2020.firebaseio.com",
    "projectId": "opensource-2020",
    "storageBucket": "opensource-2020.appspot.com",
    "messagingSenderId": "969795252117",
    "appId": "1:969795252117:web:487d5c946b2854735d909c"
}


app = Flask(__name__)
CORS(app)
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
# login = LoginManager(app)
user_id = 0
cloth_img = {}
body_mixing_img = {}
bodys = {}
face_mixing_img = {}
fixed_body = {}
upload_image = {}
model = {}
body_name = {}


def body_init():
    global bodys
    if len(bodys) == 0:
        bodys_name = db.child("bodys").get()
        cnt = 0
        for body in bodys_name.each():
            bodys[cnt] = {}
            url = storage.child(body.val()).get_url(1)
            response = urllib.request.urlopen(url).read()
            # img_file = Image.open(io.BytesIO(response))
            bodys[cnt]['name'] = body.val()
            bodys[cnt]['image'] = base64.b64encode(response).decode('utf8')
            cnt += 1


@ app.route("/addBody", methods=['GET', 'POST'])
def addBody():
    last_body_id = db.child("last_body_id").get().val()
    if last_body_id == None:
        last_body_id = 0

    last_body_id = 0
    db.child('bodys').remove()
    for i in range(10):
        body_address = "./data/body/body"+str(i+1)+".jpg"
        with open(body_address, 'rb') as imageFile:
            a = imageFile.read()
        storage.child("body"+str(last_body_id)).put(a)
        db.child('bodys').push("body"+str(last_body_id))
        last_body_id = last_body_id + 1

    db.child("last_body_id").set(last_body_id)


def base64ToImage(a):
    a += "=" * ((4 - len(a) % 4) % 4)
    im_bytes = base64.b64decode(a)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    b = Image.fromarray(im_arr)
    return b


def image4ToBase64(a):
    b = base64.b64encode(a).decode('utf8')
    return b


def pilImageToCv2Image(a):
    b = np.array(a.convert('RGB'))
    b = b[:, :, ::-1].copy()
    return b


@ app.route("/selectBody", methods=['GET', 'POST'])
def selectBody():
    global cloth_img, body_mixing_img, bodys, body_name

    selecting_bodys = {}
    body_names = {}

    flag = 1
    user_id = 0

    req_data = request.json
    flag = req_data['flag']
    user_id = req_data['user_id']

    if flag == 1:
        cloth = base64ToImage(req_data['cloth'])
        if cloth == None:
            selecting_bodys = body_mixing_img[user_id]
            body_names = bodys[user_id]
        else:
            cloth_img[user_id] = cloth

            # body mixing
            rand_num = []
            #rand_num = np.random.randint(len(bodys), size=len(bodys))
            for i in range(5):
                a = random.randrange(len(bodys))
                while a in rand_num:
                    a = random.randrange(len(bodys))
                rand_num.append(a)

                selecting_bodys[i] = bodys[a]['image']
                body_names[i] = bodys[a]['name']

    else:
        selecting_bodys = body_mixing_img[user_id]
        body_names = body_name[user_id]

    body_mixing_img[user_id] = selecting_bodys
    body_name[user_id] = body_names
    return json.dumps(selecting_bodys)


def merge_face(user_id, body_id):
    global body_name, cloth_img
    cloth = cloth_img[user_id]
    cloth_name = "cloth" + str(user_id) + ".jpg"
    cloth_image = pilImageToCv2Image(cloth)
    fp = './data/test/cloth/' + cloth_name

    #cloth = np.transpose(np.uint8(cloth.numpy()*255), (1, 2, 0))
    r, b = cv2.imencode('.jpg', cloth_image)
    data_encode = np.array(b)
    str_encode = data_encode.tostring()
    # np_img = torch.from_numpy(cloth_image)
    with open(fp, 'wb') as f:
        f.write(str_encode)
        f.flush
    # b.save(fp)
    # utils.save_image(np_img, fp, nrow=1, normalize=True)
    # cloth.save()
    body_names = body_name[user_id]
    get_mask(cloth_name)

    # GMM test
    data_list = [body_names, cloth_name]
    viton('GMM', data_list)

    # TOM test
    viton('TOM', data_list)

    body_address = "./data/result/"+body_names+".jpg"
    with open(body_address, 'rb') as imageFile:
        a = imageFile.read()
    fixed_body[user_id] = base64.b64encode(a).decode('utf8')


@ app.route("/selectFaceFirst", methods=['GET', 'POST'])
def selectFaceFirst():

    selecting_bodys = {}

    for i in range(5):
        body_address = "./data/test/cloth/000048_1.jpg"
        with open(body_address, 'rb') as imageFile:
            a = base64.b64encode(imageFile.read()).decode('utf8')
        # body = cv2.imread(body_address)
        selecting_bodys[i] = a
    return json.dumps(selecting_bodys)
    global body_mixing_img, face_mixing_img
    global fixed_body, bodys

    selecting_faces = {}
    style_v = {}

    req_data = request.json
    flag = req_data['flag']
    user_id = req_data['user_id']

    if flag == 1:
        body_id = req_data['body_id']
        if body_id == None:
            selecting_faces = face_mixing_img[user_id]['faces']
            print("Body_id is none")
        else:
            face_mixing_img[user_id] = {}
            # body_x, body_y, body_w, body_h, body_face, resized_body
            print("Body_id is not none")
            body_decode = body_mixing_img[user_id][body_id]
            body = base64ToImage(body_decode)
            body_image = pilImageToCv2Image(body)
            fixed_body[user_id] = image_divide(body_image)
            body_face = fixed_body[user_id][4]

            for i in range(5):
                print("Generate face "+str(i))
                style, face = face_gen()
                face = np.transpose(np.uint8(face.numpy()*255), (1, 2, 0))
                style_v[i] = style.tolist()
                result_img = face_swap(body_face, face)
                _, b = cv2.imencode('.jpg', result_img)
                t = image4ToBase64(b)  # base64.b64encode(b)
                selecting_faces[i] = t

            print("Generate face finish")

            face_mixing_img[user_id]['style_vector'] = style_v
            face_mixing_img[user_id]['faces'] = selecting_faces

    else:
        selecting_faces = face_mixing_img[user_id]['faces']

    return json.dumps(selecting_faces)


@ app.route("/selectFaceSecond", methods=['GET', 'POST'])
def selectFaceSecond():

    selecting_bodys = {}

    for i in range(5):
        body_address = "./data/test/cloth/000048_1.jpg"
        with open(body_address, 'rb') as imageFile:
            a = base64.b64encode(imageFile.read()).decode('utf8')
        # body = cv2.imread(body_address)
        selecting_bodys[i] = a
    return json.dumps(selecting_bodys)

    global face_mixing_img
    global fixed_body

    selecting_faces = {}
    style_v = {}

    req_data = request.json
    flag = req_data['flag']
    user_id = req_data['user_id']
    if flag == 1:
        face_id = req_data['face_id']
        if face_id == None:
            selecting_faces = face_mixing_img[user_id]['second_faces']
        else:
            face_style = face_mixing_img[user_id]['style_vector'][face_id]
            body_face = fixed_body[user_id][4]

            for i in range(5):
                print("Generate2 face "+str(i))
                new_style, _ = face_gen()
                style_v[i] = new_style.tolist()
                result = style_mixing(face_style, new_style)
                result = np.transpose(np.uint8(result.numpy()*255), (1, 2, 0))
                result = face_swap(body_face, result)
                _, b = cv2.imencode('.jpg', result)
                t = image4ToBase64(b)
                selecting_faces[i] = t

    else:
        selecting_faces = face_mixing_img[user_id]['second_faces']

    print("Generate face finish")

    face_mixing_img[user_id]['second_faces'] = selecting_faces

    return json.dumps(selecting_faces)


@ app.route("/selectModel", methods=['GET', 'POST'])
def selectModel():

    global face_mixing_img
    global fixed_body, model

    req_data = request.json
    user_id = req_data['user_id']
    face_id = req_data['face_id']
    body_id = req_data['body_id']
    merge_face(user_id, body_id)
    result_face = face_mixing_img[user_id]['second_faces'][face_id]
    result_face = base64ToImage(result_face)
    result_face = pilImageToCv2Image(result_face)

    body_img = fixed_body[user_id]
    body_img = base64ToImage(body_img)
    body_img = pilImageToCv2Image(body_img)

    result_img = image_merge_process(body_img, result_face)
    _, b = cv2.imencode('.jpg', result_img)
    t = image4ToBase64(b)
    model[user_id] = t
    return json.dumps(t)


@ app.route("/addLookBook", methods=['GET', 'POST'])
def addLookBook():
    global model
    req_data = request.json
    user_id = req_data['user_id']
    last_model_id = db.child("last_model_id").get().val()
    if last_model_id == None:
        last_model_id = 0

    storage.child("model"+str(last_model_id)).put(model[user_id])
    db.child(user_id).child('lookbook').push("model"+str(last_model_id))

    last_model_id = last_model_id + 1
    db.child("last_model_id").set(last_model_id)


@ app.route("/getLookbook", methods=['GET', 'POST'])
def getLookbook():

    selecting_bodys = {}

    for i in range(5):
        body_address = "./data/test/cloth/000048_1.jpg"
        with open(body_address, 'rb') as imageFile:
            a = base64.b64encode(imageFile.read()).decode('utf8')
        # body = cv2.imread(body_address)
        selecting_bodys[i] = a

    return json.dumps(selecting_bodys)

    cnt = 0
    lookbook = {}
    lookbook_ids = db.child("lookbook").get()
    if lookbook_ids.val() is not None:
        for lookbook_id in lookbook_ids.each():
            url = storage.child(lookbook_id.val()).get_url(1)
            response = urllib.request.urlopen(url).read()
            lookbook[cnt] = base64.b64encode(response).decode('utf8')
            cnt += 1

    return json.dumps(lookbook)


@ app.route("/startUpload", methods=['GET', 'POST'])
def startUpload():
    global cloth_img

    req_data = request.json
    print(req_data)
    user_id = req_data['user_id']
    cloth = {}
    if 'flag' in req_data is True:
        flag = req_data['flag']
        if flag == 0:
            if cloth_img[user_id] is not None:
                cloth.append(cloth_img[user_id])

    return json.dumps(cloth)


'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_id
    user_id = 1


@app.route("/settings")
def settings():
    pass


@app.route("/logout")
def logout():
    global user_id
    user_id = 0
#    logout_user()


@app.route("/refreshFace", methods=['GET', 'POST'])
def refreshFace(n=5):
    newFace = refresh_image(1)
    addFace(newFace)
    style_vector = []
    for i in range(n):
        style_v, img = face_gen()
        style_vector.append(style_v.tolist())

    return style_vector


@app.route("/myPage", methods=['GET', 'POST'])
def myPage():
    mypage = {}
    name = db.child(user_id).get()['name']
    logo_url = db.child(user_id).get()['logo_url']
    lookbook = db.child(user_id).get()['lookbook']
    mypage['name'] = name
    mypage['logo_url'] = logo_url
    mypage['lookbook'] = lookbook
    return json.dumps(mypage)
#    name = current_user.name
#    logo = storage.child(current_user.logo_url).get_url("hello.png")


def body_init():
    global bodys
    if len(bodys) == 0:
        bodys_name = db.child("bodys").get()["data"]
        for i in range(bodys_name):
            bodys.append(storage.child('bodys').download(bodys_name[i]))

    return json.dumps(lookbook)


@app.route("/getModel/<filename>", methods=['GET', 'POST'])
def getModel(filename=None):
    model_id = filename.strip('"')
    model = storage.child(user_id).child('lookbook').get_url(model_id)
    return model


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_id
    user_id = 1


@app.route("/settings")
def settings():
    pass


@app.route("/logout")
def logout():
    global user_id
    user_id = 0
#    logout_user()


@app.route("/selectFace", methods=['GET', 'POST'])
def selectFace(n):
    faces = db.child("faces").order_by_child("id").get()['faces']
    selecting_faces = []

    rand_num = np.random.randint(n, faces.size)
    for i in rand_num:
        face = storage.child(faces).get_url(faces[i].url)
        selecting_faces.append(face)
    return json.dumps(selecting_faces)

'''
if __name__ == '__main__':
    #    app.run(host='127.0.0.1', port=8888)

    app.before_first_request(body_init)
    app.run(host="0.0.0.0", port=8888, debug=True)
# -> main.html
