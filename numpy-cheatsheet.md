# NumPy 速查表（阶段 0 · 2.1~2.14）

> **用法**：忘了就查，**不要用来背**。真正记住靠"**盖住右侧，默写左边**"（主动回忆）。
> **心法**：先想"我要干嘛"，再去右列找函数——按任务查，不是按字母查。

---

## 0. 起手式
```python
import numpy as np
```

## 1. 创建数组

| 我要干嘛 | 写法 | 备注 |
| --- | --- | --- |
| 从列表建 | `np.array([1,2,3])` | 可加 `dtype=` |
| 0 / 1 填充 | `np.zeros((H,W,3))` / `np.ones((2,3))` | 形状用**元组** |
| 等差序列 | `np.arange(0, 10, 2)` | `[start, stop)` **左闭右开** |
| 等分序列 | `np.linspace(0, 1, 5)` | 含终点，分 5 个数 |
| 全常量填充 | `np.full((2,3), 7)` | |
| 单位矩阵 | `np.eye(3)` | |

## 2. 看属性 / 改类型

| 我要干嘛 | 写法 |
| --- | --- |
| 形状 | `x.shape` → 如 `(2,3)` |
| 维度数 | `x.ndim` |
| 元素个数 | `x.size` |
| 数据类型 | `x.dtype` |
| 转类型 | `x.astype(np.float32)` ← **拷贝**，新数组 |

## 3. 索引 / 切片（改一改会不会动原数组）

| 我要干嘛 | 写法 | 视图还是拷贝 |
| --- | --- | --- |
| 取一块 | `x[1:3, 0:2]` | **视图** |
| 反向 | `x[::-1]` / `x[:, ::-1]` | **视图**（倒序只是"看法"） |
| 取整维 | `x[1]` | **视图** |
| 按下标列表取 | `x[[0,2,4]]` | **拷贝**（花式索引） |
| 按条件取 | `x[x > 5]` | **拷贝**（布尔索引） |
| 条件三目 | `np.where(cond, a, b)` | 返回新数组 |
| 取条件下标 | `np.where(cond)` | 返回下标元组 |
| 两头夹紧 | `np.clip(x, 0, 255)` | **拷贝** |
| 布尔赋值 | `x[x > 255] = 255` | 原地改 |

## 4. 改形状

| 我要干嘛 | 写法 | 备注 |
| --- | --- | --- |
| 换形状 | `x.reshape(2, 3)` / `x.reshape(-1)` | `-1` 让 numpy 自己算 |
| 转置 | `x.T` / `np.transpose(x, (2,0,1))` | **视图**、结果**不连续** |
| **加一个维度** | `np.expand_dims(x, axis=0)` | ⭐你忘的那个 |
| **减一个维度** | `np.squeeze(x, axis=0)` | ⭐要写 axis |
| 拍平 | `x.ravel()`（可能视图）/ `x.flatten()`（拷贝） | |
| 保证连续 | `np.ascontiguousarray(x)` | 不连续时→**拷贝** |

> 记忆钩子：**expand = 加（胀大），squeeze = 减（挤压）**。两个都要写 `axis`。

## 5. 广播
> 从**最后一维**往前对齐；相等 或 其中一个是 **1** → 可广播。
> 例：`(H,W,3)` 减 `(3,)` → 每通道各减一个值。

## 6. 统计 / 聚合

| 我要干嘛 | 写法 | axis 作用 |
| --- | --- | --- |
| 求和 / 均值 / 标准差 | `x.sum()` / `x.mean()` / `x.std()` | `axis=k` = 压缩掉第 k 维 |
| 最大 / 最小 | `x.max()` / `x.min()` | 同上 |
| 保留维度 | `x.sum(axis=1, keepdims=True)` | 结果不塌那一维 |
| 最大/最小值的**下标** | `np.argmax(x)` / `np.argmin(x)` | 不写 axis 先展平 |
| 排序的**座次** | `np.argsort(x)` | 默认升序；降序 `[::-1]` |
| 反摊平下标 | `np.unravel_index(idx, shape)` | 把扁平下标还原成多维 |

## 7. 拼接 / 拆分

| 我要干嘛 | 写法 | 结果维数 |
| --- | --- | --- |
| 接起来 | `np.concatenate([a,b], axis=0)` | **不变** |
| 叠起来 | `np.stack((a,b), axis=-1)` | **+1 维** |
| 切开 | `np.split(x, 2)` | |

## 8. 逐元素取大 / 小（和聚合版区分！）
| 我要干嘛 | 写法 |
| --- | --- |
| 逐元素取大 | `np.maximum(a, b)` ← 检测框 IoU 用 |
| 逐元素取小 | `np.minimum(a, b)` |
| 聚合取大 | `x.max()`（**不带 x**） |

## 9. 视图 / 拷贝 判定
| 我要干嘛 | 写法 |
| --- | --- |
| 是否共享内存 | `np.shares_memory(a, b)` / `b.base is a` |
| 显式拷贝 | `b = a.copy()` |
| 是否连续 | `x.flags["C_CONTIGUOUS"]` |

> **法则**：切片 / transpose / reshape / 整维取值 = **视图**；
> 花式索引 / 布尔索引 / astype / clip / copy() / 非连续时的 ascontiguousarray = **拷贝**。

## 10. 随机数（np.random）

| 我要干嘛 | 写法 |
| --- | --- |
| 固定种子（可复现） | `np.random.seed(42)` |
| 新式写法 | `rng = np.random.default_rng(0)` → `rng.random((2,2))` |
| `[0,1)` 均匀 | `np.random.rand(2, 3)`（维度直接写）/ `np.random.random((2,3))`（形状用元组） |
| 标准正态 N(0,1) | `np.random.randn(2, 3)` |
| 正态（自定均值/标准差） | `np.random.normal(loc, scale, size)` |
| 整数 `[low,high)` | `np.random.randint(0, 10, size=5)` |
| 任意区间均匀 | `np.random.uniform(low, high, size)` |
| 抽取（不放回） | `np.random.choice(10, size=3, replace=False)` |
| **原地打乱（返回 None）** | `np.random.shuffle(arr)` ⚠️ |
| **返回打乱副本（不动原数组）** | `np.random.permutation(arr)` |

## 11. 例题三件套（第 4 章工具包雏形）
- **预处理**：`astype(float32)/255 → (x-mean)/std → transpose(2,0,1) → expand_dims(axis=0) → ascontiguousarray`
- **向量化 IoU**：`maximum/minimum` 取交集四边 → `clip(0)` → 交 ÷ 并
- **NMS**：`argsort[::-1]` → 循环 → 每轮留队首、用 IoU 筛候选

---

## 怎么用这张表（重要）
1. **平时**：写代码忘了 → 直接查右列，**不要有心理负担**。查多了自然就记住了。
2. **复习**：**盖住右列**，看左列中文，默写函数名/调用。写不出的打 `?`，重点记。
3. **频次**：每天 3 分钟闪电测（10 条），比一次看半小时有用。
