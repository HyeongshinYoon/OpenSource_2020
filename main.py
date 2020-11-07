
import cv2
from face_crop.face_crop import image_divide, image_merge_process
from face_swap.face_swap import face_swap


def main():

    #body_input = int(input())
    #body = "./image/image" + str(body_input) + ".jpg"
    body_address = "./resized_image1.jpg"
    body = cv2.imread(body_address)
    body_x, body_y, body_w, body_h, old_face, resized_body = image_divide(body)

    #new_face_input = int(input())
    new_face_input = "./crop_image5.jpg"
    new_face = cv2.imread(new_face_input)
    swap_face = face_swap(old_face, new_face)
    result_img = image_merge_process(resized_body, swap_face,
                                     body_x, body_y, body_w, body_h)

    cv2.imwrite("result_img.jpg", result_img)


if __name__ == "__main__":
    main()
