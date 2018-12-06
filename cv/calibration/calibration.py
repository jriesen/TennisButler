import numpy as np
import cv2
import glob

# termination criteria
subPixCriteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001
)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*5, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

images = glob.glob('calibration-images/*.jpeg')

for fname in images:
    print('Processing image ' + fname)
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 5), None)

    # If found, add object points, image points (after refining them)
    if ret is True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), subPixCriteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (7, 5), corners, ret)
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        cv2.imshow('image', img)

        cv2.waitKey(500)

print('All images processed.')

rms, cameraMatrix, distanceCoeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)
print(cameraMatrix)
print(distanceCoeffs)
print(rvecs)
print(tvecs)

cv2.destroyAllWindows()
