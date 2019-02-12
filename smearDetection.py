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


def process_image(dir_path):
    images = []
    for image in os.listdir(dir_path):
        img = cv2.imread(os.path.join(dir_path,image))
        if img is not None:
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eq_img = cv2.equalizeHist(gray_image)
            blur_img = cv2.blur(eq_img, (3,3))
            ret,thresh_img = cv2.threshold(blur_img,127,255,cv2.THRESH_BINARY)
            images.append(thresh_img)
    return images

def calc_mean_image(arr, length):

    i = 1
    sum_image = arr[0] * 1/length
    while (i < len(arr)):
        sum_image = cv2.add(sum_image,arr[i]* 1/length)
        i += 1
    return sum_image

def create_binary_mask(img):

    kernel = np.ones((10,10),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 5)
    dilation = cv2.dilate(erosion,kernel,iterations = 5)
    return dilation
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



