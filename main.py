import cv2
from face_crop.face_crop import image_divide, image_merge_process
from face_swap.face_swap import face_swap
from face_gen.generate import face_gen
from face_gen.mix import style_mixing


def refresh_image(n):
    style_vector = []
    for i in range(n):
        style = face_gen("new_face"+str(i)).tolist()
        style_vector.append(style)

    return style_vector


def mixing_image(style, n):

    style_vector = refresh_image(n)

    for i in range(n):
        style_mixing(style, style_vector[i], "new_face"+str(i+n))


def main():

    #body_input = int(input())
    #body = "./image/image" + str(body_input) + ".jpg"
    body_address = "./image/image1.jpg"
    body = cv2.imread(body_address)
    body_x, body_y, body_w, body_h, old_face, resized_body = image_divide(body)

    # make and choose new faces
    new_style = refresh_image(5)
    mixing_image(new_style[0], 5)

    # selecting face
    new_face_input = "./new_face4.jpg"
    new_face = cv2.imread(new_face_input)

    # swap origin face to selecting face
    swap_face = face_swap(old_face, new_face)
    cv2.imwrite("swap.jpg", swap_face)

    # merge to body and changed face
    swap_img = image_merge_process(resized_body, swap_face,
                                   body_x, body_y, body_w, body_h)

    # result_img = viton(swap_img)
    cv2.imwrite("result_img.jpg", swap_img)


if __name__ == "__main__":
    main()
