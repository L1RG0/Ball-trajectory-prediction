"""
Made by *Lirgo*

This project is devoted to calculating and
predicting the shape of a parabola
based on a video with a thrown ball
"""

import cv2
import numpy as np
import time

points = []

def parabola(point_1, point_2, point_3):

    # we define coordinates to points

    x1, y1 = point_1
    x2, y2 = point_2
    x3, y3 = point_3

    """
    the lines underneath are a result of a 
    calculated parabola function using desmos
    that you can check out in this link:
    
    https://www.desmos.com/calculator/q5khflotcq?lang=en
    """

    b = ((y1 - y2) * (x3 ** 2 - x1 ** 2) + (x1 ** 2 - x2 ** 2) * (y1 - y3)) / ((x3 - x1) * (x3 - x2) * (x1 - x2))
    a = ((y2 - y1) + b * (x1 - x2)) / (x2 ** 2 - x1 ** 2)
    c = y1 - a * x1 ** 2 - b * x1

    return a, b, c

def f(x, factors):
    a, b, c = factors
    return a * x ** 2 + b * x + c

def detect_circles(frame):
    blur = cv2.medianBlur(frame, 7)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([10, 100, 100])
    upper_blue = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # convert image to grayscale image
    gray_image = cv2.cvtColor(cv2.bitwise_and(frame, frame, mask=mask), cv2.COLOR_BGR2GRAY)
    # convert the grayscale image to binary image
    ret, thresh = cv2.threshold(gray_image, 0, 255, 0)
    # calculate moments of binary image
    M = cv2.moments(thresh)
    # calculate x,y coordinate of center
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # put text and highlight the center
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        return cX, cY
    except:
        return None

def main():
    video = cv2.VideoCapture('parabola.mp4')
    while True:
        try:
            _, frame = video.read()
            point = detect_circles(frame)
            if point is not None:
                points.append(point)
            cv2.imshow('frame', frame)
            print(points)
            if cv2.waitKey(0) == 27:
                break
        except cv2.error as e:
            # print(e)
            break

    print('done')


if __name__ == '__main__':
    main()
