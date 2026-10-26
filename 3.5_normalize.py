import cv2
import numpy as np

# ========== 造图：一张被"压扁"的低对比度渐变图 ==========
# 原本 0~255 的横向渐变，被压到 60~200 —— 对比度只剩一半，是拉伸的理想实验对象
grad = np.linspace(0, 255, 256, dtype=np.float32)
low_u8 = np.tile(grad * (140 / 255) + 60, (100, 1)).astype(np.uint8)

print('== Part 1: /255 归一化 ==')
a = low_u8.astype(np.float32) / 255
b = low_u8 / 255
print(a.dtype, b.dtype)              # 预测1: 两个 dtype 分别是？a.dtype是float32。b.dtype是float64
                                     # 为什么不同？ 代码不一样，a里面写了np.float32,b没写就按默认走。
print(a.min(), a.max())              # 预测2: a 的最小、最大（约多少？）  0.235， 0.784

print('== Part 2: normalize 拉伸到 0~255 ==')
st = cv2.normalize(low_u8, None, 0, 255, cv2.NORM_MINMAX)
print(st.dtype, st.min(), st.max())  # 预测3: dtype 是？uint8。两端是多少？0和255
print(np.array_equal(low_u8, st))    # 预测4: True 还是 False？为什么？False 。两者的值不一样了

print('== Part 3: 手写 min-max 拉伸（本节手写函数） ==')
def stretch(img):
    """把 img 的 min/max 拉到 0/255，返回 uint8。"""
    lo, hi = img.min(), img.max()
    out =((img.astype(np.float32) -lo) /(hi-lo) )*255# 空1: 一行公式——转 float32、减 lo、除 (hi-lo)、乘 255
    return out.astype(np.uint8)  # 空2: 转回什么类型才能当图像用？

mine = stretch(low_u8)
diff = np.abs(mine.astype(np.int16) - st.astype(np.int16)).max()
print('diff =', diff)                # 预测5: 手写版和 cv2 版最大差多少？1

print('== Part 4: 0~1 的坑（复现上午的实验） ==')
bad = cv2.normalize(low_u8, None, 0, 1, cv2.NORM_MINMAX)
good = cv2.normalize(low_u8, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
print(bad.dtype, np.unique(bad))     # 预测6: dtype？uint8。unique 出来几个值？2个值
print(good.dtype, good.min(), good.max())  # 预测7: dtype？float32。两端真是精确的 0 和 1 吗？不是，有浮点误差
