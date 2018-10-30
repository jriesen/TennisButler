# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
    # grab the current frame
    frame = vs.read()

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    font = cv2.FONT_HERSHEY_SIMPLEX
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # cv2.imshow("Blurr Pass",hsv)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # cv2.imshow("mask", mask)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # find center of the frame, find width, height; then divide them by two to
    # find center
    width, height = frame.shape[:2]
    centerX = int(round(height/2))
    centerY = int(round(width))

    # draw a filled circle at the center of the frame
    cv2.circle(frame, (centerX, centerY), 5, (0, 0, 255), -1)

    # bilateraly filter the raw frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bilateral_filtered_image = cv2.bilateralFilter(gray, 5, 175, 175)
    # perform canny edge filter on filtered frame
    edges = cv2.Canny(bilateral_filtered_image, 25, 200)

    # find contours in edges
    _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True),
                                  True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 8) & (area > 30)):
            contour_list.append(contour)
            drawContour = cv2.drawContours(edges, contour_list,  -1, (255, 0,
                                                                      0), 2)
            cv2.imshow('Objects Detected', drawContour)

    # process all the contours in cnts
    for c in cnts:

        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # find the maximum contour (really need to find the largest distance)
        maxC = max(cnts, key=cv2.contourArea)
        M2 = cv2.moments(maxC)
        maxCenter = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
        focal = (48*12)/2.6
        # only proceed if the radius meets a minimum size
        if radius > 20:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                              (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            print(radius)
            # calculate distance to camera using known object dimensions
            distanceCamera = (2.6*focal)/radius
            distText = str(distanceCamera)
            distText2 = "distText inches"
            cv2.putText(frame, str(round(distanceCamera, 1)), (20, 150), font,
                        1, (255, 255, 255), 1)
            # Draw a line between the center of frame and detected object
            lineThickness = 1
            cv2.line(frame, (centerX, centerY), (center), (0, 255, 0),
                     lineThickness)
            # print('This is the value of center ',center)
            (localX, localY) = maxCenter
            distCenter = int(round(((localX-centerX)**2+(localY-centerY)**2)
                                   ** .5))
        # print('this is the Distance from center:',distCenter)
        # write the Distance to Center on image

            cv2.putText(frame, str(distCenter), (20, 100), font, 1, (255, 255,
                                                                     255), 1)

            cv2.GaussianBlur(frame, (11, 11), 0)

    # # update the points queue
    # pts.appendleft(center)
    #
    # # loop over the set of tracked points
    # for i in range(1, len(pts)):
    # 	# if either of the tracked points are None, ignore
    # 	# them
    # 	if pts[i - 1] is None or pts[i] is None:
    # 		continue
    #
    # 	# otherwise, compute the thickness of the line and
    # 	# draw the connecting lines
    # 	thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    # 	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # smooth the frame

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()
