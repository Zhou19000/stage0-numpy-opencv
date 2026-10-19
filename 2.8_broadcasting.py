import numpy as np

a=np.array([[1,2,3],
            [4,5,6],])
print(a+10)   #[[11,12,13],[14,15,16]]
print(a*np.array([1,10,100]))  #[[1,20,300],[4,50,600]]
print(a+np.array([[1],[2]]))   #[[2,3,4],[6,7,8]]
print("---- 能否广播 ----")
cases = [((2, 3), (3,)), ((2, 3), (2, 1)), ((480, 640, 3), (3,)),
         ((8, 3, 224, 224), (3, 1, 1)), ((2, 3), (2,)), ((480, 640, 3), (480, 640))]
for sa,sb in cases:
    try :
        print(f"{sa} + {sb}->{(np.ones(sa)+np.ones(sb)).shape}")
    except :
        print(f"{sa} + {sb}->报错")
#((480, 640, 3), (480, 640))报错;((2, 3), (2,))报错
#((2, 3), (3,))->(2,3);((480, 640, 3), (3,))->(480,640,3);((8, 3, 224, 224), (3, 1, 1))->(8, 3, 224, 224)
#((2, 3), (2, 1))->(2,3)
#作业
#有一张 HWC 的 float32 图像 img，shape (4, 5, 3)，值域 0~1。
# 通道均值 mean = [0.485, 0.456, 0.406]，标准差 std = [0.229, 0.224, 0.225]（这是 ImageNet 的标准值，工业界通用）。

#用广播实现 (img - mean) / std；
#如果图像已经转成 CHW 格式 (3, 4, 5)，该怎么写？（提示：通道跑到第 0 维了，mean 要变成 (3, 1, 1)）
#验证：把通道均值本身代进去，结果应该是 0。
img=np.random.rand(4,5,3).astype(np.float32)

print(img.dtype)
#1、
mean=np.array([0.485, 0.456, 0.406],dtype=np.float32)    #shape(3,)
std = np.array([0.229, 0.224, 0.225],dtype=np.float32)    #shape(3,)
img1=(img-mean[None,None,:] )/std[None,None,:]

#2、
img2=np.transpose(img,(2,0,1))    #shape(3,4,5)
img3=(img2-mean[:,None,None] )/std[:,None,None]
#3
check = (mean - mean) / std
print("验证:", check)
print(img1.dtype, img3.dtype)