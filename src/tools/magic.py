import cv2
import dlib
import numpy as np
from errors.errors import NoFaceFoundError

PATH_DATASET = "src/tools/dataset/shape_predictor_68_face_landmarks.dat"


def generate_face_corresponding_points(images):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PATH_DATASET)

    corresponding_points = np.zeros((68, 2))

    list1, list2 = [], []

    for i in range(images):
        img = images[i]
        size = [img.shape[0], img.shape[0]]
        current_img = img

        faces = detector(img, 1)

        if len(faces) == 0:
            raise NoFaceFoundError

        for k, rect in enumerate(faces):
            shape = predictor()