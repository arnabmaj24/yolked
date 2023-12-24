import numpy as np
import math

def angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle

def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def cosine(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    vect1 = [c[0] - b[0], c[1] - b[1]]
    vect1 = np.array(vect1)

    vect2 = [a[0] - b[0],a[1] - b[1]]
    vect2 = np.array(vect2)

    rads = np.arccos((vect1.dot(vect2))/(magnitude(vect1)*magnitude(vect2)))

    angle = np.abs(rads * 180 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle