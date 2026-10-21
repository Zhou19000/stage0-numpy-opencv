"""
第 3 章 OpenCV · 3.2  BGR / RGB、灰度、HSV、通道拆分

老规矩：每个 print 前先写 # 预测: xxx，写不出来写 # 预测: ⚠️
写完全部预测后再运行。
"""
import os
import numpy as np
import cv2


# ============================================================
# Part 0  造图（复用 3.1 的 scene）
# ============================================================
def make_scene(h=240, w=320):
    img = np.zeros((h, w, 3), np.uint8)
    img[:, :, 0] = np.linspace(40, 200, h, dtype=np.uint8)[:, None]
    img[:, :, 1] = 90
    img[:, :, 2] = 60
    cv2.rectangle(img, (30, 40), (130, 140), (0, 0, 255), -1)        # 红色矩形
    cv2.circle(img, (220, 90), 45, (0, 255, 255), -1)                # 黄色圆
    cv2.rectangle(img, (170, 160), (290, 220), (0, 200, 0), -1)      # 绿色矩形
    cv2.putText(img, "OpenCV", (20, 200), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2)
    return img


scene = make_scene()

# 【0-1】先确认这三块是什么颜色
# 预测: scene[90, 80]（红色矩形内部）的 BGR = (0,0,255)
# 预测: scene[90, 220]（黄色圆心）的 BGR = (0,255,255)
# 预测: scene[190, 230]（绿色矩形内部）的 BGR = (0,200,0)⚠️注意看前面的代码
# 提示：都是 (B, G, R) 顺序，想一想"红"在 BGR 里哪个位置是 255 R通道


# ============================================================
# Part 1  BGR → RGB 的两种写法
# ============================================================
rgb = cv2.cvtColor(scene, cv2.COLOR_BGR2RGB)      # 方法一：cvtColor
rgb2 = scene[:, :, ::-1]                          # 方法二：通道倒序切片

# 【1-1】两种写法结果一样吗
# ⚠️预测: np.array_equal(rgb, rgb2) = ?True

# 【1-2】关键：谁是视图，谁是拷贝
# 预测: np.shares_memory(rgb, scene) = False   （rgb 和原图共享内存吗？）不共享
# 预测: np.shares_memory(rgb2, scene) = True  （rgb2 和原图共享内存吗？）共享

# 【1-3】同一个像素，两种顺序下分别长什么样
# 预测: scene[90, 80] =  (0,0,255) （BGR 顺序）
# 预测: rgb[90, 80]   =   (255,0,0)（RGB 顺序）
# 为什么这两个值"看起来一样"却含义不同？
# 因为维度的顺序不一样
# 【1-4】验证视图的副作用（看懂了这题你就真正懂了 2.13）
# rgb2 是视图，改它会怎样？
probe = scene.copy()          # 先复制一份干净的，别污染原图
view = probe[:, :, ::-1]
view[0, 0, 0] = 99            # 改"视图"的第 0 通道
# 预测: probe[0, 0, 0] = 40 【不变】
# 预测: probe[0, 0, 2] = 99  【变了】
# 预测: 说明 view[0,0,0] 实际上对应原图的哪个通道？
# R通道

# ============================================================
# Part 2  灰度图
# ============================================================
gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)

# 【2-1】形状怎么变
# 预测: gray.shape = (240,320)
# 预测: gray.ndim = 2
# 预测: 丢掉的是哪一维？（位置：第一个 / 最后一个）最后一个

# 【2-2】手动复现灰度公式，验证书里那个 0.299/0.587/0.114
manual = (0.114 * scene[:, :, 0] +      # B
          0.587 * scene[:, :, 1] +      # G
          0.299 * scene[:, :, 2])       # R
manual = np.clip(manual, 0, 255).astype(np.uint8)
# 预测: np.array_equal(manual, gray) = ?False
# 如果 False，可能差在哪里？（提示：OpenCV 用的是定点运算，取整方式可能不同）取整方式不一样
# ⚠️预测: np.abs(manual.astype(int) - gray.astype(int)).max() = ?  大概会是多少？1

# 【2-3】权重最大的通道是哪个，验证一下
# 预测: 0.299 / 0.587 / 0.114 三个数里，哪个最大？0.587 最大（绿的权重）
# 预测: 人眼对哪个颜色最敏感？绿色


# ============================================================
# Part 3  HSV 颜色空间
# ============================================================
hsv = cv2.cvtColor(scene, cv2.COLOR_BGR2HSV)

# 【3-1】形状和取值范围
# 预测: hsv.shape = (240,320,3)
# 预测: hsv.dtype = uint8
# 预测: H 通道的取值范围是什么？（写出两个数字）[0,179] 一共180个值

# 【3-2】各颜色在 HSV 里的值
# 预测: hsv[90, 220]（黄色圆心）= (30,255,255)
# 预测: hsv[90, 80]（红色矩形）=  （提示：红色 H 接近 0） (0,255,255)
# 预测: hsv[190, 230]（绿色矩形）= （提示：绿色角度 120°，要除以 2）(60,255,200)【记住 V 的定义：V = max(B, G, R)。 只要三个数里没一个到 255，V 就不到 255。】

# 【3-3】角度 → OpenCV H 的换算
# 预测: 蓝色（240°）在 OpenCV 里 H = 120
# 预测: 青色（180°）在 OpenCV 里 H = 90
# 预测: 紫色（300°）在 OpenCV 里 H = 150


# ============================================================
# Part 4  inRange 生成掩码
# ============================================================
lower = np.array([20, 100, 100])
upper = np.array([40, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

# 【4-1】掩码的形状和取值
# 预测: mask.shape = (240,320)        ← 重点！几维？2维
# 预测: mask.ndim = 2
# 预测: np.unique(mask) = [0,255]    （只有哪几种值？）

# 【4-2】这个范围筛出的是哪个形状？黄色圆形
# 预测: 黄色圆的面积大概多少？半径 45，面积 = πr² ≈ 6,361
# 预测: (mask > 0).sum() 大概是几千？（实际数会因为抗锯齿略有差异）6361

# 【4-3】掩码怎么用在三通道图上
only_yellow = cv2.bitwise_and(scene, scene, mask=mask)
# 预测: only_yellow.shape =(240,320,3)
# 预测: only_yellow[90, 220]（黄色圆心）= (0,255,255)
# 预测: only_yellow[90, 80]（红色矩形位置）= (0,0,0)
# 预测: 两维的 mask 怎么能作用在三维的图上？
# 变成(240,320,1)

# ============================================================
# Part 5  通道拆分与合并
# ============================================================
b, g, r = cv2.split(scene)

# 【5-1】split 出来的每个通道是什么形状
# 预测: b.shape = (240,320)
# 预测: b.ndim = 2
# ⚠️预测: np.array_equal(b, scene[:, :, 0]) = true

# 【5-2】合并回去
merged = cv2.merge([b, g, r])
# 预测: merged.shape = (240,320,3)
# ⚠️预测: np.array_equal(merged, scene) = true

# 【5-3】如果顺序写错会怎样（这是最经典的 bug）
wrong = cv2.merge([r, g, b])
# 预测: wrong.shape = (240,320,3)
# 预测: np.array_equal(wrong, scene) = False
# 预测: wrong[90, 80]（原本红色矩形内部）= ?  (255,0,0)（现在变成什么颜色了？）蓝色
# 一句话说明：r/g/b 顺序搞错，红蓝会怎样？取值对调


# ============================================================
# Part 6  例题 3-1：只保留红色矩形（先预测再做）
# ============================================================
# 要求：红色矩形原样保留，其余像素全变黑；并统计红色区域像素数
# 提示：红色 HSV 约为 (0, 255, 255)，但红色横跨 0 附近，可能需要两段范围

# 【6-1】先预测红色矩形的像素数
# 预测: cv2.rectangle(img, (30,40), (130,140)) 画出来的红色区域有多少像素？101*101=10201
# 提示：宽度 = 右-左+?，高度 = 下-上+?

# 【6-2】写代码（自己写，不要看笔记）
# TODO: 用 cv2.inRange 筛红色，再 bitwise_and 只保留红色
hsv=cv2.cvtColor(scene, cv2.COLOR_BGR2HSV)
maskred= cv2.inRange(hsv, np.array([0, 150, 150]), np.array([8, 255, 255]))
print(int((maskred > 0).sum()))
red=cv2.bitwise_and(scene, scene, mask=maskred)
print(red.shape, red[0, 0], red[90, 80])
# ============================================================
# 运行区
# ============================================================
print("=== Part 0 ===")
print("0-1 红块:", scene[90, 80], " 黄心:", scene[90, 220], " 绿块:", scene[190, 230])

print("=== Part 1 ===")
print("1-1 equal:", np.array_equal(rgb, rgb2))
print("1-2 shares cvtColor:", np.shares_memory(rgb, scene),
      " 切片:", np.shares_memory(rgb2, scene))
print("1-3 scene:", scene[90, 80], " rgb:", rgb[90, 80])
print("1-4 probe[0,0]:", probe[0, 0], " ← 原来是 [40 90 60]")

print("=== Part 2 ===")
print("2-1 gray:", gray.shape, gray.ndim)
print("2-2 equal:", np.array_equal(manual, gray),
      " 最大误差:", np.abs(manual.astype(int) - gray.astype(int)).max())
print("2-3 权重最大的是 0.587(G)")

print("=== Part 3 ===")
print("3-1 hsv:", hsv.shape, hsv.dtype, " H范围:", hsv[:, :, 0].min(), "~", hsv[:, :, 0].max())
print("3-2 黄心:", hsv[90, 220], " 红块:", hsv[90, 80], " 绿块:", hsv[190, 230])

print("=== Part 4 ===")
print("4-1 mask:", mask.shape, "ndim:", mask.ndim, "unique:", np.unique(mask))
print("4-2 黄色像素数:", int((mask > 0).sum()), " πr²=", 3.14159 * 45 * 45)
print("4-3 only_yellow:", only_yellow.shape,
      " 黄心:", only_yellow[90, 220], " 红块位置:", only_yellow[90, 80])

print("=== Part 5 ===")
print("5-1 b:", b.shape, b.ndim, " equal:", np.array_equal(b, scene[:, :, 0]))
print("5-2 merged equal:", np.array_equal(merged, scene))
print("5-3 wrong equal:", np.array_equal(wrong, scene), " wrong[90,80]:", wrong[90, 80])

print("=== Part 6 ===")
print("6-1 预期红色像素数:", (130 - 30 + 1) * (140 - 40 + 1))
