"""
Day7 · 2.10 argmax / argmin / argsort

规则：每个 print 后面的"预测"先自己写完，再运行对答案。
预测错了比蒙对更有价值 —— 错的那条就是今天的薄弱点。
"""
import numpy as np

# ============ 第一部分：一维，先认脸 ============
probs = np.array([0.1, 0.7, 0.2])

print(np.argmax(probs))            # 预测: 1
print(np.argmin(probs))            # 预测: 0
print(np.argsort(probs))           # 预测: (0,2,1)
print(np.argmax(probs).dtype)      # 预测:int64

scores = np.array([0.3, 0.9, 0.1, 0.7])

print(np.argsort(scores))          # 预测:[2,0,3,1]
print(np.argsort(scores)[::-1])    # 预测: [1,3,0,2]
print(scores[np.argsort(scores)[::-1]])   # 预测: [0.9,0.7,0.3,0.1]
print(np.argsort(scores)[::-1][:2])       # 预测:[1,3]

# ============ 第二部分：二维 + axis ============
logits = np.array([[0.1, 0.7, 0.2],
                   [0.6, 0.1, 0.3]])          # 2 个样本, 3 个类别

print(np.argmax(logits, axis=0))   # 预测:[1,0,1]
print(np.argmax(logits, axis=1))   # 预测:[1,0]
print(np.argmax(logits, axis=1).shape)              # 预测:(2,)
print(np.argmax(logits, axis=1, keepdims=True).shape)   # 预测: (2,1)
print(logits.max(axis=1))                            # 预测:[0.7,0.6]

# ============ 第三部分：三个易错点 ============
m = np.array([[1, 9],
              [7, 2]])

print(np.argmax(m))                # 预测:⚠️1
r, c = np.unravel_index(np.argmax(m), m.shape)
print(int(r), int(c))              # 预测:  ⚠️ 0 1
print(np.argsort(m, axis=1))       # 预测: ⚠️ [0,1],[1,0]
print(np.argsort(m, axis=1).shape) # 预测: ⚠️(2,2)

ties = np.array([3, 3, 1])
print(np.argmax(ties))             # 预测: 0

# ============ 例题 2-7（作业，不要抄答案）============
# 实现 softmax(x, axis=-1) 并取 Top-3
# logits (2,5): [[2.0, 1.0, 0.1, 3.0, 0.5],
#                [0.2, 0.2, 4.0, 1.0, 0.0]]
# ① softmax 变概率（每行和 = 1，用 keepdims=True 广播）
# ② 每个样本的预测类别   【预测类别 = 这 5 个数里最大的那个数排在第几号。】
# ③ 每个样本概率最高的 3 个类别下标（从高到低）

def softmax(x, axis=-1):
     # TODO: 三段式 —— 减最大值、取 exp、除以 sum(keepdims=True)
    shifted=x-x.max(axis=axis, keepdims=True)
    e=np.exp(shifted)
    probs=e/e.sum(axis=axis, keepdims=True)
    return probs

logits =np.array([[2.0, 1.0, 0.1, 3.0, 0.5],
                 [0.2, 0.2, 4.0, 1.0, 0.0]])
p=softmax(logits)
#1\
print(np.round(p,3))
#2\
print(np.argmax(p,axis=1))
#3\
print(np.argsort(p,axis=1)[:,::-1][:,:3])


# ---------------- 验证代码（不是答案，是"评分标准"）----------------
# 你要写的只有上面 softmax 函数体里的三行。
# 下面这 6 行是调用 + 自测用的：写完函数后把 # 号去掉，运行，
# 输出和笔记例题 2-7 的"运行结果"一模一样就算过关。

# logits = np.array([[2.0, 1.0, 0.1, 3.0, 0.5],
#                    [0.2, 0.2, 4.0, 1.0, 0.0]])
# p = softmax(logits)
# print(np.round(p, 3))
# print(p.sum(axis=1))
# print(np.argmax(p, axis=1))
# print(np.argsort(p, axis=1)[:, ::-1][:, :3])
