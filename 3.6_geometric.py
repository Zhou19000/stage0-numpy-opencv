"""
3.6 几何变换：翻转、平移、旋转、透视
================================================
本节五个函数（卡片都讲过，忘了就翻 opencv-cheatsheet.md）：
    cv2.flip(src, flipCode)                       翻转
    cv2.getRotationMatrix2D(center, angle, scale) 造 2×3 旋转矩阵（不动图！）
    cv2.warpAffine(src, M, dsize)                 仿射变换总闸门
    cv2.getPerspectiveTransform(src, dst)         造 3×3 透视矩阵（不动图！）
    cv2.warpPerspective(src, M, dsize)            透视变换

铁律三条（今天就考这三条）：
    1. dsize 一律 (宽, 高)  —— 只有 shape 是 (高, 宽)
    2. center 是 (x, y)     —— (列, 行)，又是反的
    3. 透视图点顺序 左上 → 右上 → 右下 → 左下（顺时针）

规则：每处 "预测:" 后面先把答案写进注释，全部写完再一次性运行。
     预测错才有价值，别蒙。
"""
import cv2
import numpy as np

# ========== 造图：一张"不对称"的图 ==========
# 只有不对称的图，才看得出翻转到底往哪边翻
img = np.full((100, 200, 3), 40, np.uint8)     # 深灰底，高 100 宽 200
img[10:30, 10:50] = (0, 0, 255)                # 左上角一块红
img[70:90, 150:190] = (0, 255, 0)              # 右下角一块绿

print("原图 shape:", img.shape, " img[20,180] =", img[20, 180])
# 记住这两个定位点：红块在 [10:30, 10:50]，绿块在 [70:90, 150:190]，其余是灰 40


print("\n== Part 1: flip 翻转 ==")
f1 = cv2.flip(img, 1)      # 左右翻
f0 = cv2.flip(img, 0)      # 上下翻
fm = cv2.flip(img, -1)     # 同时翻

# 提问：我们挑一个"三种翻转答案都不同"的点 (20, 180)
#      换算公式：f1[r,c] = img[r, 199-c]；f0[r,c] = img[99-r, c]；fm = 两者都换
print("f1[20,180]:", f1[20, 180])   # 预测1: 红/绿/灰 哪一个？f1[20,19] 红色
print("f0[20,180]:", f0[20, 180])   # 预测2: 红/绿/灰 哪一个？f0[79,180] 绿色
print("fm[20,180]:", fm[20, 180])   # 预测3: 红/绿/灰 哪一个？fm[79,19] 灰色
# 预测4: 三个翻转后 shape 变不变？写 (100,200,3) 或 (200,100,3) 或 (100,200) 或 其他
print("shape:", f1.shape, f0.shape, fm.shape)   #不变 都是(100,200,3)


print("\n== Part 2: 平移（手拼矩阵） ==")
# 平移矩阵 = [[1, 0, dx], [0, 1, dy]]，读法：第一列管 x、第二列管 y、第三列是平移量
M = np.float32([[1, 0, 50], [0, 1, 30]])   # 右移 50、下移 30
sh = cv2.warpAffine(img, M, (200, 100))    # dsize = (宽, 高) = (200, 100)

# 预测5: sh.shape = (100,200,3)
# 预测6: sh[40,60] = ？（提示：红块左上角原在 (行10, 列10)，右移 50、下移 30 后落在哪）img[10,10] 是红色矩形的左上角点(0,0,255)
# 预测7: sh[20,10] = ？（提示：这个位置原图有东西，但移走后谁填进来？warpAffine 默认填什么颜色）img[-10,-40] 是黑色。(0,0,0)
print(sh.shape)
print("sh[40,60]:", sh[40, 60])
print("sh[20,10]:", sh[20, 10])

# ⚠ 重点考：dsize 写反会怎样（同样的 M，同样的图，只是两个数换了位置）
sh2 = cv2.warpAffine(img, M, (100, 200))   # dsize 写成 (100, 200) —— 反了
# 预测8: sh2.shape = ？（想清楚 (100,200) 是 (宽,高) 还是 (高,宽)）⚠️【忘记写通道了】 (200,100,3),(100,200) 是 (宽,高)
# 预测9: sh2[40,80] = ？ sh2 宽只有 100，红块移到列 60~99，还在界内吗？ 在界内 红色
print(sh2.shape)
print("sh2[40,80]:", sh2[40, 80])


print("\n== Part 3: 旋转 ==")
# 换一张正方形图，绕中心转，好算
sq = np.full((200, 200, 3), 40, np.uint8)      # 灰底（注意：不是黑，好和"界外空洞"区分）
sq[20:60, 20:60] = (0, 0, 255)                 # 左上角一块红

M90 = cv2.getRotationMatrix2D((100, 100), 90, 1.0)   # 绕 (x=100, y=100) 逆时针 90°，不缩放
# 预测10: M90.shape 和 M90.dtype 分别是？⚠️(2, 3) / float64   （shape 像 (2,3) 这样写；dtype 只写类型名）
print(M90.shape, M90.dtype)

r90 = cv2.warpAffine(sq, M90, (200, 200))
# 预测11: r90[160,40] = ？（提示：屏幕上逆时针 90°，左上角跑到哪个角？红块会跟着去）红色(0,0,255)
# 预测12: r90[40,40] = ？（那块红已经走了，这里露出的是背景灰，还是界外黑？） 灰色 (40,40,40)
print("r90[160,40]:", r90[160, 40])
print("r90[40,40]:", r90[40, 40])

# 再转 30°，故意让四个角露出来
M30 = cv2.getRotationMatrix2D((100, 100), 30, 1.0)
r30 = cv2.warpAffine(sq, M30, (200, 200))
# 预测13: r30[0,0] = 灰 [40 40 40] 还是 黑 [0 0 0]？（提示：转 30° 后左上角这块地方，黑色(0,0,0)
#        原图里对应得着吗？对应不着就是"界外"，界外填 borderValue，默认是 0）原图里没有对应的点，是界外，borderValue
print("r30[0,0]:", r30[0, 0], " r30[100,100]:", r30[100, 100])


print("\n== Part 4: 透视（四点校正） ==")
# 造一张"拍歪的白纸"：深灰桌面上放一个歪四边形
# 注意：cv2.fillPoly 只是造图工具，本节不考它
paper = np.full((300, 300, 3), 40, np.uint8)
pts = np.array([[60, 40], [240, 80], [220, 270], [40, 230]], np.int32)  # 左上→右上→右下→左下
cv2.fillPoly(paper, [pts], (255, 255, 255))

src = pts.astype(np.float32)                       # 原图里那四个歪角（必须 float32！）
dst = np.float32([[0, 0], [200, 0], [200, 300], [0, 300]])   # 想掰成 200×300 的正矩形
Mp = cv2.getPerspectiveTransform(src, dst)

# 预测14: Mp.shape 和 Mp.dtype 分别是？（仿射是 2×3，透视是多少？）⚠️(3, 3) / float64
print(Mp.shape, Mp.dtype)

w = cv2.warpPerspective(paper, Mp, (200, 300))
# 预测15: w.shape = ？（dsize 是 (200, 300)，那 shape 呢） shape是(300,200,3)
print(w.shape)

# 预测16: 掰正成功的话，这张 200×300 的图里应该几乎全是白的。估个白像素比例：
#         w 里白像素占比约是 0% / 50% / 99% ？ 是99%
white = int(((w == 255).all(axis=2)).sum())
print("白像素:", white, "/", w.shape[0] * w.shape[1])

# ⚠ 再来一次，故意把前两个点的顺序调换（左上↔右上），看会发生什么
bad = np.float32([[240, 80], [60, 40], [220, 270], [40, 230]])
Mb = cv2.getPerspectiveTransform(bad, dst)
wb = cv2.warpPerspective(paper, Mb, (200, 300))
white_bad = int(((wb == 255).all(axis=2)).sum())
# 预测17: white_bad 会比 white 大还是小得多？（提示：点对错了，纸会被拧成什么样）会小很多 因为拧劲了。
print("顺序乱了的白像素:", white_bad)


print("\n== Part 5: 手写 rotate_keep（旋转不裁边） ==")
# 问题：warpAffine 的 dsize 沿用原尺寸，转 45° 后四个角必被裁掉。
# 解法：先把画布放大到"刚好装下旋转后的图"，再让中心对齐。
def rotate_keep(img_in, angle):
    """绕中心旋转，画布自动放大，保证不裁边。"""
    h, w = img_in.shape[:2]
    cx, cy = w / 2, h / 2
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)

    # 空1: 新画布宽、高各是多少？
    #      提示：旋转后包围盒 = |h·sin| + |w·cos|（宽） 和 |h·cos| + |w·sin|（高）
    #      注意得用 abs()，因为负角度的 sin 是负数
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh =int(cos*w+h*sin), int(cos*h+w*sin )  #⚠️

    # 空2: 画布变大后，图会偏到左上角，得把中心挪回新画布正中。
    #      M 的第三列就是平移量，直接加：
    M[0, 2] += nw / 2 - cx
    M[1, 2] += nh / 2 - cy

    # 空3: warpAffine 的 dsize 传什么？(宽, 高)
    return cv2.warpAffine(img_in, M,(nw,nh))


out45 = rotate_keep(img, 45)
# 预测18: out45.shape = ？（img 是 100×200，转 45° 后画布要多大？口算：0.707 左右）⚠️(212, 212, 3)
# 预测19: rotate_keep(img, 0) 的 shape = ？（不转的时候应该退化成原尺寸，这是最好的自检）(100,200,3)
print("rotate_keep(45):", out45.shape)
print("rotate_keep(90):", rotate_keep(img, 90).shape)
print("rotate_keep(0) :", rotate_keep(img, 0).shape)
