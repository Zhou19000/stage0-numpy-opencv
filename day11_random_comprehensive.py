"""
Day11 · 2.14 随机数与综合例题（例题 2-11 / 2-12 / 2-13 拆解版）

昨天你看例题觉得"一道都不会"——那是因为三题分别是：
  2-11 图像预处理函数（串：astype / 广播 / transpose / expand_dims / ascontiguousarray）
  2-12 向量化 IoU     （串：np.maximum / np.minimum / clip / 广播 / 视图规则）
  2-13 NMS            （串：argsort 倒序 / 循环 / 布尔索引）
看起来是新东西，其实是 2.1~2.13 的积木重新拼。

今天不让你"从零写函数"，而是先**拆成小步、每步写预测**，把每一步真的看懂，最后再拼成完整函数。
规则照旧：每个 print 前把"预测"写完（写不出打 ⚠️），全部写完后一次性运行对答案。

本文件结构：
  Part A  随机数基础（seed / rand / randn / randint / permutation / shuffle / choice）
  Part B  例题 2-11 拆解（图像预处理 7 小步）
  Part C  例题 2-12 拆解（向量化 IoU 6 小步）
  Part D  例题 2-13 拆解（NMS 思路填空）
  Part E  三道完整函数（抄写/自己写一遍，运行验证出题面给的答案）
"""
import numpy as np

# ============================================================
# Part A · 随机数基础
# ============================================================
# 记住：seed 写在随机调用之前，才能"锁死"后面出来的序列（跑两遍一模一样）。
np.random.seed(42)
print(np.round(np.random.rand(2, 3), 3))     # 预测:rand 出的是 [0,1) 均匀小数,维度是(2,3)，round是四舍五入到三位小数。
# ↑ rand 出的是 [0,1) 均匀小数，参数直接写维度 (2,3)

np.random.seed(42)
print(np.round(np.random.rand(2, 3), 3))     # 预测（和上一行比，一样吗？）:一样

print(np.random.rand())                      # 预测: 是标量还是数组？范围是多少？标量，[0,1)

# randn：标准正态 N(0,1)，有正有负，约 68% 落在 -1~1
np.random.seed(0)
a = np.random.randn(10000)
print(np.round(a.mean(), 2), np.round(a.std(), 2))   # 预测: 均值≈_0___ 标准差≈_1___

# randint：整数，[low, high) 左闭右开。你能看出下面的取值范围吗？
np.random.seed(0)
r = np.random.randint(0, 10, size=5)
print(r)                                     # 预测: 会出现 10 吗？_不会___ 范围是 __[0,10)__

# permutation：返回打乱后的**副本**（原数组不动）
p_arr = np.arange(5)
p_out = np.random.permutation(p_arr)
print(p_arr)                                 # 预测: 原数组变了吗？______没有______
print(p_out)                                 # 预测: 是 0~4 的某种排列吗？____是的________

# shuffle：**原地**打乱，返回 None  ← 经典坑
s_arr = np.arange(5)
s_ret = np.random.shuffle(s_arr)
print(s_arr)                                 # 预测: 原数组变了吗？___变了_________
print(s_ret)                                 # 预测: s_ret 是什么？_⚠️_None_________

# choice：从给定数组里抽，replace=False 表示不放回
np.random.seed(1)
print(np.random.choice(10, size=3, replace=False))   # 预测: 有重复吗？__没有重复__ 范围 _[0,10)___

# 形状对比：rand 吃分开的维度，random/randint 吃 size 元组
np.random.seed(2)
print(np.random.rand(2, 3).shape)            # 预测:____范围是[0,1)的小数，形状是(2,3)________
print(np.random.random((2, 3)).shape)        # 预测:_____范围是[0,1)的小数，形状是(2,3)_______
print(np.random.randint(0, 5, (2, 3)).shape) # 预测:____范围是[0,5)的整数，形状是(2,3)________


# ============================================================
# Part B · 例题 2-11 拆解：一步一行，看懂预处理
# ============================================================
# 目标：img(HWC,uint8,RGB)  →  (1,3,H,W) float32 按通道归一化 内存连续
# 为了好观察，这里用很小的图 (2,2,3)，原理和 (480,640,3) 完全一样。

img = np.array([[[10, 20, 30], [40, 50, 60]],
                [[70, 80, 90], [100, 110, 120]]], dtype=np.uint8)   # shape (2,2,3)
print(img.shape, img.dtype)                  # 预测:___(2,2,3)  uint8_______

# 步1：转 float32
x = img.astype(np.float32)
print(x.dtype)                               # 预测:__float32__________

# 步2：除以 255 归一化到 0~1（注意先转了 float32，避免整数除法）
x = x / 255.0
print(x[0, 0])                               # 预测: [10/255, 20/255, 30/255] ≈ ?__[0.039,0.078,0.118]__________

# 步3：按通道减均值除标准差（mean/std 是长度 3 的向量，靠**广播**作用到每通道）
mean = np.array([0.5, 0.5, 0.5], np.float32)
std = np.array([0.5, 0.5, 0.5], np.float32)
x = (x - mean) / std
print(x.shape)                               # 预测:___不会 还是(2,2,3)_________（广播会改 shape 吗？）

# 步4：HWC → CHW（动的是"看法"，第 2 章视图/transpose）
x = np.transpose(x, (2, 0, 1))
print(x.shape)                               # 预测:____(3,2,2)________
print(x.flags["C_CONTIGUOUS"])               # 预测:_____False_______（transpose 后连续吗？）

# 步5：加 batch 维（第 1 维）
x = np.expand_dims(x, axis=0)
print(x.shape)                               # 预测:___(1,3,2,2)_________

# 步6：保证内存连续
x = np.ascontiguousarray(x)
print(x.shape, x.flags["C_CONTIGUOUS"])      # 预测:___True_________


# ============================================================
# Part C · 例题 2-12 拆解：向量化 IoU
# ============================================================
# 框格式 [x1, y1, x2, y2]。iou = 交集面积 / 并集面积。
box = np.array([0, 0, 10, 10], dtype=np.float32)          # shape (4,)
boxes = np.array([[5, 5, 15, 15],
                  [0, 0, 10, 10],
                  [20, 20, 30, 30]], dtype=np.float32)     # shape (3,4)
print(box.shape, boxes.shape)                # 预测:___(4,)  (3,4)_________

# 步1：交集矩形的四条边
x1 = np.maximum(box[0], boxes[:, 0])
y1 = np.maximum(box[1], boxes[:, 1])
x2 = np.minimum(box[2], boxes[:, 2])
y2 = np.minimum(box[3], boxes[:, 3])
print(x1.shape)                              # 预测:______(3,)______（box[0] 标量 vs boxes[:,0] (3,)）
print(x1)                                    # 预测: [max(0,5), max(0,0), max(0,20)] = (5,0,20)____

# 步2：交集面积 = 宽 × 高，负的截成 0（不相交时宽高会是负）
inter_w = np.clip(x2 - x1, 0, None)
inter_h = np.clip(y2 - y1, 0, None)
inter = inter_w * inter_h
print(inter)                                 # 预测: [?, 100, 0] 第1个是多少？_[25,100,0]___

# 步3：各自面积
area_a = (box[2] - box[0]) * (box[3] - box[1])
area_b = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
print(area_a, area_b)                        # 预测: area_a=__100__ area_b=_(100,100,100)___

# 步4：并集 = 两个面积和 - 交集（交集被算了两次）
iou = inter / (area_a + area_b - inter)
print(np.round(iou, 3))                      # 预测: [?, 1.0, 0.0] 第一个约？__0.143__


# ============================================================
# Part D · 例题 2-13 拆解：NMS 思路
# ============================================================
# 不用写代码，先把思路用中文说清楚，然后回答下面问题：
#   ①按分数从高到低排序  ②取最高分的框保留  ③删掉与它 IoU>阈值 的框  ④重复
#
# 问1：order = np.argsort(scores)[::-1] 里，argsort 返回什么？[::-1] 起什么作用？
#     答：__argsort 返回是下标
#     ___[::-1] 返回的排序的从高到低___________________________________________
# 问2：为什么用 while 循环，而不是 for 循环？
#     答：____while循环可以比较多次，for是比较一个____________________________________________
# 问3：order[1:][ious <= iou_thr] 这一步在干嘛？（提示：布尔索引）
#     答：____[ious <= iou_thr]得到布尔索引，然后索引到order里第一行的对应值____________________________________________
#
# ↓ 用笔记里给的数据，预测最终 keep 的结果
nms_boxes = np.array([[10, 10, 100, 100],
                      [12, 12, 102, 98],
                      [200, 200, 300, 300],
                      [205, 195, 305, 298],
                      [500, 500, 550, 550]], dtype=np.float32)
nms_scores = np.array([0.9, 0.8, 0.75, 0.95, 0.6])
print(np.argsort(nms_scores)[::-1])          # 预测: 分数从高到低的下标 = ?__[3,0,1,2,4]__________
# 预测最终保留的下标:__[3,0,4]__________（哪几个框会被留下？）


# ============================================================
# Part E · 三道完整函数（照笔记参考答案自己敲一遍，运行验证）
# ============================================================
# 目标：跑出来 shape 是 (1,3,480,640)、dtype float32、连续=True、
#      三个通道均值约 [0.1 0.2 0.4]。先自己写，卡住了再回头看笔记。

def preprocess(img, mean, std):
    x=img.astype(np.float32)/255.0
    x = (x - np.asarray(mean, np.float32)) / np.asarray(std, np.float32)
    x = np.transpose(x, (2, 0, 1))
    x = np.expand_dims(x, axis=0)
    return np.ascontiguousarray(x)   #⚠️ 要变成连续的。




def iou_one_to_many(box, boxes):
    x1 = np.maximum(box[0], boxes[:, 0])  # 交集左边：取大
    y1 = np.maximum(box[1], boxes[:, 1])  # 交集上边：取大
    x2 = np.minimum(box[2], boxes[:, 2])  # 交集右边：取小
    y2 = np.minimum(box[3], boxes[:, 3])  # 交集下边：取小
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)  # 交集面积，负的截成 0
    area_a = (box[2] - box[0]) * (box[3] - box[1])  # box 自己的面积
    area_b = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])  # 每个框的面积（注意取列）
    return inter / (area_a + area_b - inter)  # 交 ÷ 并



def nms(boxes, scores, iou_thr=0.5):
    order = np.argsort(scores)[::-1]        # 分数从高到低的下标
    keep = []
    while order.size > 0:
        i = order[0]                        # 队首 = 当前最高分
        keep.append(int(i))                 # ① 保留它
        if order.size == 1:
            break
        ious = iou_one_to_many(boxes[i], boxes[order[1:]])  # ② 它 vs 剩下所有
        order = order[1:][ious <= iou_thr]  # ③ 只留下「不重叠」的当下一轮候选
    return keep


if __name__ == "__main__":
    # --- 验证 2-11 ---
    # np.random.seed(0)
    # big = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    # x = preprocess(big, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    # print(x.shape, x.dtype, x.flags["C_CONTIGUOUS"])
    # print(np.round(x.mean(axis=(0, 2, 3)), 1))

    # --- 验证 2-12 ---
    # print(np.round(iou_one_to_many(box, boxes), 3))

    # --- 验证 2-13 ---
    # print(nms(nms_boxes, nms_scores, 0.5))
    pass
