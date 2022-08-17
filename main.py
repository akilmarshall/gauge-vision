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
    w, h = (a // 2 for a in size)
    image = Image.fromarray(img)
    return np.array(image.crop((x - w, y - h, x + w, y + h)))


class Detect:
    """
    A class encapsulating the environmental parameters and abstract methods necessary to accomplish
    the task of reading pressure values from images of gauges.
    Algorithms should be parameterized with instances of this class.
    """
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
            t1=50,
            t2=200,
            aperture=3,
            ):
        """
        Circle Hough Transform 
        Computes locations of circles returns list of [[x, y, radius]]
        :dp:        inverse ratio between accumulator resolution and image resolution
        :minDist:   min distance between detected circle centers
        :p1:        CHT parameter 1
        :p2:        CHT parameter 2
        Gaussian Blur
        :kernel:	Gaussian kernel size.
        :sigma:	    Gaussian kernel standard deviation in XY direction.
        Line Hough Transform
        :rho:	    Distance resolution of the accumulator in pixels
        :theta:	    Angle resolution of the accumulator in radians
        :threshold:	Accumulator threshold parameter. Only those lines are returned that get enough votes
        Canny (edge detection)
        :t1:        threshold 1
        :t2:        threshold 2
        :aperture:  aperture size
        """
        self.fname = fname

        # CHT params
        self.dp = dp
        self.minDist = minDist
        self.p1 = p1
        self.p2 = p2

        # Gaussian Blur params
        self.kernel = kernel
        self.sigma = sigma

        # Line Hough Transform params
        self.rho = rho
        self.theta = theta
        self.threshold = threshold

        # Canny parameters
        self.t1 = t1
        self.t2 = t2
        self.aperture = aperture

    def blur(self, img: np.ndarray) -> np.ndarray:
        """
        Abstract blur method for image processing.
        currently using cv2.GaussianBlur, parameterized by: [kernel, sigma]
        """
        return cv.GaussianBlur(img, self.kernel, self.sigma) 

    def edge_detection(self, img: np.ndarray, edges=None) -> np.ndarray:
        """
        Abstract edge detection method for image processing.
        currently using cv2.Canny, parameterized by: [self.t1, self.t2, self.aperture]

        optionally seed edges with a list of (x, y)?
        """
        return cv.Canny(img, self.t1, self.t2, edges, self.aperture)


    def CHT(self, img: np.ndarray):
        """
        Circle Hough Transform.
        Attempt to find the spatial parameters of a gauge in the image

        returns: (x, y, r) | None
        """
        result = cv.HoughCircles(img, cv.HOUGH_GRADIENT, dp=self.dp, minDist=self.minDist, param1=self.p1, param2=self.p2)
        if result is not None:
            [[[x, y, r]]] = result
            return int(x), int(y), int(r)
        return None


    def LHT(self, img: np.ndarray):
        """
        Linear Hough Transform.
        A generator for tuple pairs describing the detected lines.

        returns: [((a, b), (c, d))]
        """
        result = cv.HoughLines(img, self.rho, self.theta, self.threshold)
        if result is not None:
            for [[rho, theta]] in result: 
                a = cos(theta)
                b = sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                yield pt1, pt2


# helper color variables for plotting functions
red = (0, 0, 255)
green = (0, 255, 0)


def find_and_plot_gauge(img, detect: Detect, fname: str='out.png'):
    """An example to use a parameterized Detect object to apply the Hough transform to find and plot the gauge center. """
    img_copy = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    result = detect.CHT(img)
    if result:
        x, y, r = result
        # draw the outer circle
        cv.circle(img_copy, (x, y), r, green, 2) 
        # draw the center of the circle
        cv.circle(img_copy, (x, y), 2, red, 3)
    cv.imwrite(fname, img_copy)


def find_and_plot_needle(img, detect: Detect, fname: str='out.png'):
    """An example of the entire image processing pipeline, except the result is used to plot the detected needle. """
    result = detect.CHT(img)
    if result:
        x, y, r = result
        img = crop(img, (x, y), (2 * r, 2* r))
        img_copy = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        img = detect.blur(img)
        img = detect.edge_detection(img)
        for (a, b), (c, d) in detect.LHT(img): 
            # draw the detected line in red
            cv.line(img_copy, (a, b), (c, d), red, 3, cv.LINE_AA)

        cv.imwrite('out.png', img_copy)
    else:
        print('no gauge found')


img = cv.imread('example/2.png', 0)
detect = Detect(kernel=(15, 15), sigma=3)
# find_and_plot_gauge(img, detect)
find_and_plot_needle(img, detect)

# blur is cranked up too high?
