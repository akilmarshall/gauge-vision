import numpy as np
import cv2 as cv
from functools import wraps
from time import time

from math import cos, sin, pi
from PIL import Image


def timing(f):
    """Decorator method for timing function execution. """
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print(f'elapsed time: {end - start}')
        return result
    return wrapper

def crop(img: np.ndarray, xy, size):
    x, y = xy
    width, height = size
    w = width // 2
    h = height // 2
    image = Image.fromarray(img)
    return np.array(image.crop((x - w, y - h, x + w, y + h)))

def gaussian_blur(img: np.ndarray, kernel=(5, 5), sigma=0) -> np.ndarray:
    return cv.GaussianBlur(img, kernel, sigma) 

def bilateral_filter(img: np.ndarray) -> np.ndarray:
    return cv.bilateralFilter(img, 9, 75, 75)


def CHT(img: np.ndarray, method: int=cv.HOUGH_GRADIENT, dp: float=1, minDist: float=50, p1: float=300, p2: float=150):
    """
    Circle Hough Transform 
    Computes locations of circles returns list of [[x, y, radius]]
    :method:    detection method [cv2.HOUGH_GRADIENT, cv2.HOUGH_GRADIENT_ALT]
    :dp:        inverse ratio between accumulator resolution and image resolution
    :minDist:   min distance between detected circle centers
    :p1:        CHT parameter 1
    :p2:        CHT parameter 2
    :retval:    list[tuple[tuple[int, int, int]]
    """
    circles = cv.HoughCircles(img, method, dp, minDist, param1=p1, param2=p2)
    return np.uint16(np.around(circles))


def edge_detection(img: np.ndarray) -> np.ndarray:
    return cv.Canny(img, 50, 200, None, 3)

def LHT(img: np.ndarray):
    """Line Hough Transform. """
    return cv.HoughLines(img, 1, pi / 180, 150, None, 0, 0)


@timing
def find_and_plot_gauges(img, fname: str='out.png'):
    cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    for [[x, y, r]] in CHT(gaussian_blur(img)):
        # draw the outer circle
        cv.circle(cimg,(x, y), r, green, 2)
        # draw the center of the circle
        cv.circle(cimg,(x, y) ,2, red,3)
    cv.imwrite(fname, cimg)


@timing
def find_and_plot_lines(img, fname: str='out.png'):
    cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    blur = gaussian_blur(img, kernel=(9, 9), sigma=1)
    edges = edge_detection(blur)
    cdst = np.copy(edges)
    lines = LHT(edges)
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = cos(theta)
            b = sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(cdst, pt1, pt2, red, 3, cv.LINE_AA)
    cv.imwrite(fname, cdst)


red = (0,0,255)
green = (0, 255, 0)
img = cv.imread('example/1.png', 0)
# find_and_plot_gauges(img)
[[[x, y, r]]] = CHT(gaussian_blur(img))
find_and_plot_lines(crop(img, (x, y), (630, 630)))
# cv.imwrite('out.png', crop(img, (x, y), (625, 625)))

# for [[a, b, c, d]] in lines:
#     cv.line(cimg, (a, b), (c, d), green, 2)
# cv.imwrite('out.png', cimg) cv.imwrite('edges.png', img_edges)
