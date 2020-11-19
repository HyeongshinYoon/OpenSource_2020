#! /usr/bin/env python
"""
A convex hull is a tight fitting boundary around points
We will we use a convex hull to find the boundary of a face given its points (obtained from openCV)
This can be made more efficient by doing multiple hulls in one iteration
Keeping simple for clarity
"""

import numpy as np
import cv2

def find_convex_hull(points_1, points_2, img_1, img_2):
    hull_1 = []
    hull_2 = []

    # this is the area that we will be mapping between faces
    hull_index_to_map = cv2.convexHull(np.array(points_1), returnPoints=False)

    # find the facial landmark points on both faces that are within the hull of the face we are basing our map off of
    for i in range(0, len(hull_index_to_map)):
        hull_1.append(points_1[int(hull_index_to_map[i])])
        hull_2.append(points_2[int(hull_index_to_map[i])])

    return hull_1, hull_2
