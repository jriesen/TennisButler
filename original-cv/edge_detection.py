import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt


def nothing(x):
    pass


img = cv2.imread('court1.jpg', 1)
img = imutils.resize(img, width=1000)
cv2.namedWindow('image')
hcircles = cv2.imread('court1.jpg', 0)
hcircles = imutils.resize(hcircles, width=1000)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bilateral_filtered_image = cv2.bilateralFilter(gray, 5, 175, 175)
edges = cv2.Canny(bilateral_filtered_image, 25, 200)
# find contours in edges
_, contours, _ = cv2.findContours(edges, cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)
contour_list = []
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02*cv2.arcLength(contour, True),
                              True)
    area = cv2.contourArea(contour)
    if ((len(approx) > 3) & (area > 20)):
        contour_list.append(contour)
        drawContour = cv2.drawContours(edges, contour_list,  -1, (255, 0,
                                                                  0), 2)

# use Hough Circles to find balls in imagecv2.createTrackbar('R','image',0,255, nothing)
cv2.createTrackbar('Min Distance', 'image', 0, 255, nothing)
cv2.createTrackbar('Param 1', 'image', 0, 255, nothing)
cv2.createTrackbar('Param 2', 'image', 0, 255, nothing)
cv2.createTrackbar('Min Radius', 'image', 0, 255, nothing)
cv2.createTrackbar('Max Radius', 'image', 0, 255, nothing)

# switch = '0 : OFF \n1 : ON'
# cv2.createTrackbar(switch, 'img', 0, 1, nothing)


while(1):

    cv2.imshow('detected circles', img)

    mindistance = cv2.getTrackbarPos('Min Distance', 'image')
    param1 = cv2.getTrackbarPos('Param 1', 'image')
    param2 = cv2.getTrackbarPos('Param 2', 'image')
    minRadius = cv2.getTrackbarPos('Min Radius', 'image')
    maxRadius = cv2.getTrackbarPos('Max Radius', 'image')
    # s = cv2.getTrackbarPos(switch, 'img')
    # if s == 0:
    #    img[:] = 0
    # else:
    #    img[:] = [mindistance, param1, param2, minRadius, maxRadius]

    # gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(hcircles, cv2.HOUGH_GRADIENT, 2, 120,
                               param1=50, param2=60, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imshow("img", edges)
# plt.subplot(121), plt.imshow(img, cmap='gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(edges, cmap='gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
