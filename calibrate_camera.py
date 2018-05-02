import cv2
import numpy as np
import matplotlib.pyplot as plt

nx = 9 # Number of Corners in the x direction
ny = 6 # Number of Corners in the y direction

def draw_chessboard_corners(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

	if ret == True:
	    cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
	    plt.imshow(img)

def find_image_points(calibration_image_paths):
	objpoints = [] # 3D points in real world space
	imgpoints = [] # 2D points in image plane

	# Prepare objpoints like (0,0,0), (1,0,0) (2,0,0)....(9,6,0)
	objp = np.zeros((nx*ny, 3), np.float32)
	objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2) # x, y coordinates

	for fname in calibration_image_paths:
	    img = cv2.imread(fname)
	    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

	    if ret == True:
	        print(fname)
	        imgpoints.append(corners)
	        objpoints.append(objp)

	        img = cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
	        plt.imshow(img)

	return objpoints, imgpoints



def cal_undistort_coeffs(img, objpoints, imgpoints):
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                       img.shape[1::-1], None, None)
    return mtx, dist

def undistort_image(img, mtx, dist):
    return cv2.undistort(img, mtx, dist, None, mtx)


























