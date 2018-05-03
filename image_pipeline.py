import cv2
import numpy as np
import calibrate_camera

# Calculate directional gradient
def abs_sobel_thresh(img, orient='x', sobel_kernel=3, thresh=(0, 255)):
    # Apply threshold
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if orient == 'x':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    else:
        sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
        
    abs_sobel = np.absolute(sobel)
    scaled = np.uint8(255*abs_sobel / np.max(abs_sobel))
    
    grad_binary = np.zeros_like(scaled)
    grad_binary[(scaled >= thresh[0]) & (scaled <= thresh[1])] = 1
    
    return grad_binary

# Calculate gradient magnitude
def mag_thresh(image, sobel_kernel=3, mag_thresh=(0, 255)):
    # Apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    
    mag = np.sqrt(sobelx**2 + sobely**2)
    scaled = np.uint8(255*mag / np.max(mag))
    
    mag_binary = np.zeros_like(scaled)
    mag_binary[(scaled >= mag_thresh[0]) & (scaled <= mag_thresh[1])] = 1
    
    return mag_binary

# Calculate gradient direction
def dir_threshold(image, sobel_kernel=3, thresh=(0, np.pi/2)):
    # Apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    
    direction = np.arctan2(abs_sobelx, abs_sobely)
    dir_binary = np.zeros_like(direction)
    dir_binary[(direction >= thresh[0]) & (direction <= thresh[1])] = 1
    
    return dir_binary

# Threshole the saturation value in colorspace HLS
def hls_select(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    S = hls[:,:,2]
    binary_output = np.zeros_like(S)
    binary_output[(S >  thresh[0]) & (S <= thresh[1])] = 1
    return binary_output

def hls_select_lightness(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    L = hls[:,:,1]
    binary_output = np.zeros_like(L)
    binary_output[(L > thresh[0]) & (L <= thresh[1])] = 1
    return binary_output


# image read in from matplotlib (mp)
def pipeline(undistort):
    # Kernel size
    ksize = 15
    # Gradient in X direction
    gradx = abs_sobel_thresh(undistort, orient='x', sobel_kernel=ksize, thresh=(50, 100))
    # Gradient in Y direction
    grady = abs_sobel_thresh(undistort, orient='y', sobel_kernel=ksize, thresh=(50, 100))
    # Gradient Magnitude
    mag_binary = mag_thresh(undistort, sobel_kernel=ksize, mag_thresh=(70, 100))
    # Gradient Direction
    dir_binary = dir_threshold(undistort, sobel_kernel=ksize, thresh=(0.3, 0.9))
    # Saturation Value from HLS Colorspace
    s_binary = hls_select(undistort, thresh=(90, 255))
    # Lightness Value from HSL Colorspace
    l_binary = hls_select_lightness(undistort, thresh=(100, 255))

    combined_images = np.zeros_like(s_binary)
    combined_images[((gradx == 1) & (grady == 1)) | 
                     ((mag_binary == 1) & (dir_binary == 1) | (s_binary == 1)) &
                     ((s_binary == 1) & (l_binary == 1))] = 1
    return combined_images


































