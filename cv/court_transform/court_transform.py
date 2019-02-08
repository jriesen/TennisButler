import numpy as np
import cv2
import glob

# HSV values:
green_lower = (29, 86, 10)
green_upper = (64, 255, 255)

white_lower = (0, 0, 210)     # S=0%, V=90%
white_upper = (255, 25, 255)  # S=10%, V=100%

# Joseph's iPhone 7 camera calibration
camera_matrix = np.array([[3.26547440e+03, 0.00000000e+00, 1.98304155e+03],
                          [0.00000000e+00, 3.25755683e+03, 1.49452585e+03],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
distance_coeffs = np.array([[2.83900242e-01, -1.96505698e+00,  6.32435233e-04,
                             6.94889726e-04,  4.24150588e+00]])

fnames = glob.glob('images/*.jpeg')
for fname in fnames:
    image = cv2.imread(fname)
    print('Processing image ' + fname)

    # Image correction:
    # height, width = image.shape[:2]
    # new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    #     camera_matrix, distance_coeffs, (width, height), 1, (width, height)
    # )
    # image = cv2.undistort(
    #     image, camera_matrix, distance_coeffs, None, new_camera_matrix
    # )
    # x, y, w, h = roi
    # image = image[y:y+h, x:x+w]

    cv2.imshow("image", cv2.resize(image, (0, 0), fx=0.25, fy=0.25))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # cv2.imshow("hsv", cv2.resize(hsv, (0, 0), fx=0.25, fy=0.25))

    lineMask = cv2.inRange(hsv, white_lower, white_upper)
    # lineMask = cv2.erode(lineMask, None, iterations=2)
    lineMask = cv2.dilate(lineMask, None, iterations=2)

    blurred = cv2.GaussianBlur(lineMask, (3, 3), 0)
    # cv2.imshow("blurred", cv2.resize(blurred, (0, 0), fx=0.25, fy=0.25))

    edges = cv2.Canny(blurred, 150, 200, apertureSize=3)
    cv2.imshow("edges", cv2.resize(edges, (0, 0), fx=0.25, fy=0.25))

    # lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 300)
    print('Total lines: {0}'.format(np.size(lines)))

    for line in lines:
        for r, theta in line:
            # Stores the value of cos(theta) in a
            a = np.cos(theta)
            # Stores the value of sin(theta) in b
            b = np.sin(theta)
            # x0 stores the value rcos(theta)
            x0 = a*r
            # y0 stores the value rsin(theta)
            y0 = b*r
            # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
            x1 = int(x0 + 5000*(-b))
            # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
            y1 = int(y0 + 5000*(a))
            # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
            x2 = int(x0 - 5000*(-b))
            # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
            y2 = int(y0 - 5000*(a))
            # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
            # (0,0,255) denotes the colour of the line to be
            # drawn. In this case, it is red.
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 4)

    cv2.imshow("output", cv2.resize(image, (0, 0), fx=0.25, fy=0.25))
    # cv2.imwrite(fname + ".with_lines.jpg", image)

    # This INCREDIBLY helpful answer let me determine major intersection points
    # of the Hough lines while ignoring the overlap of the near-parallel lines:
    # https://stackoverflow.com/a/46572063/2801058

    # mask = cv2.inRange(hsv, green_lower, green_upper)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
    # small_mask = cv2.resize(mask, (0, 0), fx=0.25, fy=0.25)
    # cv2.imshow("mask", small_mask)

    key = cv2.waitKey(0) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
