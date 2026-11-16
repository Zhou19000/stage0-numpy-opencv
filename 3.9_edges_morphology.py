# 3.9 边缘检测 + 形态学 —— 毕设检测链路预演
# 线1: 二值目标图 -> open 灭噪点 -> close 填洞 -> 数连通块
# 线2: Canny 出细边 -> dilate 加粗（细边经不起腐蚀！）
#
# ========== 我的预测（跑之前填！）==========
# 预测1 原图白色连通块数（4 个噪点 + 方块，数数看）:
# 预测2 open(5x5) 后连通块数（噪点全灭了吗）:
# 预测3 close(15x15) 后白像素（8x8 的洞 64 个像素填回来了吗）:
# 预测4 Canny 后连通块数（外框+内框+4 噪点，自己推）:
# 预测5 dilate(5x5) 后白像素（336 会变大还是变小？）:

import cv2
import numpy as np

# 1. 造图: 黑底 + 白方块(=目标) + 洞(=目标内部空洞) + 噪点
img = np.zeros((200, 200), np.uint8)
img[60:130, 60:130] = 255          # 70x70 白方块
img[100:108, 100:108] = 0          # 方块内 8x8 黑洞
for y, x in [(20, 30), (160, 40), (170, 170), (30, 150)]:
    img[y:y+3, x:x+3] = 255        # 四个 3x3 噪点

def count(img_):
    """数白色连通块个数"""
    n, _ = cv2.connectedComponents(img_)
    return n - 1

# ========== 线1: 目标块链（形态学的本职工作）==========
print('原图连通块:', count(img), ' 白像素:', int((img > 0).sum()))   # 预测1   5个白色块

k5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, k5)
print('open(5x5) 后连通块:', count(opened), ' 白像素:', int((opened > 0).sum()))  # 预测2   1个，4个小的3*3的噪点没有了

k15 = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, k15)
print('close(15x15) 后白像素:', int((closed > 0).sum()))              # 预测3   8*8 的黑块没有了，中间只有70*70的白方块了

# ========== 线2: 边缘链（细边怕腐蚀，只能加粗）==========
edges = cv2.Canny(img, 50, 150)
print('Canny 后连通块:', count(edges), ' 白像素:', int((edges > 0).sum()))  # 预测4    6个连通块

dilated = cv2.dilate(edges, k5)
print('dilate(5x5) 后白像素:', int((dilated > 0).sum()))              # 预测5   白色像素会变大
