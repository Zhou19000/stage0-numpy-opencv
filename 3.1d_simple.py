import cv2
import numpy as np

img = np.zeros((100, 100, 3), np.uint8)   # 造一张 100x100 黑图
img[20:60, 20:60] = (0, 0, 255)           # 中间涂一块红色

ok, buf = cv2.imencode(".png", img)       # 图像 → 字节
buf.tofile("简.png")                       # 字节 → 文件

data = np.fromfile("简.png", dtype=np.uint8)   # 文件 → 字节
img2 = cv2.imdecode(data, cv2.IMREAD_COLOR)    # 字节 → 图像

print(img.shape, img2.shape, np.array_equal(img, img2))

# 自己敲的
ok1,buf=cv2.imencode(".png",img)
buf.tofile("红块.png")

data1=np.fromfile("红块.png", dtype=np.uint8)
img3=cv2.imdecode(data1,cv2.IMREAD_GRAYSCALE)
cv2.imshow("", img3)
cv2.waitKey(0)
cv2.destroyAllWindows()