"""
Day10 · 2.13 视图 vs 拷贝，与内存连续性
昨天彩蛋题那个"a 为什么没变"的答案，就在今天。
两个概念先记牢：
  视图(view)：和原数组**共用同一块内存**，改一个另一个也变。（切片、transpose、reshape 都是视图）
  拷贝(copy)：有自己**独立的内存**，互不影响。（布尔索引、花式索引、astype、copy() 都是拷贝）
内存连续性：数组在内存里是"一行接一行"整块摆的（C 连续）。
  transpose 只改"看的方式"、不搬数据 → 结果**不连续**。
  很多底层库（推理引擎 / OpenCV / C++ 交互）要求输入连续 → 用 np.ascontiguousarray(...) 重排。
规则还是一样：每个 print 后面先把"预测"写完（写不出打 ⚠️），再整体运行对答案。
判断口诀：**改一改，看原数组变没变。**
"""
import numpy as np

# ============ 第一部分：视图 vs 拷贝 认脸 ============
a = np.arange(6)                 # [0 1 2 3 4 5]
b = a[1:4]                       # 基本切片
b[0] = 100
print(a)                         # 预测:[0,100,2,3,4,5]  (a 变了吗？b 是视图还是拷贝？)

c = a[1:4].copy()                # 显式拷贝
c[0] = -1
print(a)                         # 预测: [0,100,2,3,4,5]  (这次 a 变了吗？) 不变
print(np.shares_memory(a, b))    # 预测: True (共不共用内存？)
print(np.shares_memory(a, c))    # 预测:  False

# ============ 第二部分：哪种取法是视图？（改一改，看原数组）============
# ---- 2-1 基本切片 ----
a1 = np.arange(10)
v1 = a1[2:5]
v1[0] = -1
print(a1)                        # 预测:[0,1,-1,3,4,5,6,7,8,9]

# ---- 2-2 反向切片 ----
a2 = np.arange(10)
v2 = a2[::-1]
v2[0] = -1
print(a2)                        # 预测: ⚠️[ 0  1  2  3  4  5  6  7  8 -1] (-1 会落在 a2 的哪一号位置？)

# ---- 2-3 花式索引（下标列表）----
a3 = np.arange(10)
v3 = a3[[1, 3, 5]]
v3[0] = -1
print(a3)                        # 预测: ⚠️[0,1,2,3,4,5,6,7,8,9]  花式索引是拷贝

# ---- 2-4 布尔索引 ----
a4 = np.arange(10)
v4 = a4[a4 > 6]
v4[0] = -1
print(a4)                        # 预测:⚠️[0,1,2,3,4,5,6,7,8,9]  布尔索引是拷贝

# ---- 2-5 np.clip ----
a5 = np.arange(10)
v5 = np.clip(a5, 3, 7)
v5[0] = -1
print(a5)                        # 预测:[0,1,2,3,4,5,6,7,8,9]
print(v5)                        # 预测: [-1  3  3  3  4  5  6  7  7  7] (v5 自己变成什么了？)

# ---- 2-6 astype ----
a6 = np.arange(5)
v6 = a6.astype(np.float32)
v6[0] = -1
print(a6)                        # 预测:[0,1,2,3,4]

# ============ 第三部分：图像场景（这才是真会踩的坑）============
img = np.zeros((4, 5, 3), dtype=np.uint8)
roi = img[1:3, 1:4]              # 切片 → 视图
roi[:] = 255                     # 整块涂白
print(img[1, 1])                 # 预测: [255,255,255] (原图那个位置被涂白了吗？)
print(img[0, 0])                 # 预测: [0,0,0] (没裁到的位置呢？)
print(np.shares_memory(img, roi))  # 预测:True

img2 = np.zeros((4, 5, 3), dtype=np.uint8)
roi2 = img2[1:3, 1:4].copy()     # 加了 .copy()
roi2[:] = 255
print(img2.max())                # 预测: 0 (原图最大像素值是多少？)
# 反向题：从大图裁出一块 ROI，要给它画框、调亮度，但原图还要留着做对比图 —— 该怎么写？
# 答：roi=img[1:3, 1:4].copy()

# ============ 第四部分：内存连续性 ============
x = np.arange(6).reshape(2, 3)
print(x.flags["C_CONTIGUOUS"])                        # 预测:True
xt = x.T                                              # 转置
print(xt.flags["C_CONTIGUOUS"])                       # 预测:False
print(np.shares_memory(x, xt))                        # 预测:  True (转置是视图还是拷贝？) 视图
print(np.ascontiguousarray(xt).flags["C_CONTIGUOUS"])  # 预测: True
print(np.shares_memory(xt, np.ascontiguousarray(xt)))  # 预测:⚠️ False
# (这次重新排，有没有搬数据？)原来xt是视图内存没动，只改变读取方式。
# np.ascontiguousarray(xt) 内存动了，变成按行读取的了。所以是False
img3 = np.zeros((4, 5, 3), dtype=np.float32)          # HWC
chw = np.transpose(img3, (2, 0, 1))                   # 换成 CHW
print(chw.shape, chw.flags["C_CONTIGUOUS"])           # 预测:(3,4,5)  False
print(np.ascontiguousarray(chw).flags["C_CONTIGUOUS"])  # 预测: True

# ============ 例题 2-10（作业，自己写）============
# 不运行代码，先预测下面每一步之后 a 的内容，再运行验证。
#   a = np.arange(5)      → 预测 a: [0,1,2,3,4]
#   b = a[:3]             → b 是视图还是拷贝？ 视图
#   b[0] = 99             → 预测 a: [99,1,2,3,4]
#   c = a[a > 2]          → c 是视图还是拷贝？ 拷贝
#   c[0] = -1             → 预测 a: [99,1,2,3,4]
#   最后 a 是什么？       a还是[99,1,2,3,4]
#
# 在下面写你的代码（记得打印 a 以及 shares_memory）：

a = np.arange(5)
b = a[:3]
b[0] = 99
print(a)
c = a[a > 2]
c[0] = -1
print(a)
print(np.shares_memory(a,b))