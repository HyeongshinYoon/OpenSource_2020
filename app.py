import pyrebase
from flask import Flask
from numpy import np
#from flask_login import LoginManager, current_user


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
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
# login = LoginManager(app)
user_id = 0


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


@app.route("/selectBody", methods=['GET', 'POST'])
def selectBody(n):
    bodys = db.child("bodys").order_by_child("id").get()['bodys']
    selecting_bodys = []

    rand_num = np.random.randint(n, bodys.size)
    for i in rand_num:
        body = storage.child(bodys).get_url(bodys[i].url)
        selecting_bodys.append(body)
    return json.dumps(selecting_bodys)


@app.route("/addFace", methods=['GET', 'POST'])
def addFace():
    if request.method == 'POST':
        last_face_id = db.child("last_face_id").get().val()
        if last_face_id == None:
            last_face_id = 0

        face = request.files.get('face')
        files = []

        storage.child(last_face_id).put(face)
        files.append(last_face_id)

        data = [{"id": last_face_id, "child": 'false', "child_num": []}]
        db.child('faces').child(last_face_id).push(data)

        last_face_id = last_face_id + 1
        db.child("last_face_id").set(last_face_id)


@app.route("/addBody", methods=['GET', 'POST'])
def addBody():
    if request.method == 'POST':
        last_body_id = db.child("last_body_id").get().val()
        if last_body_id == None:
            last_body_id = 0

        body = request.files.get('body')
        files = []

        storage.child(last_body_id).put(body)
        files.append(last_body_id)

        data = [{"id": last_body_id, "child": 'false', "child_num": []}]
        db.child('bodys').child(last_body_id).push(data)

        last_body_id = last_body_id + 1
        db.child("last_body_id").set(last_body_id)


@app.route("/addNewModel", methods=['GET', 'POST'])
def addNewModel():
    if request.method == 'POST':
        last_model_id = db.child("last_model_id").get().val()
        if last_model_id == None:
            last_model_id = 0

        model = request.files.get('model')
        files = []

        storage.child(last_model_id).put(model)
        files.append(last_model_id)

        data = [{"id": last_model_id}]
        db.child(user_id).child('lookbook').child(last_model_id).push(data)

        last_model_id = last_model_id + 1
        db.child("last_model_id").set(last_model_id)


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


@app.route("/getLookbook", methods=['GET', 'POST'])
def getLookbook(user):
    Lookbook_id = db.child(user).child("lookbook_id").get().val()
    lookbook = {}
    if Lookbook_id.each() == None:
        return json.dumps('')
    else:
        model = storage.child('LookBook').child(Lookbook_id).get()
        for id in Lookbook_id.each():
            lookbook[id.val()] = (model.val())

    return json.dumps(lookbook)


@app.route("/getModel/<filename>", methods=['GET', 'POST'])
def getModel(filename=None):
    model_id = filename.strip('"')
    model = storage.child(user_id).child('lookbook').get_url(model_id)
    return model


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
# -> main.html
