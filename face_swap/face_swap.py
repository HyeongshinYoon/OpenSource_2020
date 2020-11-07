#! /usr/bin/env python
"""
Run all the separate components of face swapping in an easily understandable high-level runner class
reference: https://github.com/BruceMacD/Face-Swap-OpenCV
"""

import cv2
from face_swap.landmark_detection import detect_landmarks
from face_swap.convex_hull import find_convex_hull
from face_swap.delaunay_triangulation import find_delauney_triangulation
from face_swap.affine_transformation import apply_affine_transformation
from face_swap.clone_mask import merge_mask_with_image

EXPECTED_NUM_IN = 2


def face_swap(img_2, img_1):

    # find the facial landmarks which return the key points of the face
    # localizes and labels areas such as eyebrows and nose
    # we are using the first face found no matter what in this case, could be expanded for multiple faces here
    landmarks_1 = detect_landmarks(img_1)[0]
    landmarks_2 = detect_landmarks(img_2)[0]

    # create a convex hull around the points, this will be like a mask for transferring the points
    # essentially this circles the face, swapping a convex hull looks more natural than a bounding box
    # we need to pass both sets of landmarks here because we map the convex hull from one face to another
    hull_1, hull_2 = find_convex_hull(landmarks_1, landmarks_2, img_1, img_2)

    # divide the boundary of the face into triangular sections to morph
    delauney_1 = find_delauney_triangulation(img_1, hull_1)

    # warp the source triangles onto the target face
    img_1_face_to_img_2 = apply_affine_transformation(
        delauney_1, hull_1, hull_2, img_1, img_2)

    swap_1 = merge_mask_with_image(hull_2, img_1_face_to_img_2, img_2)

    return swap_1
