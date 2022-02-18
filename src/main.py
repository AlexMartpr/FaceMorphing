import cv2
import argparse

import tools.magic as util


def read_images(img1, img2):
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img2)
    return [image1, image2]


if __name__ == '__main__':
    parser_arg = argparse.ArgumentParser(prog="face-morphing",
                                         description="The program is providing morphing 2 faces")
    parser_arg.add_argument("-img1", "-i1", required=True, default="Input/test_image1.jpeg")
    parser_arg.add_argument("-img2", "-i2", required=True, default="Input/test_image2.jpeg")
    parser_arg.add_argument("-duration", "-d", type=int, default=5)
    parser_arg.add_argument("-frames", "-f", type=int, default=20)
    parser_arg.add_argument("-showdt", '-sdt', type=bool, default=False)
    parser_arg.add_argument("-output", default="Output")
    args = vars(parser_arg.parse_args())

    images = read_images(args["img1"], args["img2"])
    util.get_face_points(images)
