import cv2
import os
import numpy as np
from scipy.ndimage.filters import gaussian_filter

# =================================================
# Take sequence input helper function
# =================================================

def getInput(dir):
    for dirname, dirnames, filenames in os.walk(dir):
        if dirname == dir:
            return dirnames, filenames

# =================================================
# gaussian blur helper function
# =================================================

def gaussian_blur(bgr_img, kernel_size=3):
  return np.array([gaussian_filter(bgr_img[i], kernel_size) for i in xrange(bgr_img.shape[0])])


#
# main
#

if __name__ == '__main__':
    
    dirct, images = getInput('sample_drive/cam_0')
    sorted(images)

    for i in range(len(images)):
        image = cv2.imread('sample_drive/cam_0/' + images[i])
        image = cv2.resize(image, (400, 400))
        cv2.namedWindow("Test")
        cv2.imshow("Test", image)
        print(images[i])
        cv2.waitKey(0)



