import numpy as np
a=np.array([[1,5,3],[8,2,6]])
print(a.shape)  #(2,3)

print(a.sum())  #25
print(a.mean())   #4.1666666666666666666666666666667
print(a.max(axis=0))  #(3,) [8,5,6]
print(a.sum(axis=1))   #(2,) [9,16]
print(a.mean(axis=0))   #(3,)  [4.5,3.5,4.5]
print(a.std(axis=1))    #(2,)   [1.633,2.494]

print(a.sum(axis=1).shape)   #(2,)
print(a.sum(axis=1,keepdims=True).shape)   #(2,1)

imgs=np.random.randint(low=0,high=256,size=(4,8,8,3))
print(imgs.shape)   #(4,8,8,3)
print(imgs.mean(axis=(0,1,2)).shape)   #(3,)
print(imgs.mean(axis=0).shape)    #(8,8,3)
print(imgs.max(axis=-1).shape)    #(4,8,8)
print(imgs.std(axis=(1,2)).shape)   #(4,3)

print(imgs.sum().dtype)   #int64⚠️sum 不升级，mean 必升级。
print(imgs.mean().dtype)  #float64

#作业
#有 10 张 (32, 32, 3) 的图像组成的 batch，shape (10, 32, 32, 3)，像素是 0~255 的随机整数：

#求出整个数据集每个通道的均值和标准差（各是长度 3 的数组）；
#求出每张图片的整体平均亮度（长度 10 的数组）；
#说明这两步各自压掉了哪些 axis（文字回答就行，这是笔记要求的一部分）

img=np.random.randint(low=0,high=256,size=(10,32,32,3))
#1
img_mean=img.mean(axis=(0,1,2))
img_std=img.std(axis=(0,1,2))
#2
img_mean1=img.mean(axis=(1,2,3))
#3 问题1中压掉了维度0,1,2。 问题2中压掉了维度1,2,3
