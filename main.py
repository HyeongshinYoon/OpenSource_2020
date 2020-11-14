'''
import cv2
from PIL import Image
# from face_crop.face_crop import image_divide, image_merge_process
# from face_swap.face_swap import face_swap
# from face_gen.generate import face_gen
# from face_gen.mix import style_mixing
from cp_viton.get_mask import get_mask
from cp_viton.test import viton

# def refresh_image(n):

#     style_vector = []
#     for i in range(n):
#         style_v, img = face_gen("new_face"+str(i))
#         style = style_v.tolist()
#         style_vector.append(style)

#     return style_vector


# def mixing_image(style, n):

#     style_vector = refresh_image(n)
#     for i in range(n):
#         style_mixing(style, style_vector[i], "new_face"+str(i+n))


def main():

    # # get body and resize body
    # body_address = "./image/image1.jpg"
    # body = cv2.imread(body_address)
    # body_x, body_y, body_w, body_h, old_face, resized_body = image_divide(body)

    # # make and choose new faces
    # new_style = refresh_image(5)
    # mixing_image(new_style[0], 5)

    # # selecting face
    # new_face_input = "./new_face4.jpg"
    # new_face = cv2.imread(new_face_input)

    # # swap origin face to selecting face
    # swap_face = face_swap(old_face, new_face)
    # cv2.imwrite("swap.jpg", swap_face)

    # # merge to body and changed face
    # swap_img = image_merge_process(resized_body, swap_face,
    #                                body_x, body_y, body_w, body_h)

    # get cloth masks and save to ./data/test/cloth-mask/
    img_names = ["000889_0.jpg"]
    cloth_names = ["000048_1.jpg"]
    get_mask(cloth_names)

    # GMM test
    data_list = [img_names, cloth_names]
    viton('GMM', data_list)

    # TOM test
    viton('TOM', data_list)

    # result_img = viton(swap_img)
    cv2.imwrite("result_img.jpg", swap_img)


if __name__ == "__main__":
    main()
'''
