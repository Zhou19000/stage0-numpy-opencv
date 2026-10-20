"""
第 3 章 OpenCV · 3.1 读写显示图像与测试图的生成

规则：每个 print 之前先写 # 预测: xxx，写不出来就写 # 预测: ⚠️
写完全部预测后再运行，最后对照实际输出。
"""
import os
import numpy as np
import cv2

# ============================================================
# Part 0  先造图（照抄教材，不许改）
# ============================================================
def make_scene(h=240, w=320):
    img = np.zeros((h, w, 3), np.uint8)
    img[:, :, 0] = np.linspace(40, 200, h, dtype=np.uint8)[:, None]  # B 通道渐变
    img[:, :, 1] = 90
    img[:, :, 2] = 60
    cv2.rectangle(img, (30, 40), (130, 140), (0, 0, 255), -1)        # 红色矩形
    cv2.circle(img, (220, 90), 45, (0, 255, 255), -1)                # 黄色圆
    cv2.rectangle(img, (170, 160), (290, 220), (0, 200, 0), -1)      # 绿色矩形
    cv2.putText(img, "OpenCV", (20, 200), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2)
    return img


scene = make_scene()

# 【0-1】造出来的图长什么样
# 预测: scene.shape = (240,320,3)
# 预测: scene.dtype = uint8
# ⚠️预测: scene[10, 20] 大概是什么值？（提示：第 10 行是渐变的顶端，B 通道接近 40） [46,90,60]
# 预测: scene[10, 20, 2]（蓝还是红？）红色。因为OpenCV默认是BGR通道，2维是R


# 【0-2】这一行是重点，看懂它你在第 2 章就毕业了
# img[:, :, 0] = np.linspace(40, 200, h, dtype=np.uint8)[:, None]
# ⚠️预测: np.linspace(40, 200, 240).shape  = (240,)【第三个参数是点的个数】
# ⚠️预测: np.linspace(40, 200, 240)[:, None].shape =(240,1)
# 预测: 为什么要加 [:, None]？不加会怎样？（一句话说明）
#【[:, None] 的本质是把数组的最后一维从“240”变成“1”，让它变成可拉伸的那个 1。】

# ============================================================
# Part 1  存图 / 读图
# ============================================================
cv2.imwrite("scene.png", scene)

# 【1-1】读回来还是不是同一张
img = cv2.imread("scene.png")
# ⚠️预测: type(img) = numpy.ndarray【是类型 不是元素类型】
# 预测: img.shape = (240,320,3)
# 预测: img.dtype = uint8
# 预测: np.array_equal(img, scene) = ?（True / False，说明理由）
# True 两者是等价的

# 【1-2】换成 jpg 会怎样
cv2.imwrite("scene_q90.jpg", scene, [cv2.IMWRITE_JPEG_QUALITY, 90])
jpg_img = cv2.imread("scene_q90.jpg")
# 预测: np.array_equal(jpg_img, scene) = False 因为存在压缩
# ⚠️预测: jpg_img.shape 和 scene.shape 一样吗？ 一样
# 【jpg 是有损压缩，丢的是“像素值精度”，不是“尺寸”。
# 图像还是 240 行 320 列 3 通道，只是每个像素的数值变了（比如原本 200 变成 197）。
# shape 由图像的尺寸决定，与压缩方式无关。】
# 预测: 文件大小 scene.png vs scene_q90.jpg 哪个大？scene_q90.jpg大
# ⚠️【不要记“jpg 一定更小”，要记“看内容选格式”：
# 照片 → jpg（省空间）
# 截图/图标/示意图/合成图 → png（无损且更小）】

# 【1-3】读成灰度
gray = cv2.imread("scene.png", cv2.IMREAD_GRAYSCALE)
# 预测: gray.shape = (240,320)
# 预测: gray.ndim = 2
# 预测: 彩色图的三维里，丢掉的是哪一维？（用"最后一个/第一个/中间"回答）最后一个
#

# ============================================================
# Part 2  易错点：读不到文件返回 None
# ============================================================
missing = cv2.imread("no_such_file.jpg")
# 预测: missing = ?（会抛异常吗？）会返回None
# ⚠️预测: missing 的 type 是什么？NoneType
# ⚠️预测: 下一行 print(missing.shape) 会报什么错？（写出异常类型名）AttributeError


# ============================================================
# Part 3  中文路径（Windows 必踩）
# ============================================================
# 【3-1】先用普通 imwrite 试试中文名
if os.path.exists("测试图.png"):
    os.remove("测试图.png")          # 先删掉上次跑出来的，否则看不出 imwrite 到底成没成
ret = cv2.imwrite("测试图.png", scene)
print("imwrite 返回值:", ret, " 文件真的存在?", os.path.exists("测试图.png"))
# ⚠️ 实测：返回 False，文件根本没生成！imwrite 遇中文路径会静默失败。
# 所以下面 np.fromfile 会报 FileNotFoundError —— 这不是 bug，是 imwrite 没写成。
# 修正：用 tofile 造这个文件（tofile 支持中文路径）
if not os.path.exists("测试图.png"):
    ok0, buf0 = cv2.imencode(".png", scene)
    buf0.tofile("测试图.png")

# 【3-2】用 imread 读中文名
img_cn_direct = cv2.imread("测试图.png")
# 预测: img_cn_direct = ?（能读到吗？可能是 None）读不到

# 【3-3】正确解法：字节层 + 图像层 拆开
data = np.fromfile("测试图.png", dtype=np.uint8)
img_cn = cv2.imdecode(data, cv2.IMREAD_COLOR)
# 预测: data.shape = ?（这是几维的？里面是什么？）一维数组
# 预测: img_cn.shape = (240,320,3)
# 预测: np.array_equal(img_cn, scene) = True

# 【3-4】写中文名的正确姿势
ok, buf = cv2.imencode(".png", scene)
#buf 的名称叫 buffer缓冲区，它的性质是：
#buf 就是一个 .png 文件的内容，只不过内容存放在内存里，而不是硬盘上。
buf.tofile("另存为.png")
# 预测: ok = ?（True / False）true
# 预测: buf 是什么类型？（ndarray? bytes?）ndarray
# 预测: buf.shape =(N，) 【是一维的】
# 预测: 两个函数 cv2.imencode / np.fromfile 谁负责"编码"，谁负责"读字节"？
#cv2.imencode 编码；np.fromfile是读字节

# ============================================================
# Part 4  显示（本机有图形界面，可以真跑）
# ============================================================
# 【4-1】先预测，再取消下面三行的注释运行
# 预测: 如果不写 cv2.waitKey(0)，窗口会怎样？ 快速的运行完毕后退出
# 预测: waitKey(0) 里的 0 是什么意思？ 一直等待
# cv2.imshow("scene", scene)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# ============================================================
# Part 5  自己算，不查笔记
# ============================================================
# 【5-1】一张手机拍的照片：宽 4000 像素、高 3000 像素、彩色。
# 预测: 用 cv2.imread 读出来的 shape =(3000,4000,3)
# 预测: 如果加 cv2.IMREAD_GRAYSCALE 读，shape = (3000,4000)
# 预测: 如果转成 CHW（PyTorch 要的格式），shape = (3,3000,4000)

# 【5-2】img.shape = (720, 1280, 3)，那么 img[0] 是什么形状？img[:, 0] 是什么形状？
# ⚠️预测: img[0].shape = (1280,3)
# ⚠️预测: img[:, 0].shape = (720,3)


# ============================================================
# 下面这一行开始，运行你的全部代码
# ============================================================
print("=== Part 0 ===")
print("0-1 shape:", scene.shape, "dtype:", scene.dtype)
print("0-1 pixel:", scene[10, 20])
print("0-2 linspace:", np.linspace(40, 200, 240).shape,
      np.linspace(40, 200, 240)[:, None].shape)

print("=== Part 1 ===")
print("1-1", type(img), img.shape, img.dtype, np.array_equal(img, scene))
print("1-2 jpg equal:", np.array_equal(jpg_img, scene), jpg_img.shape)
print("1-2 size png:", os.path.getsize("scene.png"),
      "jpg:", os.path.getsize("scene_q90.jpg"))
print("1-3 gray:", gray.shape, gray.ndim)

print("=== Part 2 ===")
print("2 missing:", missing, type(missing))
try:
    print(missing.shape)
except Exception as e:
    print("2 error:", type(e).__name__, e)

print("=== Part 3 ===")
print("3-2 direct:", img_cn_direct if img_cn_direct is None else img_cn_direct.shape)
print("3-3 data:", data.shape, "img_cn:", img_cn.shape,
      "equal:", np.array_equal(img_cn, scene))
print("3-4 ok:", ok, "buf type:", type(buf), "buf shape:", buf.shape)

print("=== Part 5 ===")
demo = np.zeros((720, 1280, 3), np.uint8)
print("5-2 demo[0].shape:", demo[0].shape, "demo[:,0].shape:", demo[:, 0].shape)
