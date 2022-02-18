import cv2
import dlib
import numpy as np
from errors.errors import NoFaceFoundError

PATH_DATASET = "src/tools/dataset/shape_predictor_68_face_landmarks.dat"


def get_face_points(images):
    detector = dlib.get_frontal_face_detector()
    landmarks_points_predictor = dlib.shape_predictor(PATH_DATASET)

    face_points = np.zeros((68, 2))

    list1, list2 = [], []

    index_image = 0
    size = []
    for img in images:
        size = [img.shape[0], img.shape[0]]
        faces = detector(img, 1)

        # Return error if no faces were found
        if len(faces) == 0:
            raise NoFaceFoundError

        if index_image == 0:
            current_list = list1
        else:
            current_list = list2

        for k, rect in enumerate(faces):
            shape = landmarks_points_predictor(img, rect)
            for i in range(0, 68):
                [x, y] = shape.part(i).x, shape.part(i).y
                current_list.append((x, y))
                # Fill coordinates of features of face
                face_points[i][0] += x
                face_points[i][1] += y

            current_list.append((1, 1))
            current_list.append((size[1] - 1, 1))
            current_list.append(((size[1] - 1) // 2, 1))
            current_list.append((1, size[0] - 1))
            current_list.append((1, (size[0] - 1) // 2))
            current_list.append(((size[1] - 1) // 2, size[0] - 1))
            current_list.append((size[1] - 1, size[0] - 1))
            current_list.append(((size[1] - 1), (size[0] - 1) // 2))

        index_image += 1

    arr = face_points / 2
    arr = np.append(arr, [[1, 1]], axis=0)
    arr = np.append(arr, [[size[1] - 1, 1]], axis=0)
    arr = np.append(arr, [[(size[1] - 1) // 2, 1]], axis=0)
    arr = np.append(arr, [[1, size[0] - 1]], axis=0)
    arr = np.append(arr, [[1, (size[0] - 1) // 2]], axis=0)
    arr = np.append(arr, [[(size[1] - 1) // 2, size[0] - 1]], axis=0)
    arr = np.append(arr, [[size[1] - 1, size[0] - 1]], axis=0)
    arr = np.append(arr, [[(size[1] - 1), (size[0] - 1) // 2]], axis=0)
