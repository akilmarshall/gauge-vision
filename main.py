import numpy as np
import cv2 as cv
from functools import wraps
from time import time


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

def blur(img: np.ndarray) -> np.ndarray:
    return cv.GaussianBlur(img, (5, 5), 0)


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


@timing
def find_and_plot_gauges(img, fname: str='out.png'):
    cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    for [[x, y, r]] in CHT(blur(img)):
        # draw the outer circle
        cv.circle(cimg,(x, y), r, green, 2)
        # draw the center of the circle
        cv.circle(cimg,(x, y) ,2, red,3)

    cv.imwrite(fname, cimg)


red = (0,0,255)
green = (0, 255, 0)
img = cv.imread('example/1.png', 0)
find_and_plot_gauges(img)

# lines = cv.HoughLinesP(
#         img_edges,
#         1,                  # rho
#         np.pi / 180,    # theta
#         150,                 # threashold
#         None,               # min line len
#         0,                 # max line gap
#     )
# for [[a, b, c, d]] in lines:
#     cv.line(cimg, (a, b), (c, d), green, 2)
# cv.imwrite('out.png', cimg)
# cv.imwrite('edges.png', img_edges)
