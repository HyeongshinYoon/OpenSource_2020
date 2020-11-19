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
import imageio
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
    body_address = ["000003_0", "000012_0", "000014_0", "000025_0", "000111_0", "000189_0", "000206_0", "000234_0", "000254_0", "000268_0", "000289_0",
                    "000467_0", "000528_0", "000661_0", "001040_0", "001074_0", "001246_0", "001312_0", "001523_0", "001556_0", "001560_0", "001696_0", "001783_0"]
    for i in range(len(body_address)):
        address = "./data/test/image/"+str(body_address[i])+".jpg"
        with open(address, 'rb') as imageFile:
            a = imageFile.read()
        storage.child(body_address[i]+".jpg").put(a)
        db.child('bodys').push(body_address[i]+".jpg")
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


def stringToRGB(base64_string, name, cloth):
    if cloth == True:
        base64_string = base64_string.split(",")[1]
        base64_string += "=" * ((4 - len(base64_string) % 4) % 4)
    imgdata = base64.b64decode(str(base64_string))
    with io.BytesIO(imgdata) as fh:
        image = Image.open(fh)
        image.save(name)

    return image


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

        cloth = req_data['cloth']
        cloth_name = "cloth" + str(user_id) + ".jpg"
        if cloth == None:
            selecting_bodys = body_mixing_img[user_id]
            body_names = bodys[user_id]
        else:
            cloth = stringToRGB(cloth,
                                './data/test/cloth/'+cloth_name, True)
            cloth_img[user_id] = cloth

            # body mixing
            rand_num = []
            # rand_num = np.random.randint(len(bodys), size=len(bodys))
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
    global body_name, body_mixing_img, fixed_body
    cloth_name = "cloth" + str(user_id) + ".jpg"

    body_names = body_name[user_id][body_id]
    get_mask(cloth_name)

    # GMM test
    data_list = [body_names, cloth_name]
    viton('GMM', data_list)

    # TOM test
    viton('TOM', data_list)

    body_address = "./data/result/"+body_names
    fixed_body[user_id] = {}
    fixed_body[user_id]['body_address'] = "./data/result/"+body_names
    a = cv2.imread(body_address)
    return a


@ app.route("/selectFaceFirst", methods=['GET', 'POST'])
def selectFaceFirst():
    global body_mixing_img, face_mixing_img, body_name
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
         #           print(str(body_mixing_img[user_id][req_data['body_id']]))
            body_img = base64.b64decode(
                str(body_mixing_img[user_id][req_data['body_id']]))
            name = './data/test/image/' + body_name[user_id][body_id]
            with io.BytesIO(body_img) as fh:
                image = Image.open(fh)
                image.save(name)

            face_mixing_img[user_id] = {}
            # body_x, body_y, body_w, body_h, body_face, resized_body
            print("Body_id is not none")
            image = pilImageToCv2Image(image)
            fixed_body[user_id] = image_divide(image)
            body_face = fixed_body[user_id][4]
            for i in range(5):
                print("Generate face "+str(i))
                style, face = face_gen()
                face = np.transpose(np.uint8(face.numpy()*255), (1, 2, 0))
                # face = cv2.resize(face, dsize=(100, 100),
                #                  interpolation=cv2.INTER_CUBIC)
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
    global face_mixing_img
    global fixed_body

    selecting_faces = {}
    selecting_images = {}
    style_v = {}

    req_data = request.json
    flag = req_data['flag']
    user_id = req_data['user_id']
    if flag == 1:
        face_id = req_data['face_id']
        if face_id == None:
            selecting_faces = face_mixing_img[user_id]['second_faces']['json']
            selecting_images = face_mixing_img[user_id]['second_faces']['images']
        else:
            face_mixing_img[user_id]['second_faces'] = {}
            face_style = face_mixing_img[user_id]['style_vector'][face_id]
            body_face = fixed_body[user_id][4]

            for i in range(5):
                print("Generate2 face "+str(i))
                new_style, _ = face_gen()
                style_v[i] = new_style.tolist()
                result = style_mixing(face_style, new_style)
                result = np.transpose(np.uint8(result.numpy()*255), (1, 2, 0))
                result = face_swap(body_face, result)
                selecting_images[i] = result
                _, b = cv2.imencode('.jpg', result)
                t = image4ToBase64(b)
                selecting_faces[i] = t

    else:
        selecting_faces = face_mixing_img[user_id]['second_faces']['json']
        selecting_images = face_mixing_img[user_id]['second_faces']['images']

    print("Generate face finish")

    face_mixing_img[user_id]['second_faces']['json'] = selecting_faces
    face_mixing_img[user_id]['second_faces']['images'] = selecting_images

    return json.dumps(selecting_faces)


@ app.route("/selectModel", methods=['GET', 'POST'])
def selectModel():

    global face_mixing_img
    global fixed_body, model, body_name

    req_data = request.json
    user_id = req_data['user_id']
    face_id = req_data['face_id']
    body_id = req_data['body_id']
    result_face = face_mixing_img[user_id]['second_faces']['images'][face_id]

    body_img = fixed_body[user_id]
    body_img = image_merge_process(body_img, result_face)

    name = './data/test/image/' + body_name[user_id][body_id]
    cv2.imwrite(name, body_img)

    result_img = merge_face(user_id, body_id)
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

    imgdata = base64.b64decode(str(model[user_id]))
    name = fixed_body[user_id]['body_address']
    storage.child("model"+str(last_model_id)).put(name)
    db.child(user_id).child('lookbook').push("model"+str(last_model_id))

    last_model_id = last_model_id + 1
    db.child("last_model_id").set(last_model_id)
    return json.dumps({})


@ app.route("/getLookbook", methods=['GET', 'POST'])
def getLookbook():
    req_data = request.json
    user_id = req_data['user_id']
    lookbook_ids = db.child(user_id).child('lookbook').get()

    cnt = 0
    lookbook = {}
    if lookbook_ids is not None:
        for lookbook_id in lookbook_ids.each():
            url = storage.child(lookbook_id.val()).get_url(1)
            response = urllib.request.urlopen(url).read()
            lookbook[cnt] = base64.b64encode(response).decode('utf8')
            cnt += 1

    return json.dumps(lookbook)


'''
    selecting_bodys = {}

    for i in range(5):
        body_address = "./data/test/cloth/000048_1.jpg"
        with open(body_address, 'rb') as imageFile:
            a = base64.b64encode(imageFile.read()).decode('utf8')
        # body = cv2.imread(body_address)
        selecting_bodys[i] = a

    return json.dumps(selecting_bodys)
'''


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


'''
if __name__ == '__main__':
    #    app.run(host='127.0.0.1', port=8888)

    # app.before_first_request(addBody)
    app.before_first_request(body_init)
    app.run(host="0.0.0.0", port=8888, debug=True)
# -> main.html
