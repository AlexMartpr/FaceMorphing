import argparse

import cv2
import numpy as np

import tools.Delaunay.correct_delaunay as delaunay
import tools.detect_face_points.magic as util


def read_images(img1, img2):
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img2)
    return [image1, image2]


if __name__ == '__main__':
    parser_arg = argparse.ArgumentParser(prog="face-morphing",
                                         description="The program is providing morphing 2 faces")
    parser_arg.add_argument("-img1", "-i1", default="Input/img_2.jpg")
    parser_arg.add_argument("-img2", "-i2", default="Input/img_1.png")
    parser_arg.add_argument("-duration", "-d", type=int, default=5)
    parser_arg.add_argument("-frames", "-f", type=int, default=20)
    parser_arg.add_argument("-showdt", '-sdt', type=bool, default=False)
    parser_arg.add_argument("-output", default="Output")
    args = vars(parser_arg.parse_args())

    # alpha = 0.5
    # beta = (1.0 - alpha)
    # dst = cv2.addWeighted(src1, alpha, src2, beta, 0.0)
    #
    # cv2.imshow('dst', dst)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    images = read_images(args["img1"], args["img2"])
    points = util.get_face_points(images)
    new_points = np.asarray(points, dtype=np.float64)
    height = images[0].shape[0]
    for i in range(len(new_points)):
        new_points[i][1] = height - new_points[i][1]
        # new_points.append(delaunay.Vector(float(p[0]), float(height - p[1])))
    # new_points = sorted(new_points)
    # new_points = points
    with open('landmarks_points.txt', 'w') as file:
        for p in new_points:
            file.write(f"x : {p[0]} y : {p[1]} \n")
            # file.write(str(p) + "\n")
    # exit(-1)
    # loop over the (x, y)-coordinates for the facial landmarks
    # and draw them on the image
    # for (x, y) in points:
    #     cv2.circle(images[0], (int(x), int(y)), 2, (0, 255, 0), 1)

    # show the output image with the face detections + facial landmarks
    # while True:
    #     cv2.imshow("Output", images[0])
    #     k = cv2.waitKey(5) & 0xFF
    #     if k == 27:
    #         cv2.destroyAllWindows()
    #         exit(-1)
    # new_points = []
    # new_points.append(delaunay.Vector(1, 1))
    # new_points.append(delaunay.Vector(1, 5))
    # new_points.append(delaunay.Vector(1, 7))
    # new_points.append(delaunay.Vector(2, 6))
    # delaun = delaunay.DelaunayTriangulation(new_points)
    delaun = delaunay.delaunay(new_points)
    i = 0
    triangles = []
    for e in delaun:
        # if i == 6:
        #     break
        i += 1
        cv2.line(images[0], (int(e.org[0]), int(height - e.org[1])), (int(e.dest[0]), int(height - e.dest[1])), (0, 255, 0), 1)
        # cv2.circle(images[0], (int(x), int(y)), 2, (0, 255, 0), 1)

    # show the output image with the face detections + facial landmarks
    while True:
        cv2.imshow("Output", images[0])
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            exit(-1)
    # delaun.do_triangulation()
    print("Success")
