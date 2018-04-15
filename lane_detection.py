#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
https://zhuanlan.zhihu.com/p/25354571?group_id=820292423715545088
'''

import cv2
import numpy as np
import os

rho = 1
theta = np.pi / 180
threshold = 15
min_line_length = 40
max_line_gap = 20


def show(image):
    cv2.namedWindow('img', cv2.WINDOW_KEEPRATIO)
    cv2.imshow("img", image)
    cv2.waitKey(0)


def roi_mask(img, vertices):
    mask = np.zeros_like(img)
    mask_color = 255
    cv2.fillPoly(mask, vertices, mask_color)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold,
                min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                            minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


if not os.path.exists('output'):
    os.makedirs('output')
for num in range(1, 100):
    file_name = "%s.jpg" % num
    img = cv2.imread('dataset/' + file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # show(gray)
    blur_ksize = 5  # Gaussian blur kernel size
    blur_gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0, 0)
    # show(blur_gray)

    canny_lthreshold = 50  # Canny edge detection low threshold
    canny_hthreshold = 150  # Canny edge detection high threshold
    edges = cv2.Canny(blur_gray, canny_lthreshold, canny_hthreshold)
    # show(edges)
    x = cv2.line(edges, (0, 240), (460, 325), (255, 0, 0), 5)
    y = cv2.line(x, (520, 325), (320, 240), (255, 0, 0), 5)
    roi_vtx = np.array([[(0, img.shape[0]), (100, 100),
                         (img.shape[1], 100), (img.shape[1], img.shape[0])]])
    # show(y)
    roi_edges = roi_mask(edges, roi_vtx)
    # show(roi_edges)
    try:
        line_img = hough_lines(roi_edges, rho, theta, threshold,
                               min_line_length, max_line_gap)
        # show(line_img)
        last = cv2.addWeighted(img, 0.8, line_img, 1, 0)
        # show(last)
        cv2.imwrite('output/' + file_name, last)
    except TypeError:
        cv2.imwrite('output/' + file_name, roi_edges)
        pass
