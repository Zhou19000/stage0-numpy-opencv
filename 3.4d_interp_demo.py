import cv2
import numpy as np
#
# img = np.zeros((40, 40, 3), np.uint8)
# img[:, :20] = (0, 0, 255)  # 左半红，右半黑
#
# big_n = cv2.resize(img, (200, 200), interpolation=cv2.INTER_NEAREST)
# big_l = cv2.resize(img, (200, 200), interpolation=cv2.INTER_LINEAR)
#
# print("NEAREST 边界:", big_n[100, 90:110, 2])  # 通道 2 = R
# print("LINEAR  边界:", big_l[100, 90:110, 2])
#
# pad = cv2.copyMakeBorder(img, 10, 20, 30, 40, cv2.BORDER_CONSTANT, value=(114, 114, 114))
# print("补边后 shape:", pad.shape, pad[0, 0])

