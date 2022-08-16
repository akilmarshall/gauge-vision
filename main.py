from functools import wraps
from math import cos, pi, sin
from time import time

from PIL import Image
import cv2 as cv
import numpy as np



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

def edge_detection(img: np.ndarray) -> np.ndarray:
    return cv.Canny(img, 50, 200, None, 3)


class Detect:
    def __init__(
            self,
            fname='out.png',
            dp=1,
            minDist=50,
            p1=300,
            p2=150,
            kernel=(9, 9),
            sigma=1,
            rho=1,
            theta=pi / 180,
            threshold=150,
            ):
        """
        Circle Hough Transform 
        Computes locations of circles returns list of [[x, y, radius]]
        :method:    detection method [cv2.HOUGH_GRADIENT, cv2.HOUGH_GRADIENT_ALT]
        :dp:        inverse ratio between accumulator resolution and image resolution
        :minDist:   min distance between detected circle centers
        :p1:        CHT parameter 1
        :p2:        CHT parameter 2
        :retval:    list[tuple[tuple[int, int, int]]
        Line Hough Transform
        """
        self.fname = fname
        self.dp = dp
        self.minDist = minDist
        self.p1 = p1
        self.p2 = p2
        self.kernel = kernel
        self.sigma = sigma
        self.rho = rho
        self.theta = theta
        self.threshold = threshold

    def gauge(self, img: np.ndarray):
        """Compute the position and radius of the gauge in image. """
        result = cv.HoughCircles(
                gaussian_blur(img),
                cv.HOUGH_GRADIENT,
                dp=self.dp,
                minDist=self.minDist,
                param1=self.p1,
                param2=self.p2
            )
        if result is not None:
            # now that result is not None
            [[[x, y, r]]] = result 
            return int(x), int(y), int(r)


    def needle(self, img: np.ndarray):
        result = cv.HoughLines(edge_detection(gaussian_blur(img, kernel=self.kernel, sigma=self.sigma)),
                self.rho, self.theta, self.threshold)
        if result is not None:
            for [[rho, theta]] in result: 
                a = cos(theta)
                b = sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                yield pt1, pt2


red = (0,0,255)
green = (0, 255, 0)


def find_and_plot_gauge(img, detect: Detect, fname: str='out.png'):
    img_copy = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    result = detect.gauge(img)
    if result:
        x, y, r = result
        # draw the outer circle
        cv.circle(img_copy, (x, y), r, green, 2) 
        # draw the center of the circle
        cv.circle(img_copy, (x, y), 2, red, 3)
    cv.imwrite(fname, img_copy)


def find_and_plot_needle(img, detect: Detect, fname: str='out.png'):
    img_copy = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    for (a, b), (c, d) in detect.needle(img): 
        cv.line(img_copy, (a, b), (c, d), red, 3, cv.LINE_AA)
    cv.imwrite(fname, img_copy)




img = cv.imread('example/2.png', 0)
detect_a = Detect()
# find_and_plot_gauge(img, detect_a)
find_and_plot_needle(img, detect_a)
