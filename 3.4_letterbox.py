import cv2
import numpy as np

def letterbox(img, size=640, color=(114, 114, 114)):
    h, w = img.shape[:2]
    scale = min([size/h,size/w])                                         # 空1: min 还是 max？size 除以谁？
    nw, nh = int(scale*w), int(scale*h)                                     # 空2: 新宽新高，注意 int()
    resized = cv2.resize(img, (nw, nh))
    dw, dh = size - nw, size - nh
    top, bottom = dh // 2, dh - dh // 2
    left, right = dw // 2, dw - dw // 2
    out = cv2.copyMakeBorder(resized,top, bottom,left, right,   # 空3: 五个位置参数
                             cv2.BORDER_CONSTANT, value=color)
    return out, scale, (left, top)

# ========== 运行区 ==========
img = np.zeros((200, 300, 3), np.uint8)
img[:, :150] = (0, 0, 255)          # 左半红，右半黑

out, scale, pad = letterbox(img)
print(out.shape, scale, pad)
print(out[320, 0], out[320, 639])   # 中部一行的最左、最右像素
print(out[0, 0], out[639, 320])     # 左上角、底边中部
print(out[106, 0], out[107, 0])     # 补边和图像的分界线
