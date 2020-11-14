import pyrebase
from flask import Flask
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import json
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
bodys = []
face_mixing_img = {}
fixed_body = {}


@app.route("/", methods=['GET', 'POST'])
def body_init():
    global bodys
    if len(bodys) == 0:
        bodys_name = db.child("bodys").get()["data"]
        for i in range(bodys_name):
            bodys.append(storage.child('bodys').download(bodys_name[i]))


@app.route("/addBody", methods=['GET', 'POST'])
def addBody():
    last_body_id = db.child("last_body_id").get().val()
    if last_body_id == None:
        last_body_id = 0

    for i in range(10):
        body_address = "./data/test/cloth/000048_1.jpg"
        body = Image.open(body_address)
        #body = cv2.imread("./data/body/body"+str(i+1)+".jpg")
        storage.child("body"+str(last_body_id)).put(body)
        # storage.child("body"+str(last_body_id)).put(Image.fromarray(body))
        db.child('bodys').push("body"+str(last_body_id))
        last_body_id = last_body_id + 1

    db.child("last_body_id").set(last_body_id)


@app.route("/selectBody", methods=['GET', 'POST'])
def selectBody():
    global cloth_img, body_mixing_img, bodys

    selecting_bodys = {}

    # test
    for i in range(5):
        body_address = "./data/test/cloth/000048_1.jpg"
        body = Image.open(body_address)
        selecting_bodys[i] = body

    # real
    '''
    flag = request.form.get('flag')
    user_id = request.form.get('user_id')
    if flag == True:
        cloth = request.file.get('cloth')
        if cloth == None:
            selecting_bodys = face_mixing_img[user_id]
            pass
        else:
            cloth_img[user_id] = cloth
            get_mask(cloth)

            # body mixing
            rand_num = np.random.randint(5, bodys.size)
            for i in range(5):
                body = bodys[rand_num[i]]

                # GMM test
                data_list = [body, cloth]
                viton('GMM', data_list)

                # TOM test
                viton('TOM', data_list)

                # result_img
                selecting_bodys[i] = body

    else:
        selecting_bodys = body_mixing_img[user_id]

    '''
    body_mixing_img[user_id] = selecting_bodys

    return json.dumps(selecting_bodys)


@app.route("/selectFaceFirst", methods=['GET', 'POST'])
def selectFaceFirst():

    global body_mixing_img, face_mixing_img
    global fixed_body

    selecting_faces = {}
    style_v = {}

    flag = request.form.get('flag')
    user_id = request.form.get('user_id')
    if flag == True:
        body_id = request.form.get('body_id')
        if body_id == None:
            selecting_faces = face_mixing_img[user_id]['faces']
        else:
            # body_x, body_y, body_w, body_h, body_face, resized_body
            body = body_mixing_img[user_id][body_id]
            fixed_body[user_id] = image_divide(body)
            body_face = fixed_body[user_id][4]

            for i in range(5):
                style, face = face_gen()
                style_v[i] = style.tolist()
                selecting_faces[i] = face_swap(body_face, face)

            face_mixing_img[user_id]['style_vector'] = style_v
            face_mixing_img[user_id]['faces'] = selecting_faces

    return json.dumps(selecting_faces)


@app.route("/selectFaceSecond", methods=['GET', 'POST'])
def selectFaceSecond():

    global face_mixing_img

    selecting_faces = {}
    style_v = {}

    flag = request.form.get('flag')
    user_id = request.form.get('user_id')
    if flag == True:
        face_id = request.form.get('face_id')
        if face_id == None:
            selecting_faces = face_mixing_img[user_id]['second_faces']
        else:
            face_style = face_mixing_img[user_id]['style_vector'][face_id]

            for i in range(5):
                new_style, _ = face_gen()
                style_v[i] = new_style.tolist()
                selecting_faces[i] = style_mixing(face_style, new_style)

            face_mixing_img[user_id]['second_faces'] = selecting_faces

    return json.dumps(selecting_faces)


@app.route("/selectModel", methods=['GET', 'POST'])
def selectModel():

    global face_mixing_img
    global fixed_body

    user_id = request.form.get('user_id')
    face_id = request.form.get('face_id')
    result_face = face_mixing_img[user_id]['second_faces'][face_id]

    model = image_merge_process(fixed_body[user_id], result_face)

    return json.dumps(model)


@app.route("/addLookBook", methods=['GET', 'POST'])
def addLookBook():
    user_id = request.form.get('user_id')
    last_model_id = db.child("last_model_id").get().val()
    if last_model_id == None:
        last_model_id = 0

    model = request.file.get('model')
    storage.child("model"+str(last_model_id)).put(model)

    db.child(user_id).child('lookbook').push("model"+str(last_model_id))

    last_model_id = last_model_id + 1
    db.child("last_model_id").set(last_model_id)


@app.route("/getLookbook", methods=['GET', 'POST'])
def getLookbook(user):

    user_id = request.form.get('user_id')
    lookbook_ids = db.child(user_id).child('lookbook').get()

    lookbook = {}
    if lookbook_ids.each() == None:
        return json.dumps('')
    else:
        for i in range(lookbook_ids):
            model = storage.child(lookbook_ids[i]).get_url()
            lookbook[i] = model

    return json.dumps(lookbook)


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
    app.run(host="0.0.0.0", port=8888, debug=True)
    body_init()
# -> main.html
