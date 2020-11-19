import cv2
import shutil
from os import listdir
from os.path import isfile, join


def image_divide():

    face_cascade = cv2.CascadeClassifier('../xml/haarcascade_frontface.xml')

    # 3, 12, 14, 25, 111, 189, 206, 234, 254, 268, 289, 467, 528, 661, 1040, 1074, 1246, 1312, 1523, 1556, 1560, 1696, 1783
    # body_address = ["000003_0", "000012_0", "000014_0", "000025_0", "000111_0", "000189_0", "000206_0", "000234_0", "000254_0", "000268_0", "000289_0",
    #                 "000467_0", "000528_0", "000661_0", "001040_0", "001074_0", "001246_0", "001312_0", "001523_0", "001556_0", "001560_0", "001696_0", "001783_0"]
    body_address = [f for f in listdir("../image/image/")]
    # print(body_address)
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
