#! /usr/bin/env python
"""
Using the provided functions in dlib to detect the points of facial landmarks in an image
"""
import numpy as np
import cv2
import dlib

# Pre-trained shape predictor from iBUG 300-W dataset
SHAPE_PREDICTOR = 'data/shape_predictor_68_face_landmarks.dat'

frontal_face_detector = dlib.get_frontal_face_detector()
landmarks_predictor = dlib.shape_predictor(SHAPE_PREDICTOR)


# another conversion from imutils
def landmarks_to_numpy(landmarks):
    # initialize the matrix of (x, y)-coordinates with a row for each landmark
    coords = np.zeros((landmarks.num_parts, 2), dtype=int)

    # convert each landmark to (x, y)
    for i in range(0, landmarks.num_parts):
        coords[i] = (landmarks.part(i).x, landmarks.part(i).y)

    # return the array of (x, y)-coordinates
    return coords


def detect_landmarks(img):
    # this list will contain the facial landmark points for each face detected
    points = []
    # second argument of 1 indicates the image will be upscaled once, upscaling creates a bigger image so it is easier
    # to detect the faces, can increase this number if there are troubles detecting faces
    # returns a bounding box around each face
    detected_faces = frontal_face_detector(img, 1)

    # now that we have the boxes containing the faces find the landmarks inside them
    for face in detected_faces:
        # use dlib to find the expected facial landmarks in the boxes around the detected faces
        landmarks = landmarks_predictor(img, face)
        # add the facial landmarks in a form we can use later without dlib
        points.append(landmarks_to_numpy(landmarks))

    return points
