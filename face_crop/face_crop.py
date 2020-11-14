import cv2


def image_divide(img):

    face_cascade = cv2.CascadeClassifier('./xml/haarcascade_frontface.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    (x, y, w, h) = faces[0]
    resize_img = cv2.resize(
        img, None, fx=256.0/w, fy=256.0/h, interpolation=cv2.INTER_AREA)
    resize_gray = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
    resize_faces = face_cascade.detectMultiScale(resize_gray, 1.3, 5)

    (rx, ry, rw, rh) = resize_faces[0]
    y1, y2 = int(ry - int(rh/4)), int(ry + rh + int(rh/4))
    x1, x2 = int(rx - int(rw/4)), int(rx + rw + int(rw/4))

    old_face = resize_img[y1:y2, x1:x2]
    cv2.imwrite('old_face.jpg', old_face)
    cv2.imwrite('resize_image.jpg', resize_img)

    return [rx, ry, rw, rh, old_face, resize_img]


def image_merge_process(fixed_body, face):
    x, y, w, h, _, body = fixed_body

    y1, y2 = int(y - int(h/4)), int(y + h + int(h/4))
    x1, x2 = int(x - int(w/4)), int(x + w + int(w/4))
    resized_face = cv2.resize(face,
                              (y2-y1, x2-x1), interpolation=cv2.INTER_CUBIC)

    # If you want to use only changed image using GAN, you use next line only.
    body[y1:y2, x1:x2] = resized_face

    # Mixing background and GAN image.
#    alpha_s = 0.5
#    alpha_l = 1.0 - alpha_s
#    for color in range(0, 3):
#        img[y1:y2, x1:x2, color] = (alpha_s * gan_img[:, :, color] +
#                                    alpha_l * img[y1:y2, x1:x2, color])

    # Save mixing image.
#    resize_img = cv2.resize(
#        img, (w, h), interpolation=cv2.INTER_CUBIC + cv2.INTER_LINEAR)
#    cv2.imwrite("merge_image{}.jpg".format(num), resize_img)

    return body
