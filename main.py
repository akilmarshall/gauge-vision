import numpy as np
import cv2 as cv


red = (0,0,255)
green = (0, 255, 0)
img = cv.imread('example/2.png',0)
img = cv.GaussianBlur(img, (7, 7), 0)
img_edges = cv.Canny(img, 100, 200)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)

# circles = cv.HoughCircles(
#         img,
#         cv.HOUGH_GRADIENT,  # method
#         1,                  # dp
#         50,                 # minDist
#         param1=300, 
#         param2=150,
#         )
# circles = np.uint16(np.around(circles))
# for [[x, y, r]] in circles:
#     # draw the outer circle
#     cv.circle(cimg,(x, y), r, green, 2)
#     # draw the center of the circle
#     cv.circle(cimg,(x, y) ,2, red,3)


lines = cv.HoughLinesP(
        img_edges,
        1,                  # rho
        np.pi / 180,    # theta
        150,                 # threashold
        None,               # min line len
        0,                 # max line gap
    )
for [[a, b, c, d]] in lines:
    cv.line(cimg, (a, b), (c, d), green, 2)
cv.imwrite('out.png', cimg)
cv.imwrite('edges.png', img_edges)
