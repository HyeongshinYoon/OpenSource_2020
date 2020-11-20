import cv2
import shutil
from os import listdir
from os.path import isfile, join


def image_divide():

    face_cascade = cv2.CascadeClassifier('../xml/haarcascade_frontface.xml')
    
    body_address = [f for f in listdir("../image/image/")]
    for i in range(len(body_address)):
        address = "../image/image/" + \
            str(body_address[i])
        img = cv2.imread(address)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            resize_img = cv2.resize(
                img, None, fx=256.0/w, fy=256.0/h, interpolation=cv2.INTER_AREA)
            resize_gray = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
            resize_faces = face_cascade.detectMultiScale(resize_gray, 1.3, 5)
            if (len(resize_faces) > 0):
                print(resize_faces[0])
                fromFilePathName = '../image/image/' + \
                    str(body_address[i])
                resultFilePathName = '../data/test2/image/' + \
                    str(body_address[i])
                shutil.move(fromFilePathName, resultFilePathName)

                fromFilePathName = '../image/image-parse/' + \
                    str(body_address[i]).replace('.jpg', '.png')
                resultFilePathName = '../data/test2/image-parse/' + \
                    str(body_address[i]).replace('.jpg', '.png')
                shutil.move(fromFilePathName, resultFilePathName)

                fromFilePathName = '../image/pose/' + \
                    str(body_address[i].replace(
                        '.jpg', '_keypoints.json'))
                resultFilePathName = '../data/test2/pose/' + \
                    str(body_address[i].replace(
                        '.jpg', '_keypoints.json'))
                shutil.move(fromFilePathName, resultFilePathName)


image_divide()
