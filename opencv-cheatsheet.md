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

## 五、色彩在 OpenCV 里的速查

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

## 六、返回值形状速查（最容易混）

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
| `imdecode` | `(N,)` | `(H,W,3)` |
| `np.fromfile` | — | `(N,)` |
| 切片 `img[0]` | `(H,W,3)` | **`(W, 3)` 少了第一维** |
| 切片 `img[0:1]` | `(H,W,3)` | `(1, W, 3)` 保留维 |
