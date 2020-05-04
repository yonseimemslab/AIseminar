# Standard imports
import cv2
import numpy as np


im = cv2.imread("tes"
                "t.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow('image',im)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()


#Detect blobs.
keypoints = detector.detect(im)
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Detect blobs.
keypoints = detector.detect(im)
print (keypoints)
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
#im_with_keypoints = draw_keypoints(im, keypoints)

# Show keypoints
print (im_with_keypoints)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

#contour detection

# ret, thresh = cv2.threshold(im, 127, 255, 0)
# im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# im_with_contour = cv2.drawContours(im, contours, -1, (0,255,0), 2)
# cnt = contours[0]
# print (type(contours))
# cv2.imshow('contour', im_with_contour)
# cv2.waitKey(0)
