"""
3.8 滤波：平滑与去噪
================================================
本节四个函数：
    cv2.blur              均值滤波（邻域取平均）
    cv2.GaussianBlur      高斯滤波（按距离加权）
    cv2.medianBlur        中值滤波（取中位数，专治椒盐）
    cv2.bilateralFilter   双边滤波（去噪保边）

三个量化指标（贯穿全文）：
    平坦区 std   = 残留噪声有多少（越小越干净）
    边缘过渡带   = 边缘被糊掉多少列（0 = 完全没糊）
    耗时 ms      = 谁慢

规则：每处 "预测:" 后面先把答案写进注释，全部写完再一次性运行。
"""
import cv2
import numpy as np
import time

# ========== 造图：有内容、有硬边的一张图 ==========
# 底 120，中间一个亮方块 200，右边一条斜边三角形 60 —— 三种灰度、三种边界
base = np.full((300, 300), 120, np.uint8)
base[60:140, 40:120] = 200                      # 亮方块（四条硬边）
tri = np.array([[300, 180], [300, 300], [180, 300]], np.int32)
cv2.fillPoly(base, [tri], 60)                   # 右下斜边三角（斜边最能看出糊）
clean = base.copy()                             # 无噪声的干净版，用来对比

# 两种噪声
np.random.seed(7)
gauss_noise = np.random.normal(0, 12, base.shape).astype(np.int16)
noisy_g = np.clip(base.astype(np.int16) + gauss_noise, 0, 255).astype(np.uint8)  # 高斯噪声

noisy_sp = base.copy()                          # 椒盐噪声：1% 像素随机变 0 或 255
mask = np.random.rand(*base.shape) < 0.01
noisy_sp[mask] = np.random.choice([0, 255], mask.sum())
noisy_sp = noisy_sp.astype(np.uint8)

FLAT = (slice(200, 280), slice(20, 100))        # 平坦区（无边缘），用来量噪声残留
def flat_std(x):
    return round(float(x[FLAT].std()), 2)

def edge_width(x, lo=135, hi=185):
    """过渡带宽度：先对行 70~130（方块内部，无上下边）按列求平均，把随机噪声压掉，
       再数有多少列的均值落在 120 和 200 之间 —— 干净图应为 0，糊了才会 >0。"""
    prof = x[70:130, :].mean(axis=0)
    return int(((prof > lo) & (prof < hi)).sum())

print("原图:", base.shape, base.dtype, " 干净平坦区 std =", flat_std(clean))
print("高斯噪声 std =", flat_std(noisy_g), " 椒盐噪声 std =", flat_std(noisy_sp))


print("\n== Part 1: blur 均值 vs GaussianBlur 高斯 ==")
b5 = cv2.blur(noisy_g, (5, 5))
g5 = cv2.GaussianBlur(noisy_g, (5, 5), 0)
b9 = cv2.blur(noisy_g, (9, 9))
# 预测1: b5.shape / b5.dtype 是？（跟原图比）b5.shape=(300,300),b5.dtype是np.uint8
print("b5:", b5.shape, b5.dtype)
# 预测2: 平坦区 std：b5 和 g5 谁更小？（提示：两者对平坦区的处理差异大吗）b5更小吧，但是两者处理差异不大。
print("平坦区 std  b5 =", flat_std(b5), "  g5 =", flat_std(g5))
# 预测3: 边缘过渡带宽度：b5(5x5) 和 b9(9x9) 谁更宽？b9(9x9)更宽
print("过渡带  b5 =", edge_width(b5), "  b9 =", edge_width(b9), "  干净图 =", edge_width(clean))
# 预测4: cv2.GaussianBlur(noisy_g, (4, 4), 0) —— ksize 是偶数，能跑吗？不能，必须得是正奇数
try:
    g4 = cv2.GaussianBlur(noisy_g, (4, 4), 0)
    print("(4,4) 跑通了", g4.shape)
except cv2.error as e:
    m = str(e)
    print("(4,4) 报错:", m[m.find("error:"):][:70])


print("\n== Part 2: medianBlur 中值（专治椒盐）==")
# 预测5: ksize 参数写法是 (5,5) 还是 5？是5
m5_sp = cv2.medianBlur(noisy_sp, 5)
b5_sp = cv2.blur(noisy_sp, (5, 5))
# 预测6: 椒盐图上 medianBlur(5) 之后，平坦区 std 接近 0 还是接近原噪声 std？更接近于0
print("椒盐图  原始 std =", flat_std(noisy_sp))
print("  median5 后 std =", flat_std(m5_sp))
# 预测7: 同一张椒盐图，b5(均值) 的 flat std 比 median 大还是小？大
print("  blur5   后 std =", flat_std(b5_sp))
# 边缘：中值会不会把斜边糊掉 。  不会
m5_g = cv2.medianBlur(noisy_g, 5)
print("过渡带  median5 =", edge_width(m5_g), "  blur5 =", edge_width(b5), "  干净图 =", edge_width(clean))


print("\n== Part 3: bilateralFilter 双边（去噪保边）==")
# 预测8: 双边的边缘过渡带比 GaussianBlur(9,9) 宽还是窄？窄
bl = cv2.bilateralFilter(noisy_g, 9, 75, 75)
g9 = cv2.GaussianBlur(noisy_g, (9, 9), 0)
print("过渡带  双边(9,75,75) =", edge_width(bl), "  高斯(9,9) =", edge_width(g9))
print("平坦区 std  双边 =", flat_std(bl), "  高斯9 =", flat_std(g9))
# 预测9: sigmaColor 从 75 调到 200，过渡带会变宽还是变窄？变宽
bl200 = cv2.bilateralFilter(noisy_g, 9, 200, 75)
print("过渡带  双边 sigmaColor=200 =", edge_width(bl200))
# 预测10: 16 位整型图能跑双边吗？不能，是8位或者32位浮点数
try:
    cv2.bilateralFilter(noisy_g.astype(np.uint16), 9, 75, 75)
    print("uint16 跑通了")
except cv2.error as e:
    m = str(e)
    print("uint16 报错:", m[m.find("error:"):][:70])


print("\n== Part 4: 四种滤波综合对比（耗时）==")
big = np.random.randint(0, 255, (512, 512), np.uint8)
def cost(f, n=10):
    s = time.perf_counter()
    for _ in range(n):
        f()
    return round((time.perf_counter() - s) / n * 1000, 2)

# 预测11: 处理椒盐噪声，四种里哪个效果最好？（看 Part 2 的 std） 中值滤波
# 预测12: 四种里哪个最慢？（9x9，思考"排序"和"乘法"哪个更贵） 中值滤波。排序更贵
print("blur      ms:", cost(lambda: cv2.blur(big, (9, 9))))
print("gauss     ms:", cost(lambda: cv2.GaussianBlur(big, (9, 9), 0)))
print("median    ms:", cost(lambda: cv2.medianBlur(big, 9)))
print("bilateral ms:", cost(lambda: cv2.bilateralFilter(big, 9, 50, 9)))
