import sys
import base64
import numpy as np
import cv2

assistant_result = np.ones((200, 1500, 3), np.uint8) * 255
cv2.imshow('HAND', assistant_result)
cv2.waitKey()