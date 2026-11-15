"""
3.7 阈值、直方图与对比度增强
================================================
本节五个函数：
    cv2.threshold            一刀切二值化（返回元组！）
    cv2.adaptiveThreshold    分区域自适应阈值（返回单个值！）
    cv2.calcHist             直方图统计
    cv2.equalizeHist         全局均衡
    cv2.createCLAHE          分块+限高均衡（你的毕设主角）

规则：每处 "预测:" 后面先把答案写进注释，全部写完再一次性运行。
"""
import cv2
import numpy as np

# ========== 造图：灰底 + 暗块 + 亮块 + 稀疏噪点 ==========
# 暗块 100、底 120、亮块 140 —— 三档灰度挤在 40 的宽度里，低对比度
# 噪点：每隔 23 行 37 列撒一个亮点（后面看 CLAHE 会不会把它放大）
np.random.seed(42)
g = np.full((120, 160), 120, np.uint8)
g[20:60, 20:70] = 100          # 左上暗块 40x50
g[70:110, 90:150] = 140        # 右下亮块 40x60
noise = np.random.randint(0, 3, (120, 160)).astype(np.uint8)
noise[::23, ::37] = 90         # 稀疏亮点
gray = g + noise               # min 100 / max 230

print("原图:", gray.shape, gray.dtype, "范围:", gray.min(), "~", gray.max())


print("\n== Part 1: threshold 固定阈值 + Otsu ==")
r1, t1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
print("r1 =", r1, " 类型:", type(r1).__name__)     # 预测1: r1 是多少？127。int 还是 float？float
print("t1.shape =", t1.shape)                       # 预测2: shape 是？gray.shape=(120,160)。
                                                     # unique 出来几个值、哪些值？两个值，0和255.
print("t1.unique =", np.unique(t1))

r2, t2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# 预测3: r2 是 0 吗？（Otsu 会自己算阈值，算出来大约在哪一带：100 前后 / 120 前后 / 140 前后）不是，是OTSU算出来的阈值，应该在120前后
print("r2 (Otsu 算的) =", r2)
white = int((t2 == 255).sum())
print("Otsu 后白像素:", white, "/", gray.size, "≈", round(white / gray.size * 100, 1), "%")
# 预测4: 白像素占比接近多少？哪些像素变白了？（暗块100/底120/亮块140/噪点210+） 约为12.5% 亮块和噪点变白了


print("\n== Part 2: adaptiveThreshold 自适应阈值 ==")
# 同一张图，只改 C，看白像素数量往哪边变
a1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                           cv2.THRESH_BINARY, 11, 5)    # C=5
a2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                           cv2.THRESH_BINARY, 11, 1)    # C=1
# 预测5: C=5 和 C=1，谁的白像素多？（提示：有效阈值 = 邻域均值 − C，  C=5白像素多
#        C 越大有效阈值越低还是越高？低阈值放进来的像素多还是少？）     C 越大有效阈值越低，低阈值放进来的像素多
print("C=5 白像素:", int((a1 == 255).sum()), "  C=1 白像素:", int((a2 == 255).sum()))

try:
    cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                          cv2.THRESH_BINARY, 10, 5)     # blockSize=10，偶数！
except cv2.error as e:
    msg = str(e)
    print("blockSize=10 报错了:", msg[msg.find("error:") :][:80])
# 预测6: blockSize=10 能跑吗？报错信息里那个条件是什么？ 不能，必须得是正奇数


print("\n== Part 3: calcHist 直方图 ==")
h = cv2.calcHist([gray], [0], None, [256], [0, 256])
# 预测7:⚠️ h.shape = (256,)（你环境是 OpenCV 5.0.0，你自己抓出来的那个答案）
#        ⚠️h.dtype = float32
print("h:", h.shape, h.dtype)
# 预测8: h.sum() 等于多少？（不用算具体数，说它应该等于什么）等于所有不同灰度值的数量总和
print("h.sum() =", h.sum(), "  总像素 =", gray.size)
# 预测9: 直方图最高的柱子（像素最多的灰度值）是哪个？120（提示：图里面积最大的是哪个灰度档）
print("柱子最高的灰度值 =", int(h.argmax()))


print("\n== Part 4: equalizeHist vs CLAHE ==")
eq = cv2.equalizeHist(gray)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
cl = clahe.apply(gray)
clahe10 = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8, 8))
cl10 = clahe10.apply(gray)
# 用 std（标准差）量化对比度：std 越大 = 灰度拉得越开
# 预测10: 三个 std 从大到小排序。（eq 是全局硬拉，cl2 限得紧，cl10 限得松）eq  std>cl10>cl2 std
print("eq  std =", round(float(eq.std()), 1))
print("cl2 std =", round(float(cl.std()), 1))
print("cl10 std =", round(float(cl10.std()), 1))
# 预测11: cl 和 eq 的 shape 分别是？
print("shapes:", eq.shape, cl.shape) #eq.shape=(120,160)  cl.shape=(120,160)


print("\n== Part 5: 彩色图的均衡（毕设预热：只动 V 通道） ==")
# 彩色图不能直接 equalizeHist（只吃单通道），标准做法：BGR→HSV，只均衡 V
bgr = np.zeros((120, 160, 3), np.uint8)
bgr[:, :, 0] = 180                # 偏蓝的底
bgr[20:60, 20:70] = (255, 100, 0) # 一块橙（BGR）

hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)      # 空1: 转到哪个空间？转到HSV
hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])         # 空2: 均衡哪个通道？（V 在第几维）V通道，第三维
out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)       # 空3: 转回什么？转回BGR

print("out.shape:", out.shape)
print("out[100, 100]:", out[100, 100], " out[40, 40]:", out[40, 40])
# 预测12: 这两个点会是"蓝色系"还是"橙色系"？out[100, 100]是蓝色系。out[40, 40]是橙色系
#        （H 通道从头到尾没被动过 —— 这就是只均衡 V 的意义）
