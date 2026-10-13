"""
Day8 · 2.11 concatenate / stack / split

规则还是一样：每个 print 后面的"预测"先自己写完，再运行对答案。
今天全场只有一个核心问题 —— **concatenate 和 stack 到底差在哪**。
答案藏在"结果的 shape 是几维"里，不在具体怎么拼。
"""
import numpy as np

# ============ 第一部分：二维基础，先认脸 ============
a = np.array([[1, 2],
              [3, 4]])
b = np.array([[5, 6],
              [7, 8]])

print(np.concatenate((a, b), axis=0).shape)     # 预测:(4,2)
print(np.concatenate((a, b), axis=1).shape)     # 预测:(2,4)
print(np.concatenate((a, b), axis=0))           # 预测:[[1,2],[3,4],[5,6],[7,8]
print(np.stack((a, b)).shape)                   # 预测:(2,2,2)
print(np.stack((a, b), axis=0)[0])              # 预测:[[1,2],[3,4]]
print(np.stack((a, b), axis=1)[0])              # 预测:[[1,2],[5,6]]
print(np.stack((a, b), axis=-1).shape)          # 预测:(2,2,2)
print(np.stack((a, b), axis=-1)[0, 0])          # 预测:⚠️[1 5]
print(np.vstack((a, b)).shape)                  # 预测:(4,2)
print(np.hstack((a, b)).shape)                  # 预测:(2,4)

parts = np.split(np.arange(6), 3)
print(parts)                                    # 预测:[0,1],[2,3],[4,5]
print(type(parts))                              # 预测:⚠️list
print(parts[1])                                 # 预测:[2,3]

# ============ 第二部分：图像场景（三维）============
i1 = np.zeros((4, 6, 3), dtype=np.uint8)        # 全黑图
i2 = np.full((4, 6, 3), 100, dtype=np.uint8)    # 灰图
i3 = np.full((4, 6, 3), 200, dtype=np.uint8)    # 亮图

print(np.stack([i1, i2, i3], axis=0).shape)         # 预测:(3,4,6,3)
print(np.concatenate([i1, i2, i3], axis=1).shape)   # 预测:(4,18,3)
print(np.concatenate([i1, i2, i3], axis=-1).shape)  # 预测:(4,6,9)
print(np.stack([i1, i2, i3], axis=-1).shape)        # 预测:(4,6,3,3)

# ============ 第三部分：易错点（先预测"会不会报错"）============
# 提示：这几行单独试，一个报错会中断后面。先写下预测，再一行一行取消注释运行。
x = np.ones((2, 2))
y = np.ones((3, 2))

# print(np.concatenate((x, y), axis=1).shape)   # 预测: 会 报错，原因：第0维不一样
# print(np.concatenate((x, y), axis=0).shape)   # 预测:不报错 (5,2)
# print(np.stack((x, y)).shape)                 # 预测: 会 报错，原因：x和y的shape不一样
# print(np.split(np.arange(7), 3))              # 预测: 会 报错，原因：7个数无法均等分成三份，输出还得是int64


# ============ 例题 2-8（作业，自己写）============
# 有 3 张 (4, 6, 3) 的小图：i1 全 0、i2 全 100、i3 全 200（上面已建好）
# ① 把 3 张图堆成 shape (3, 4, 6, 3) 的 batch
# ② 把 3 张图左右并排拼成一张 (4, 18, 3) 的对比图
# ③ 打印 wide[0, ::6, 0]，用来验证"每 6 列正好是下一张图"，应输出 [0 100 200]
#
# 先问自己：① 要新增一个维度吗？→ 用谁
#             ② 只是在已有的"宽度"维上相接吗？→ 用谁，axis 填几（0=高 1=宽 2=通道）

# 在下面写你的代码：
batch=np.stack((i1,i2,i3),axis=0)
print(batch.shape)
duibitu=np.concatenate((i1,i2,i3),axis=1)
print(duibitu.shape)
print(duibitu[0, ::6, 0])