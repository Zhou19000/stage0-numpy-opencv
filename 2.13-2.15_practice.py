# 建一个 3 行 4 列的全 0 数组
import numpy as np
img=np.zeros((3,4),np.uint8)
# 生成 0 到 9 的整数序列
a=np.arange(0,10,1)
# ⚠️把数组转成 float32
img1=img.astype(np.float32)
# 看这个数组一共有多少个元素
print(img1.size)
# 取 第 2~3 行、第 1~2 列 那一块
print(img1[1:3,0:2])
# 给数组加一个维度（放在最前面）
img2=np.expand_dims(img1,axis=0)
print(img2.shape)
# 去掉长度为 1 的那个维度（axis=0）
img3=np.squeeze(img2)
print(img3.shape)
# 把 HWC 换成 CHW（按 (2, 0, 1) 重排）
img4=np.zeros((3,4,3),np.uint8)
img5=np.transpose(img4,(2,0,1))
# 沿 axis=1 求平均值
print(np.mean(img5,axis=1))
# 找出最大值所在的下标
print(np.argmax(img5))

# 第 2 章收口自测
# 1｜图像 shape
# 一张 480 行 × 640 列的彩色图，shape 是(480,640,3)
# 像素 (行 100, 列 200) 的 B 通道怎么写？img[100,200,0]
#
# 2｜uint8 溢出
#np.array([200], dtype=np.uint8) + np.array([100], dtype=np.uint8)
# ⚠️结果是多少？为什么？
#44。因为uint8的最大取到255【是256个数】，100+200-256=44。
# 3｜归一化标准写法
# 把一张 uint8 图压到 0~1，标准的一行怎么写？（提示：防什么坑） 忘了
# ⚠️img.astype(np.float32) / 255.0
# 4｜reshape vs transpose
# 把 (2,3) 变成 (3,2)：
#x.reshape(3,2)
# x.reshape(3,2) 和 x.T 得到的内容一样吗？不一样
# 分别是什么？（随便举个数说清区别）x.reshape(3,2)是按照顺序重新分行， x.T是直接转置。
# 5｜squeeze
# x.shape = (1,3,1,5)，执行 np.squeeze(x, axis=0) 后 shape 是？
#(3,1,5)
# 6｜广播
# (3,1) 和 (1,4) 相加，结果 shape 是？
#(3,4)
# 7｜axis 压缩
# x.shape = (2,3,4)，x.sum(axis=1) 的结果 shape 是？
#⚠️(2,4)。axis=1 = 把第 1 维（长度 3）压掉，剩下 (2, 4) 按原顺序保留。
# 8｜concat vs stack
# 两个 (2,3) 数组：
#
# np.concatenate([a,b], axis=0) → shape？(4,3)
# np.stack([a,b], axis=0) → shape？⚠️(2,2,3)
# 9｜视图还是拷贝
# a[a > 0] 和 a[1:3]，哪个是拷贝、哪个是视图？
#a[a > 0]是拷贝  a[1:3]是视图
# 10｜送推理引擎前
# transpose 之后的数组能直接喂给推理引擎吗？不能的话要加什么？
# 不能 要np.ascontiguousarray