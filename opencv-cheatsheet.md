# OpenCV 函数速查表（第 3 章）

> 用法：每个函数一个卡片。**先看「干什么」，再看「参数」，最后看「最小例子」**。
> 看不懂某一节时，直接翻回这里对应的卡片，不要硬猜。

---

## 一、图像读写（3.1）

### `cv2.imread(文件名, flags)`

**干什么**：从硬盘读一张图，返回 NumPy 数组。**读不到就返回 `None`，不报错。**

| 参数 | 含义 | 常用值 |
|---|---|---|
| 文件名 | 路径字符串 | `"cat.jpg"` |
| flags | 怎么读（可省，默认彩色） | `cv2.IMREAD_COLOR` 彩色三通道（默认）<br>`cv2.IMREAD_GRAYSCALE` 灰度两维<br>`cv2.IMREAD_UNCHANGED` 连透明通道一起读 |

**返回**：`ndarray`（shape 是 `(高, 宽, 3)` 或 `(高, 宽)`，dtype 是 `uint8`）；失败返回 `None`

```python
img = cv2.imread("cat.jpg")                            # (H, W, 3) BGR
gray = cv2.imread("cat.jpg", cv2.IMREAD_GRAYSCALE)     # (H, W)
```

**坑**：
- 读不到不报错，返回 `None` → 后面 `.shape` 才报 `AttributeError: 'NoneType' object has no attribute 'shape'`
- **Windows 下中文路径会失败**，返回 `None`（改成 `np.fromfile` + `imdecode`）

---

### `cv2.imwrite(文件名, 图像, 参数列表)`

**干什么**：把图像写成文件。

| 参数 | 含义 |
|---|---|
| 文件名 | 后缀决定格式（`.png` / `.jpg`） |
| 图像 | 要写的 `ndarray` |
| 参数列表 | 可选，如 `[cv2.IMWRITE_JPEG_QUALITY, 90]`（jpg 质量 0~100） |

**返回**：`bool` —— **成功 True，失败 False。必须检查！**

```python
ok = cv2.imwrite("out.png", img)
print(ok)     # True 才真写进去了

cv2.imwrite("out.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
```

**坑**：
- **返回 False 不报错**，文件可能根本没生成
- **中文路径会失败**（返回 False）
- png 无损、jpg 有损；**但 jpg 不一定比 png 小**——截图/示意图/纯色块图 png 反而更小

---

### `cv2.imshow(窗口名, 图像)`

**干什么**：弹一个窗口显示图像。**必须有桌面环境**，服务器/Jupyter 里不能用。

| 参数 | 含义 |
|---|---|
| 窗口名 | 字符串，同名窗口会复用 |
| 图像 | `ndarray`，`uint8`（float 要先转回 0~255） |

**返回**：`None`

```python
cv2.imshow("win", img)
cv2.waitKey(0)              # 必须！不然窗口一闪而过
cv2.destroyAllWindows()     # 关窗口
```

---

### `cv2.waitKey(毫秒)`

**干什么**：**暂停程序，等键盘输入**。`imshow` 只是“画上去”，`waitKey` 才是“停住让人看”。

| 参数 | 含义 |
|---|---|
| 毫秒 | `0` = 无限等待直到按键<br>`1` = 等 1 毫秒<br>`1000` = 等 1 秒 |

**返回**：按下的键的 ASCII 码（int）；超时返回 `-1`

```python
key = cv2.waitKey(0)
if key == 27:          # 27 = Esc
    cv2.destroyAllWindows()
```

---

### `cv2.destroyAllWindows()`

**干什么**：关掉所有 OpenCV 窗口。无参数，无返回。

```python
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### `cv2.imencode(扩展名, 图像, 参数列表)`

**干什么**：把图像**编码成一串字节**（内存里）。**完全不碰硬盘**。

| 参数 | 含义 |
|---|---|
| 扩展名 | **`.png` / `.jpg`，带点，不是文件名！** |
| 图像 | 要编码的 `ndarray` |
| 参数列表 | 可选，如 `[cv2.IMWRITE_JPEG_QUALITY, 90]` |

**返回**：`(ok, buf)` 元组
- `ok`：`bool` 成功标志
- `buf`：`ndarray`，**一维**（`shape = (N,)`，dtype `uint8`），`N` 就是文件字节数

```python
ok, buf = cv2.imencode(".png", img)
buf.tofile("中文名.png")        # 配合 tofile 写盘，支持中文路径
print(buf.shape)                # (7411,)  正好等于文件大小
```

**坑**：传 `"啊.png"` 也能跑（库只取最后一个点后面的部分），但**语义错误**——它不需要文件名

---

### `cv2.imdecode(字节数组, flags)`

**干什么**：把字节流**解码成图像**。

| 参数 | 含义 |
|---|---|
| 字节数组 | 一维 `uint8` 数组（通常来自 `np.fromfile`） |
| flags | 同 `imread`：`IMREAD_COLOR` / `IMREAD_GRAYSCALE` |

**返回**：`ndarray` 图像；失败返回 `None`

```python
data = np.fromfile("中文名.png", dtype=np.uint8)
img = cv2.imdecode(data, cv2.IMREAD_COLOR)
```

---

### `np.fromfile(文件名, dtype=np.uint8)`

**干什么**：把**任意文件**原样读成一维字节数组。是 NumPy 的函数，**支持中文路径**。

| 参数 | 含义 |
|---|---|
| 文件名 | 路径字符串 |
| dtype | 固定写 `np.uint8`（一个字节一个值） |

**返回**：一维 `ndarray`，`shape = (文件字节数,)`

```python
data = np.fromfile("测试图.png", dtype=np.uint8)
print(data.shape)     # (7411,)
```

**坑**：**读不到会抛 `FileNotFoundError`**（比 imread 的静默失败好排查）

---

### `数组.tofile(文件名)`

**干什么**：把一维数组**原样写到硬盘**。是 ndarray 的方法，**支持中文路径**。

| 参数 | 含义 |
|---|---|
| 文件名 | 路径字符串 |

**返回**：`None`

```python
buf.tofile("另存为.png")
```

---

### 绘图三件套（造测试图用）

#### `cv2.rectangle(img, 左上, 右下, 颜色, 线宽)`

| 参数 | 含义 |
|---|---|
| 左上 | `(x, y)` 元组，**x 是列、y 是行** |
| 右下 | `(x, y)` 元组 |
| 颜色 | BGR 元组，如 `(0,0,255)` 是红 |
| 线宽 | **`-1` = 实心填充**，正数 = 边框粗细 |

```python
cv2.rectangle(img, (30, 40), (130, 140), (0, 0, 255), -1)
```

**坑**：**两个端点像素都包含**，所以宽度 = `右-左+1`（130-30+1 = 101，不是 100）

---

#### `cv2.circle(img, 圆心, 半径, 颜色, 线宽)`

```python
cv2.circle(img, (220, 90), 45, (0, 255, 255), -1)     # 黄色实心圆
```

参数同 rectangle，`-1` 表示实心。

---

#### `cv2.putText(img, 文字, 左下角, 字体, 字号, 颜色, 线宽)`

| 参数 | 含义 |
|---|---|
| 文字 | 字符串（**不支持中文**） |
| 左下角 | `(x, y)`，注意是文字**左下**的定位点 |
| 字体 | 一般用 `cv2.FONT_HERSHEY_SIMPLEX` |
| 字号 | float，`1.0` 约等于 20px 高 |

```python
cv2.putText(img, "OpenCV", (20, 200), cv2.FONT_HERSHEY_SIMPLEX,
            1.0, (255, 255, 255), 2)
```

---

## 二、颜色空间（3.2）

### `cv2.cvtColor(图像, 转换代码)`

**干什么**：颜色空间转换（BGR↔RGB、BGR↔灰度、BGR↔HSV）。**返回拷贝，不共享内存。**

| 参数 | 含义 |
|---|---|
| 图像 | 输入 `ndarray` |
| 转换代码 | `cv2.COLOR_BGR2RGB` BGR 转 RGB<br>`cv2.COLOR_BGR2GRAY` 转灰度<br>`cv2.COLOR_BGR2HSV` 转 HSV<br>`cv2.COLOR_BGR2GRAY` 反向就写 `GRAY2BGR` |

**返回**：新的 `ndarray`

```python
rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)     # (H,W,3)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # (H,W)   少一维！
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)     # (H,W,3)
```

**要点**：
- 灰度：`Gray = 0.299R + 0.587G + 0.114B`（**绿的权重最大，因为人眼对绿最敏感**）
- HSV：H 是 0~179（**角度 ÷ 2**，因为 uint8 装不下 360），S/V 是 0~255
- 等价写法：`img[:, :, ::-1]` 也能 BGR→RGB，但**那是视图**（改它原图会变）

---

### `cv2.inRange(图像, 下限, 上限)`

**干什么**：判断**每个像素的三个通道是否都落在 [下限, 上限] 内**，是则给 255，否则 0。**三通道结论合并成一个。**

| 参数 | 含义 |
|---|---|
| 图像 | `ndarray`，通常是 HSV 图 |
| 下限 | 数组，和通道数一样长，如 `np.array([20, 100, 100])` |
| 上限 | 同上 |

**返回**：`(H, W)` 的 `uint8` 掩码，**只有 0 和 255 两种值**，**两维（没有通道维）**

```python
mask = cv2.inRange(hsv, np.array([20,100,100]), np.array([40,255,255]))
print(mask.shape)      # (240, 320)   ← 两维！
print(np.unique(mask)) # [0 255]
```

**意义**：`lower = [H下, S下, V下]`，三个条件**同时满足**才通过（逻辑与）

**坑**：
- 红色跨越色环接缝（0 和 179 都是红），**必须两段范围 + `bitwise_or` 合并**
- 其他颜色（黄绿青蓝）一段就够

---

### `np.unique(数组, return_counts=False)`

**干什么**：**去重 + 排序**，返回里面有哪些不同的值。

| 参数 | 含义 |
|---|---|
| 数组 | 任意 `ndarray` |
| return_counts | `True` 时额外返回每个值出现几次 |

**返回**：去重排序后的一维数组；`return_counts=True` 时返回 `(值数组, 计数数组)`

```python
np.unique([3,1,3,2])                        # [1 2 3]
np.unique(mask)                             # [  0 255]   ← 检查掩码是否干净
vals, cnts = np.unique(mask, return_counts=True)
# vals=[0 255]  cnts=[13139 6361]    ← 6361 就是黄色圆面积
```

**用途**：拿到不知道哪来的掩码/标签图，先 `unique` 一眼看是什么材质

---

## 三、通道操作与掩码（3.2）

### `cv2.split(图像)`

**干什么**：把三通道图拆成三个**单通道**图。

| 参数 | 含义 |
|---|---|
| 图像 | 三通道 `ndarray` |

**返回**：`(b, g, r)` 三个 `(H, W)` 数组（**两维，通道维被拿走**）

```python
b, g, r = cv2.split(img)
print(b.shape)                          # (240, 320)
print(np.array_equal(b, img[:, :, 0]))  # True  ← 和切片完全等价
```

---

### `cv2.merge([通道1, 通道2, 通道3])`

**干什么**：三个单通道图合并成一个三通道图。**顺序很重要！**

| 参数 | 含义 |
|---|---|
| 列表 | `[b, g, r]` 按 **BGR** 顺序传 |

**返回**：`(H, W, 3)` 数组

```python
merged = cv2.merge([b, g, r])           # 正确
wrong  = cv2.merge([r, g, b])           # 红蓝颠倒！
```

**坑**：**顺序写错不报错**，但红色变蓝色。这正是“模型准确率悄悄下降”的经典原因

---

### `cv2.bitwise_and(图像1, 图像2, mask=掩码)`

**干什么**：两张图逐像素按位与。**最常见的用法其实是“用掩码裁剪”**。

| 参数 | 必需？ | 含义 |
|---|---|---|
| 图像1 | ✅ 必需 | `src1` |
| 图像2 | ✅ 必需 | `src2`，**不能省！** |
| mask | ❌ 可选 | 只处理 255 处，0 处输出变黑 |

**返回**：同形状的 `ndarray`

```python
only_red = cv2.bitwise_and(img, img, mask=red_mask)
```

**要点**：
- 传**两次自己**，因为 `img AND img = img`，让"与"不起作用，纯靠 mask 筛选
- 只传一次会报 `missing required argument 'src2' (pos 2)`
- 两维 mask 能配三维图，因为 mask 会广播（`(H,W)` → `(H,W,1)` → `(H,W,3)`）

---

### `cv2.bitwise_or(图像1, 图像2)` / `cv2.bitwise_not(图像)` / `cv2.bitwise_xor(a, b)`

| 函数 | 作用 | 典型用途 |
|---|---|---|
| `bitwise_or` | 或：任一边非零就保留 | **合并两段掩码**（红色两段范围） |
| `bitwise_not` | 非：黑白反转 | **取反掩码**（保留区域外的部分） |
| `bitwise_xor` | 异或：不同才保留 | 找两张图差异 |

```python
red_mask = cv2.bitwise_or(mask_a, mask_b)      # 合并两段红
inv = cv2.bitwise_not(red_mask)                # 反转：只要非红区域
```

---

## 四、缩放与补边（3.4）

### `cv2.resize(图像, dsize, fx, fy, interpolation)`

**干什么**：改变图像尺寸。**返回拷贝，不共享内存。**

| 参数 | 必填 | 含义 |
|---|---|---|
| 图像 | ✅ | 原图 ndarray |
| dsize | ✅ | **`(宽, 高)`** —— 和 shape 的 `(高, 宽)` **正好相反**；写 `None` 时用 fx/fy |
| fx, fy | ❌ | 宽、高各自的缩放倍数；与 dsize 二选一，都写时 **dsize 优先** |
| interpolation | ❌ | 插值方式，默认 `INTER_LINEAR` |

**返回**：`ndarray`，`shape = (新高, 新宽, 通道数)`，dtype 不变

```python
half = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))   # 缩一半
big  = cv2.resize(img, None, fx=2, fy=2)                          # 放大两倍
```

**坑**：
- **dsize 写反不报错**，图被拉成别的比例 —— 最阴的坑
- dsize 必须是**整数**元组，`(w*0.5, h*0.5)` 是 float 会报 `Can't parse 'dsize'`
- 缩小用 LINEAR 会混叠（漏看 96/100 的像素），要用 AREA

### 四种插值方式（背这张）

| 常量 | 中文 | 怎么算新像素 | 什么时候用 |
|---|---|---|---|
| `INTER_NEAREST` | 最近邻 | 直接抄最近的像素 | 最快；掩码/标签图（不能造中间值）；马赛克 |
| `INTER_LINEAR` | 双线性 | **2×2** 邻居按距离加权 | 默认；**放大首选** |
| `INTER_CUBIC` | 双三次 | **4×4** 邻居加权，更锐 | 高质量放大（慢，边缘轻微过冲） |
| `INTER_AREA` | 区域重采样 | 整块覆盖区域取均值 | **缩小首选** |

> 插值直觉：**放大怕"太空"（造新像素，按距离加权），缩小怕"太挤"（会漏像素，AREA 一个不漏）**。
> 放大 5 倍时边界只出现 4 个过渡值（f = 0.2/0.4/0.6/0.8），如 255→204→153→102→51→0。

### `cv2.copyMakeBorder(图像, top, bottom, left, right, borderType, value)`

**干什么**：给图像四周加边框。**letterbox 的补边就靠它。**

| 参数 | 必填 | 含义 |
|---|---|---|
| 图像 | ✅ | 原图 |
| top, bottom, left, right | ✅ | **上、下、左、右**各加几像素（不是顺时针！） |
| borderType | ✅ | `BORDER_CONSTANT` 填固定色（letterbox 用）/ `REPLICATE` 复制边缘 / `REFLECT` 镜像 |
| value | ❌ | 填充色 **BGR**，如 `(114, 114, 114)` 灰；只对 CONSTANT 生效 |

**返回**：`ndarray`，`shape = (高+top+bottom, 宽+left+right, 通道)`

### `letterbox` 模板（目标检测预处理标准操作）

```python
def letterbox(img, size=640, color=(114, 114, 114)):
    h, w = img.shape[:2]
    scale = min(size / h, size / w)          # 取小的：两条边都不超标
    nw, nh = int(w * scale), int(h * scale)  # 等比新尺寸
    resized = cv2.resize(img, (nw, nh))
    dw, dh = size - nw, size - nh
    top, bottom = dh // 2, dh - dh // 2      # 空隙平分，余数丢给下/右
    left, right = dw // 2, dw - dw // 2
    out = cv2.copyMakeBorder(resized, top, bottom, left, right,
                             cv2.BORDER_CONSTANT, value=color)
    return out, scale, (left, top)
```

**三步记忆**：① `scale = min(...)` 等比缩到长边顶满 ② resize ③ 空隙 `//2` 平分补灰。
**为什么取 min**：取 max 会有一边超出 size，超了就得裁；不够可以补，超了不能裁。
**正方形图**：dw=dh=0，自动退化成普通等比 resize，不用写 if。
**返回 scale 和 pad 干嘛用**：模型输出的框坐标是补边图上的，要 ÷scale、−pad 才能映射回原图。

---

## 五、数值归一化（3.5）

### `cv2.normalize(图像, dst, alpha, beta, norm_type, dtype)`

**干什么**：把数值线性变换到指定区间（`NORM_MINMAX` 时）。

| 参数 | 必填 | 含义 |
|---|---|---|
| 图像 | ✅ | 输入数组 |
| dst | ✅ | 输出数组，**Python 里永远写 `None`**（函数新建并返回） |
| alpha, beta | ✅ | MINMAX 模式 = 目标区间的**最小值、最大值** |
| norm_type | ❌ | `NORM_MINMAX` 拉到 [alpha, beta]；`NORM_L1/L2/INF` 是范数归一化（图像预处理不用） |
| dtype | ❌ | `-1` = 跟原图一致 —— **归一到 0~1 时必须写 `cv2.CV_32F`** |

**返回**：新 ndarray

```python
# 拉伸到 0~255（= 对比度拉伸）
st = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

# 归一化到 0~1（喂模型）—— 必须带 dtype
x = cv2.normalize(img, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
```

**四种 norm_type 别搞混**：

| type | 保证什么 | 图像用吗 |
|---|---|---|
| `NORM_MINMAX` | min→alpha，max→beta | ✅ 唯一的 |
| `NORM_L1` | 所有元素**绝对值之和** = alpha | ❌ |
| `NORM_L2` | 平方和开根 = alpha | ❌ |
| `NORM_INF` | **最大绝对值** = alpha | ❌ |

> 只有 MINMAX 同时用 alpha 和 beta，其余三个只用 alpha。

### 两个坑（都是“不报错的错”）

**坑 1：uint8 装不下 0~1 的小数**

```python
bad  = cv2.normalize(img, None, 0, 1, cv2.NORM_MINMAX)                    # uint8 → 只剩 [0 1] 两个值
good = cv2.normalize(img, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)  # float32 → 0.0~1.0
```

`[60, 130, 200]` 归一化到 0~1 得 `[0, 0.5, 1]`，但结果写回 uint8（只有 0/1 两档整数）→ `[0, 0, 1]`，**中间值全灭**。

**坑 2：`img / 255` 的 dtype 是 float64（黑洞）**

```python
a = img.astype(np.float32) / 255   # float32 ← 正确
b = img / 255                      # float64 ← 整数参与 / 必升 float64，内存 ×8
```

规则：**整数数组只要参与 `/`，结果必是 float64**；float32 参与运算才保持 float32。

### 三种“归一/拉伸”的区别

```
归一化 /255：      新值 = 原值 × (1/255)                 只缩放，不平移
min-max 拉伸：    新值 = (原值 − min) × 255/(max−min)    先平移再缩放，两端被顶满
标准化（standardize）：新值 = (原值 − 均值) / 标准差      范围不是 0~1，深度学习常用
```

> 全范围图（min=0, max=255）做前两种结果相同。区别只在**没占满范围**的图上显现：拉伸提对比度，除 255 不提。

### 手写 min-max 拉伸（不依赖 cv2）

```python
def stretch(img):
    lo, hi = img.min(), img.max()
    out = (img.astype(np.float32) - lo) / (hi - lo) * 255
    return out.astype(np.uint8)
```

与 `cv2.normalize(...NORM_MINMAX)` 的结果**最大差 1**（舍入方向不同），不要用 `array_equal` 判等，用 `np.abs(a.astype(np.int16) - b).max()`。

**浮点提醒**：算出来的“0”常是 `-1.86e-09` 这类灰尘，判零写 `abs(x) < 1e-6`，永远别写 `== 0`。

---

## 六、几何变换（3.6）

### 先分清两个家族（本节最大的坑）

| 家族 | 函数 | 返回什么 | 动图吗 |
|---|---|---|---|
| **出图纸** | `getRotationMatrix2D(center, angle, scale)` | `(2, 3)` float64 | ❌ 一个像素都不动 |
| | `getAffineTransform(src3, dst3)` | `(2, 3)` float64 | ❌ |
| | `getPerspectiveTransform(src4, dst4)` | `(3, 3)` float64 | ❌ |
| **施工** | `warpAffine(img, M, dsize)` | 图像 `(h, w, 3)` | ✅ |
| | `warpPerspective(img, M, dsize)` | 图像 `(h, w, 3)` | ✅ |

> 矩阵里装的是 `cosθ`、`sinθ` 这类小数 → **dtype 固定 float64**，shape 是 `(2,3)` 或 `(3,3)`，**没有第三维，根本不是图**。
> 口诀：`get` 开头 = 出图纸；`warp` 开头 = 按图纸施工。

### 三条铁律

```
1. dsize 一律 (宽, 高)   —— 只有 shape 是 (高, 宽)
2. center 是 (x, y)      —— 即 (列, 行)，跟 shape 反
3. 透视图点顺序 左上 → 右上 → 右下 → 左下（顺时针，两边必须一致）
```

### `cv2.flip`

```python
cv2.flip(src, flipCode) -> ndarray
```

| 参数 | 含义 |
|---|---|
| `flipCode` | `1` 左右翻（水平）　`0` 上下翻（垂直）　`-1` 两者都翻 |

**返回**：图，**shape 不变**，拷贝。**坑**：`1` 是左右、`0` 是上下，最易记反。

### `cv2.getRotationMatrix2D`

```python
cv2.getRotationMatrix2D(center, angle, scale) -> ndarray(2×3, float64)
```

| 参数 | 含义 |
|---|---|
| `center` | 绕哪个点转，**`(x, y)`** = `(列, 行)` |
| `angle` | 角度（度），**逆时针为正**，顺时针写负数 |
| `scale` | 缩放倍数，`1.0` = 不缩放 |

**返回**：`[[cos, sin, tx], [-sin, cos, ty]]`，float64。**第三列是绕中心转自带的平移补偿**（不补的话图会甩出画面）。

### `cv2.warpAffine`

```python
cv2.warpAffine(src, M, dsize, flags=INTER_LINEAR, borderMode=BORDER_CONSTANT, borderValue=0) -> ndarray
```

| 参数 | 含义 |
|---|---|
| `src` | 原图 |
| `M` | 2×3 矩阵，**dtype 必须 float32 / float64**，不能用 uint8 |
| `dsize` | 输出 **`(宽, 高)`** |
| `flags` | 插值方式，同 resize 那一套 |
| `borderValue` | 变换后空出来的角落填什么，默认 `0`（黑） |

**平移矩阵**：`np.float32([[1, 0, dx], [0, 1, dy]])` —— 第一列管 x、第二列管 y、第三列是平移量。

**坑**：`dsize` 沿用原尺寸，旋转后四角必然被裁。

### 透视：`getPerspectiveTransform` + `warpPerspective`

```python
cv2.getPerspectiveTransform(src, dst) -> ndarray(3×3, float64)
cv2.warpPerspective(src, M, dsize)    -> ndarray
```

| 参数 | 含义 |
|---|---|
| `src` | 原图里 4 个点，`shape (4,2)`，**每行 `(x, y)`**，**dtype 必须 float32** |
| `dst` | 希望映射到的 4 个点，同样 `(4,2)` float32 |
| 顺序 | 左上 → 右上 → 右下 → 左下 |

**怎么判断校正成功了**：结果矩形内几乎全是目标内容（实验值 59750/60000 白）。
**顺序搞错的标志**：只剩几十个白像素，图被拧成麻花。

### 旋转不裁边：`rotate_keep` 模板

```python
def rotate_keep(img, angle):
    h, w = img.shape[:2]
    cx, cy = w / 2, h / 2
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)

    cos, sin = abs(M[0, 0]), abs(M[0, 1])          # 直接向矩阵要，不用自己算
    nw, nh = int(w*cos + h*sin), int(h*cos + w*sin)  # 旋转后包围盒

    M[0, 2] += nw / 2 - cx                          # 中心挪回新画布正中
    M[1, 2] += nh / 2 - cy

    return cv2.warpAffine(img, M, (nw, nh))
```

**包围盒公式怎么来的**：矩形转过 θ，它的两条边各留下"影子"，外接框的宽 = 两条边的水平影子之和：
`nw = w·cos + h·sin`、`nh = h·cos + w·sin`。

| 角度 | nw | nh | 含义 |
|---|---|---|---|
| 0° | w | h | 退化成原尺寸（自检点） |
| 90° | h | w | **长宽互换**（探针） |
| 45° | 200×0.707+100×0.707 = 212 | 同左 | 两方向一样大 |

**自检法**：`rotate_keep(img, 90)` 的长宽必须互换。三行输出全一样，就说明 `dsize` 没吃进 `nw/nh`。

---

## 七、阈值、直方图与对比度增强（3.7）

### 先记一条铁律：这一族只吃单通道灰度图

`threshold` / `adaptiveThreshold` / `equalizeHist` / `clahe.apply` **全部只收 `(H, W)` 的 uint8 灰度图**。喂三通道彩色图不报"色彩乱"，而是直接 `Assertion failed`（`histogram.cpp` / `thresh.cpp`）。

彩色图要做均衡，标准三步（Part 5 的手感）：

```python
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)      # ① 转 HSV
hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])        # ② 只均衡 V（第 2 号维度）
out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)      # ③ 转回 BGR
```

> **为什么只动 V**：H 管色相、S 管饱和度。动了 H 颜色就串了，动了 S 就发灰发艳。只有 V（亮度）可以拉。

### `cv2.threshold`

```python
retval, dst = cv2.threshold(src, thresh, maxval, type)
```

| 参数 | 含义 |
|---|---|
| `src` | **单通道 uint8 灰度图** |
| `thresh` | 阈值；用 Otsu 时**随便填**（被忽略） |
| `maxval` | 判为"达标"时赋的值，通常 255 |
| `type` | 见下表 |

| type | 规则 |
|---|---|
| `THRESH_BINARY` | `x > thresh → maxval`，否则 0 |
| `THRESH_BINARY_INV` | 反过来 |
| `THRESH_TRUNC` | `x > thresh → thresh`，否则原值 |
| `THRESH_TOZERO` | `x > thresh` 保留，否则 0 |
| `THRESH_OTSU` | **与上面任一按位或**：`THRESH_BINARY \| THRESH_OTSU`，自己算阈值 |

**返回**：**元组 `(retval, dst)`** —— 必须写 `ret, th = cv2.threshold(...)`，只接一个的话拿到的是元组，`.shape` 会报 `AttributeError`。

- **`retval` 是 `float`**（`127.0` 不是 `127`），别以为它是 int
- 没用 Otsu：`retval` = 你传进去的 `thresh`
- 用了 Otsu：`retval` = 它算出来的阈值（实测低对比度图 100~140 三档时算出 `122.0`）

**Otsu 在干嘛**：把直方图分成两堆，找一个让"堆内差异最小、堆间差异最大"的阈值。图里的灰度分成几档差别明显时，它一次就找准，不用你手调。

### `cv2.adaptiveThreshold`

```python
dst = cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C)
```

| 参数 | 含义 |
|---|---|
| `src` | **单通道 uint8** |
| `maxValue` | 达标赋的值 |
| `adaptiveMethod` | `ADAPTIVE_THRESH_MEAN_C`（邻域均值）/ `ADAPTIVE_THRESH_GAUSSIAN_C`（高斯加权） |
| `thresholdType` | **只能 `THRESH_BINARY` / `THRESH_BINARY_INV`**（不能带 Otsu） |
| `blockSize` | 邻域边长，**必须是奇数且 > 1**，否则 `Assertion failed: blockSize % 2 == 1 && blockSize > 1` |
| `C` | 从邻域均值里**减掉**的常数 |

**返回**：**只有一个 `dst`**（不像 `threshold` 返回元组）—— 这俩最容易混。

**C 的方向（易写反，实测确认）**：

```
有效阈值 = 邻域均值 − C
C 大 → 阈值低 → 宽松 → 白像素多
C 小 → 阈值高 → 严格 → 白像素少
```

实测（同一张图，blockSize=11）：`C=5 → 17999` 白，`C=1 → 11237` 白。

**为什么需要它**：一张纸一半被灯照亮一半在阴影里，全局切一刀，亮的全白、暗的全黑。自适应是**每个像素问自己周围的邻居**"这块平均多亮"，各自定标准。

### `cv2.calcHist` —— 直方图（⚠️ 5.0 返回一维）

```python
hist = cv2.calcHist(images, channels, mask, histSize, ranges)
```

| 参数 | 写法（**五个参数全是列表**） |
|---|---|
| `images` | `[gray]` |
| `channels` | 灰度 `[0]`；BGR 分别 `[0]`/`[1]`/`[2]` |
| `mask` | `None` = 全图；给掩码则只统计掩码内 |
| `histSize` | `[256]` = 分 256 格 |
| `ranges` | `[0, 256]`（**是 256 不是 255**，开区间上界） |

**返回（重要）**：

| 版本 | shape | 取"灰度 120 的像素数" |
|---|---|---|
| OpenCV 4.x（教材写法） | `(256, 1)` | `hist[120]` → 1 元素数组 |
| **OpenCV 5.0.0（本机）** | **`(256,)`** | `hist[120]` → **标量** |

dtype **永远是 `float32`**（不是 float64、不是 uint8）。
兼容两版的写法：`cv2.calcHist(...).flatten()`。

**怎么理解这个数组**：一条 256 格的表，**每格装"这个灰度有多少像素"**：

```python
h[0]        # 灰度 0 的像素个数
h[120]      # 灰度 120 的像素个数
h.sum()     # 所有格子加起来 = 图像总像素数 H×W   ← 免费自检！
h.argmax()  # 像素最多的灰度值（图里占比最大的那一档）
```

> **不是 `(256,256)` 方阵** —— 那是把"灰度 × 灰度"的二维直方图搞混了（3.8 的 2D 直方图才有多维）。
> **`h.sum() == H×W` 不对 → 检查 mask / ranges / histSize**。

### `cv2.equalizeHist` —— 全局均衡

```python
dst = cv2.equalizeHist(src) -> ndarray
```

| 参数 | 含义 |
|---|---|
| `src` | **单通道 uint8 灰度图**（彩色报错） |

**返回**：同 shape 灰度图，**尺寸不变，只改灰度分布**。

**干的事**：把直方图摊平 —— 出现多的灰度区间被拉开、出现少的被压缩。

**两个毛病**：
1. **全局一刀切**：一半亮一半暗时，均衡后亮的更亮暗的更暗，局部对比度反而变差
2. **噪声被放大**：5 个点的噪声被拉开到 50 个灰度级，肉眼可见

### `cv2.createCLAHE` —— 分块 + 限高（毕设主角）

```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
dst = clahe.apply(src)
```

| 参数 | 含义 |
|---|---|
| `clipLimit` | 对比度上限，2.0~4.0 常用 |
| `tileGridSize` | 切成几×几块，`(8,8)` = 64 块，每块**自己算自己的直方图** |

**返回**：⚠️ **返回的不是图像，是一个 CLAHE 处理器对象**（`cv2.CLAHE`），必须 `.apply(图)`。

```python
cv2.createCLAHE(2.0, (8,8))(gray)   # ❌ TypeError: 'cv2.CLAHE' object is not callable
clahe = cv2.createCLAHE(2.0, (8,8)) # ✅ 造处理器
cl = clahe.apply(gray)              # ✅ 处理器吃图
cl2 = clahe.apply(other)            # ✅ 一个处理器可以反复用
```

**两个关键词**：
- **分块（tile）**：亮区暗区各拉各的，互不干扰 → 解决 equalizeHist 一刀切
- **限高（clip）**：直方图柱子太高被削平，削下来的像素平摊给所有格子 → 噪声不放大

**`clipLimit` 调大 → 两个方向同时变**：

| clipLimit | 对比度 | 噪声 |
|---|---|---|
| 2.0（限得紧） | 温和 | 少 |
| 10.0（限得松） | 强 | **明显放大** |

实测 std（对比度量化指标）：`equalizeHist 74.5 > CLAHE(clip=10) 16.0 > CLAHE(clip=2) 10.8`。
> `eq` 的 std 特别大不是"更好"，是因为它把整张图硬拉到 0~255 全range，局部反而失真。

**为什么毕设用它**：医学图像病灶灰度变化细微、又常带噪声。全局均衡把噪声放大到看不清，CLAHE 分块提局部对比度 + 限高压噪声，两个问题一起解决。`clipLimit` 和 `tileGridSize` 就是你要搜的两个超参。

### 选型一张表

| 场景 | 用什么 |
|---|---|
| 光照均匀、目标和背景灰度差明显 | `threshold` + Otsu |
| 光照不均（半边暗、拍照有阴影） | `adaptiveThreshold` |
| 想知道图亮不亮、暗不暗、平不平 | `calcHist`（画出来看） |
| 整张图偏灰、想快速提对比度 | `equalizeHist` |
| 局部细节要提、又不能放大噪声 | `createCLAHE` ← 毕设 |

## 八、滤波：平滑与去噪（3.8）

### 一张表定选型

| 滤波 | 函数 | 怎么合 25 个数 | 椒盐噪声 | 高斯噪声 | 边缘 | 耗时（512², 9×9） |
|---|---|---|---|---|---|---|
| 均值 | `cv2.blur` | 求和 ÷ 面积 | ❌ 把噪声抹成一片灰 | ✅ 一般（2.40） | ❌ 糊（12 列） | **0.17 ms** |
| 高斯 | `cv2.GaussianBlur` | 距离加权（中心最重） | ❌ | ✅ 好（2.03） | ❌ 略好于均值（7 列） | **0.15 ms** |
| 中值 | `cv2.medianBlur` | **排序取中位数** | ✅ **最佳（std→0）** | ✅ 可用 | ✅ **不糊（0 列）** | 9.11 ms（最慢） |
| 双边 | `cv2.bilateralFilter` | 距离 × **颜色差** 双权重 | ❌ | ✅ 好（1.77） | ✅ **保边（4 列）** | 3.39 ms |

> 数字是 3.8 练习的实测（平坦区 std / 过渡带列数）。**std 越小越干净，过渡带 0 = 没糊。**

### 核心机制：为什么中值能同时“去椒盐 + 保边”

```
均值/高斯：会算出新值  → 边缘被磨成斜坡（模糊的由来）
中值    ：只从邻域已有值里挑一个 → 永远不产生新值 → 边缘只能"跳"，不会斜坡
```

窗口跨在 100|180 的边界上：25 个数排序后取第 13 个，要么 100 要么 180，**不可能是 140**。
椒盐同理：0 和 255 是极端值，排序后排在两头，中位数根本取不到它们（前提：噪声占比 < 一半）。

### `cv2.blur` / `cv2.boxFilter`

```python
dst = cv2.blur(src, ksize)   # ksize = (宽, 高) 元组
```

- 允许偶数 ksize（但偶数窗口没正中心，图会整体偏半像素）→ **一律用奇数**
- `boxFilter` 是同族，多 `ddepth`（填 `-1`）和 `normalize`（`True` = 求平均；`False` = 只求和，全白爆表）

### `cv2.GaussianBlur`

```python
dst = cv2.GaussianBlur(src, ksize, sigmaX, sigmaY=0)
```

| 参数 | 要点 |
|---|---|
| `ksize` | **必须奇数**（或 `(0,0)` 由 sigma 反推）；偶数 → `Assertion failed: ksize.width % 2 == 1` |
| `sigmaX` | **`0` = 自动按 ksize 推算**（不是"不模糊"！5×5 → 1.1） |
| `sigmaY` | 填 `0` = 与 sigmaX 相同 |

- `ksize` 定窗口大小，`sigma` 定加权曲线的陡缓
- **可分离**（横一遍 + 竖一遍）→ 极快，实时首选

### `cv2.medianBlur`

```python
dst = cv2.medianBlur(src, ksize)   # ksize 是单个整数！不是元组
```

- `ksize` 必须**奇数且 > 1**；写 `(5,5)` 直接报错
- 专治**椒盐噪声**（0/255 孤立点），且**保边**
- 慢：每像素维护邻域直方图，不可分离，并行度低 → 视频处理时 ksize 别开大

### `cv2.bilateralFilter`

```python
dst = cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace)
```

| 参数 | 要点 |
|---|---|
| `d` | 邻域**直径**：`d=5` → 5×5；`d<=0` 时由 `sigmaSpace` 反推（约 `round(σs*1.5)*2+1`） |
| `sigmaColor` | **颜色差容忍度**。小（20~50）= 只允许相近颜色进来 = 保边；**大（150+）= 全放进来 = 退化成高斯** |
| `sigmaSpace` | 空间距离容忍度，越大越糊 |
| 支持类型 | **8U / 32F**（`uint16` 报 `-210 Unsupported format`） |

**机制**：`权重 = f(距离) × g(颜色差)`。跨边缘时颜色差大 → `g≈0` → 边缘外的邻居不参与平均 → 边缘保住。

> ⚠️ **`sigmaColor` 越大不等于越保边，而是越糊**。这是最反直觉的一条。

### 三个坑合集

1. **参数形态不同**：`blur` / `GaussianBlur` 传**元组** `(5,5)`；`medianBlur` 传**单个整数** `5`
2. **`sigmaX=0` 不是不模糊**，是自动算
3. **耗时排序看"可分离性"不看"数学复杂度"**：卷积类（`blur`/`GaussianBlur`）的 2D 窗口能拆成横竖两遍（`k²`→`2k`）再叠加 SIMD，所以极快；`medianBlur` 要维护邻域直方图、拆不开，反而最慢。实测 512×512、9×9：`gauss` 0.15 ≈ `blur` 0.17 ≪ `bilateral` 3.39 ≪ **`median` 9.11 ms**。
   高斯/均值**可分离**（`k²` → `2k`），中值**不可分离**

### 毕设建议流水线

```
原图 → (高斯/中值去噪) → CLAHE 提对比度 → 归一化 → 喂模型
```

顺序别反：**先降噪再提对比度**，否则 CLAHE 会把噪声一起拉亮。

## 九、边缘检测：Sobel / Scharr / Laplacian / Canny（3.9）

### 梯度三个算子

```python
gx = cv2.Sobel(src, cv2.CV_16S, 1, 0, ksize=3)   # dx=1 → 找竖直边
gy = cv2.Sobel(src, cv2.CV_16S, 0, 1, ksize=3)   # dy=1 → 找水平边
g  = cv2.Scharr(src, cv2.CV_16S, 0, 1)           # 权重更大，更敏感（5.0 已无 ksize 参数）
lap = cv2.Laplacian(src, cv2.CV_16S, ksize=3)    # 二阶导，噪声放大最狠
```

| 算子 | 阶数 | 核权重和（dy） | 响应（差 160 的台阶） | 特点 |
|---|---|---|---|---|
| Sobel | 1 阶 | 4 | **640** | 标准选择 |
| Scharr | 1 阶 | 16 | **2560**（Sobel 的 4 倍） | 3×3 里精度最高，小图/弱边首选 |
| Laplacian | 2 阶 | — | 双边响应 | 对噪声极敏感，**先 GaussianBlur** |

### 三条铁律

1. **`dx=1` 找竖直边**（求导方向 ⊥ 边的走向）。想找水平边就给 `dy=1`
2. **`ddepth` 必须写 `cv2.CV_16S`**。写 `CV_8U` 时：负梯度被削成 **0**，正梯度超过 255 被削平到 **255** → 右/下边整条消失，上/左边全成纯白线
3. 梯度**有正负**：往下变亮（40→200）= `+640`；往下变暗（200→40）= `−640`

```python
abs_g = cv2.convertScaleAbs(gy)   # 取绝对值 + 转 uint8，显示用
```

### Sobel 核长什么样（`dy`，ksize=3）

```
-1  -2  -1     上面一行的权重和 = -4
 0   0   0
 1   2   1     下面一行的权重和 = +4
```

**梯度 = 上下亮度差 × 权重和**。所以 160 的台阶 → `160 × 4 = 640`。
`ddepth=CV_32F` 时 Scharr 也是 2560（不是 640×4 之外的额外因素，就是权重和 16）。

> ⚠️ **读数值避开拐角**：方块左上角 `(30,50)` 处测 `gy` 得 480 而非 640，因为那一列左边还是暗的，3×3 邻域里混进了横向差异。取边中段（如 `(30,70)`）才是干净的 640。

### `cv2.Canny`

```python
edges = cv2.Canny(image, threshold1, threshold2[, apertureSize[, L2gradient]])
```

| 参数 | 要点 |
|---|---|
| `image` | 8 位图。**彩色 3 通道也能直接进**（内部转灰度），输出仍是单通道 |
| `threshold1` | 低阈值 |
| `threshold2` | 高阈值。**顺序无所谓**，内部自动把小的当低阈值 |
| `apertureSize` | 内部 Sobel 核，默认 3 |
| `L2gradient` | `False`=\|gx\|+\|gy\|（快）；`True`=√(gx²+gy²)（准） |

**返回**：单通道 `uint8`，值**只有 0 和 255**，shape 同输入前两维。

### 内部三步（理解这三步就全懂了）

```
Sobel 算 gx,gy → ① NMS 削成 1 像素 → ② 双阈值分档 → ③ 滞后连接
```

| 步骤 | 干什么 | 实测证据 |
|---|---|---|
| ① NMS | 粗边削细 | Sobel 上边界 `row29`/`row30` **两行都 640**；Canny 后只剩 `row29` 一行 |
| ② 双阈值 | `>t2` 强边直接要；`<t1` 丢弃；中间是弱边候选 | 弱边梯度 ~100，`Canny(50,100)`→332 点保留；`Canny(50,120)`→176 点，弱边全灭 |
| ③ 滞后连接 | 弱边**只要挨着强边就保留**，孤立则丢 | 弱块接在强块下面（无缝隙）→ 弱段 100 个点；中间隔 5 行 → 弱段 **0** 个点 |

**最关键一条**：弱边本身不合格，但连接到强边就被拉活。所以 Canny 出来的线基本连通，不会断成一截一截。

### 坑合集

1. `np.unique(edges)` 只有 `[0, 255]`，别把输入图的灰度值当成输出
2. `Canny` **只返回一个值**（不像 `threshold` 返回元组）
3. 阈值不是"越高边越准"，是"越高边越少"。t2 一过弱边梯度，弱边成片消失
4. 先滤波再 Canny，否则噪声梯度直接进强边

### 形态学四件套

```python
k  = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))     # 5x5 全 1
ke = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))  # 圆形目标用它，角上不误切
e  = cv2.erode(img, k, iterations=1)    # 腐蚀 = 邻域取最小，亮区变瘦
d  = cv2.dilate(img, k, iterations=1)   # 膨胀 = 邻域取最大，亮区变胖
o  = cv2.morphologyEx(img, cv2.MORPH_OPEN,  k)   # 开 = 先腐后膨：灭小白点
c  = cv2.morphologyEx(img, cv2.MORPH_CLOSE, k)   # 闭 = 先膨后腐：填小黑洞
```

**结构元不是权重**：滤波核是加权求和能算出新值；结构元只是 0/1 的"哪些格子必须全亮"检查表，**输出永远是已有值**。

### 尺寸换算（都是实测）

| 调用 | 80 宽方块 |
|---|---|
| `erode(k5)` | 76（每边缩 2 = (k−1)/2，不是缩 5） |
| `erode(k5, iterations=2)` | 72 —— **完全等价于 `erode(k9)`**（array_equal True） |
| `erode(k9)` | 72 |
| `dilate(k5)` | 84 |

```
iterations = n  ≡  核尺寸 + 2(n-1)
```

### 开运算实测（为什么"灭点不缩块"）

| 操作 | 白像素 | 连通块 | 大块宽 | 4×4 小白点 |
|---|---|---|---|---|
| 原图 | 6316 | 2 | 80 | 16 |
| `erode5` | 5580 | 1 | 76 | **0** |
| `open5` | **6300** | **1** | **80** | **0** |

erode 杀光小白点 → dilate 把大块胖回原尺寸，**但被杀的救不回来**。
开完白像素一点没少 = 图里没有比核小的结构（有用的信号）。

### 闭运算填洞有硬上限

10×10 的洞：`close 5×5` 填不动、`close 9×9` 填不动、`close 11×11` 才填上。
**洞必须小于核**。与开运算"灭小白点"完全对称。

### 毕设链路（3.9 = 检测前处理最后一环）

```
灰度图 → GaussianBlur 去噪 → Canny(50,150) 出 1 像素细边
       → MORPH_OPEN 去碎点 → MORPH_CLOSE 补断线 → dilate 加粗 → 找轮廓/数个数
```

Canny 给碎边，形态学把碎边粘成整块、把洞填上——没有这一步，轮廓检测会数出一堆碎片。

### 形态学坑合集

1. **OpenCV 5.0.0 的 `erode` / `dilate` 必须传 `kernel`**，省略直接报错（4.x 可省略默认 3×3）
2. erode/dilate **shape 永远不变**（全黑图腐蚀完还是 (50,50)，只是内容没了）
3. 灰度图也能用：erode=局部 min、dilate=局部 max。**暗块腐蚀后反而扩张**（暗刷子护自己人）
4. `ELLIPSE (5,5)` 不是圆，只有 21 个 1（RECT 25 个）；圆目标别用 RECT，角上会多切

## 十、色彩在 OpenCV 里的速查

### BGR 里各颜色的值

| 颜色 | BGR | HSV（OpenCV） |
|---|---|---|
| 红 | `(0, 0, 255)` | `(0, 255, 255)` |
| 黄 | `(0, 255, 255)` | `(30, 255, 255)` |
| 绿 | `(0, 255, 0)` | `(60, 255, 255)` |
| 青 | `(255, 255, 0)` | `(90, 255, 255)` |
| 蓝 | `(255, 0, 0)` | `(120, 255, 255)` |
| 洋红 | `(255, 0, 255)` | `(150, 255, 255)` |
| 白 | `(255, 255, 255)` | `(0, 0, 255)` |
| 黑 | `(0, 0, 0)` | `(0, 0, 0)` |

### 角度 → OpenCV H

```
H_opencv = 角度 / 2
0°→0   60°→30   120°→60   180°→90   240°→120   300°→150   360°→180
```

---

## 十一、返回值形状速查（最容易混）

| 函数 | 输入 shape | 输出 shape |
|---|---|---|
| `imread`（彩色） | — | `(H, W, 3)` |
| `imread`（灰度） | — | `(H, W)` |
| `cvtColor(BGR2GRAY)` | `(H,W,3)` | **`(H, W)`** |
| `cvtColor(BGR2HSV)` | `(H,W,3)` | `(H,W,3)` |
| `inRange` | `(H,W,3)` | **`(H, W)`** |
| `split` | `(H,W,3)` | 三个 **`(H, W)`** |
| `merge` | 三个 `(H,W)` | `(H,W,3)` |
| `bitwise_and(mask=)` | `(H,W,3)` + `(H,W)` | `(H,W,3)` |
| `imencode` | `(H,W,3)` | **`(N,)` 一维字节** |
| `resize(img, (w2,h2))` | `(H,W,3)` | `(h2, w2, 3)` —— **dsize 是(宽,高)，shape 是(高,宽)** |
| `copyMakeBorder(t,b,l,r)` | `(H,W,3)` | `(H+t+b, W+l+r, 3)` |
| `letterbox(img, 640)` | 任意 | **`(640, 640, 3)` 恒定** |
| `flip` | `(H,W,3)` | `(H,W,3)` **shape 不变** |
| `getRotationMatrix2D` | — | **`(2,3)` float64 矩阵，不是图** |
| `getPerspectiveTransform` | — | **`(3,3)` float64 矩阵，不是图** |
| `warpAffine(img, M, (w2,h2))` | `(H,W,3)` | `(h2, w2, 3)` |
| `warpPerspective(img, M, (w2,h2))` | `(H,W,3)` | `(h2, w2, 3)` |
| `rotate_keep(img, 90)` | `(H,W,3)` | **`(W,H,3)` 长宽互换** |
| `normalize(..., 0, 1)` | `(H,W,3)` uint8 | `(H,W,3)` **uint8（坑）** / 带 `dtype=CV_32F` 则 float32 |
| `img / 255` | `(H,W,3)` uint8 | `(H,W,3)` **float64**；`img.astype(np.float32)/255` 才得 float32 |
| `imdecode` | `(N,)` | `(H,W,3)` |
| `threshold` | `(H,W)` 灰度 | **元组 `(retval, dst)`**：retval 是 **float**，dst 是 `(H,W)`，值只有 0/maxval |
| `adaptiveThreshold` | `(H,W)` 灰度 | **只有 `(H,W)`**（不是元组！） |
| `calcHist` | `(H,W)` 灰度 | **5.0.0：`(256,)` float32** / 4.x：`(256,1)`；`h.sum() == H×W` |
| `equalizeHist` | `(H,W)` 灰度 | `(H,W)` **shape 不变** |
| `createCLAHE` | — | **CLAHE 对象，不是图**（要 `.apply()`，且对象不能直接调用） |
| `clahe.apply` | `(H,W)` 灰度 | `(H,W)` |
| `blur` / `GaussianBlur` / `medianBlur` / `bilateralFilter` | `(H,W)` 或 `(H,W,3)` | **同 shape、同 dtype**，都是拷贝 |
| `Sobel` / `Scharr` / `Laplacian` | `(H,W)` 或 `(H,W,3)` | **同 shape**，dtype 由 `ddepth` 定（**写 `CV_16S`**） |
| `convertScaleAbs` | `CV_16S` 图 | 同 shape **`uint8`**，负值取绝对值 |
| `Canny` | `(H,W)` 或 `(H,W,3)` | **`(H,W)` uint8，值只有 0/255**，只返回一个值 |
| `np.fromfile` | — | `(N,)` |
| 切片 `img[0]` | `(H,W,3)` | **`(W, 3)` 少了第一维** |
| 切片 `img[0:1]` | `(H,W,3)` | `(1, W, 3)` 保留维 |
