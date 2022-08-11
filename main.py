import numpy as np
import cv2 as cv
img = cv.imread('example/2.png',0)
img = cv.GaussianBlur(img, (5, 5), 0)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
circles = cv.HoughCircles(
        img,
        cv.HOUGH_GRADIENT,  # method
        1,                  # dp
        50,                 # minDist
        param1=300, 
        param2=150,
        )
circles = np.uint16(np.around(circles))
print(circles)
for i in circles[0,:]:
    # draw the outer circle
    cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv.imwrite('out.png', cimg)
