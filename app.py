import pyrebase
from flask import Flask
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
    user_id = 0
#    logout_user()

# random 5


@app.route("/selectBody", methods=['GET', 'POST'])
def selectBody():
    bodys = db.child("bodys").get()
    return json.dumps(bodys)


@app.route("/selectFace", methods=['GET', 'POST'])
def selectFace():
    bodys = db.child("faces").get()
    return json.dumps(bodys)


@app.route("/addFace", methods=['GET', 'POST'])
def addFace():
    if request.method == 'POST':
        last_face_id = db.child("last_face_id").get().val()
        if last_face_id == None:
            last_face_id = 0

        title = request.form['title']
        face = request.files.get('face')
        files = []

        storage.child(last_face_id).put(face)
        files.append(last_face_id)

        data = [{"title": title, "files": files}]
        db.child('faces').child(last_face_id).push(data)

        last_face_id = last_face_id + 1
        db.child("last_face_id").set(last_face_id)


@app.route("/addBody", methods=['GET', 'POST'])
def addBody():
    if request.method == 'POST':
        last_body_id = db.child("last_body_id").get().val()
        if last_body_id == None:
            last_body_id = 0

        title = request.form['title']
        body = request.files.get('body')
        files = []

        storage.child(last_body_id).put(body)
        files.append(last_body_id)

        data = [{"title": title, "files": files}]
        db.child('bodys').child(last_body_id).push(data)

        last_body_id = last_body_id + 1
        db.child("last_body_id").set(last_body_id)


@app.route("/addNewModel", methods=['GET', 'POST'])
def addNewModel():
    if request.method == 'POST':
        last_model_id = db.child("last_model_id").get().val()
        if last_model_id == None:
            last_model_id = 0

        title = request.form['title']
        model = request.files.get('model')
        files = []

        storage.child(last_model_id).put(model)
        files.append(last_model_id)

        data = [{"title": title, "files": files}]
        db.child('models').child(last_model_id).push(data)

        last_model_id = last_model_id + 1
        db.child("last_model_id").set(last_model_id)


@app.route("/myPage", methods=['GET', 'POST'])
def myPage():
    name = current_user.name
    logo = storage.child(current_user.logo_url).get_url("hello.png")


@app.route("/getLookbook/<user>", methods=['GET', 'POST'])
def getLookbook(user):
    Lookbook_id = db.child(user).child("LookbookId").get()
    lookbook = {}
    if Lookbook_id.each() == None:
        return json.dumps('')
    else:
        model = storage.child('LookBook').child(Lookbook_id).get()
        for id in Lookbook_id.each():
            lookbook[id.val()] = (model.val())

    return json.dumps(lookbook)


@app.route("/getModel/<filename>", methods=['GET', 'POST'])
def getPhoto(filename=None):
    text = filename.strip('"')
    photo = storage.child('model').get_url("hello.png")
    return photo


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        global last_post_id
        last_post_id = db.child("last_post_id").get().val()
        if last_post_id == None:
            last_post_id = 0

        title = request.form['title']
        subtitle = request.form['subtitle']
        tag = request.form.getlist('tag')
        photos = request.files.getlist('photos')
        files = []

        for photo in photos:
            storage.child(photo.filename).put(photo)
            files.append(photo.filename)

        data = [{"title": title, "subtitle": subtitle, "tag": tag, "files": files}]
        db.child('posts').child(last_post_id).push(data)

        for tag_id in tag:
            db.child("tag").child(tag_id).push(last_post_id)
        last_post_id = last_post_id + 1
        db.child("last_post_id").set(last_post_id)
    return render_template('Upload.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
# -> main.html
