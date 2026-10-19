import numpy as np
#
# a=np.arange(12)
# print(a.reshape(3,4).shape)  #(3,4)
# print(a.reshape(2,-1).shape)  #(2,6)
# print(a.reshape(-1,6).shape)  #(2,6)
#
# m=a.reshape(3,4)
# print(m.ravel())    #[0,1,2,3,4,5,6,7,8,9,10,11]
# print(m.flatten().shape)  #(12,)
#
# b=np.arange(6).reshape(2,3)
# print(b)   #[[0,1,2],[3,4,5]]
# print(b.reshape(3,2))   #(3,2)
# print(b.T)   #[[0,3],[1,4],[2,5]]
#
# img=np.zeros((480,640,3),dtype=np.uint8)
# print(img.shape)      #(480,640,3)
# chw=np.transpose(img,(2,0,1))  #(3,480,640)
# nchw=np.expand_dims(chw,axis=0)
# print(nchw.shape)   #(1,3,480,640)
# print(chw[np.newaxis,...])   #(1,3,480,640)
# back=np.squeeze(nchw,axis=0)
# print(back.shape)         #(3,480,640)
# print( np.transpose(back, (1, 2, 0)).shape) #(480,640,3)


# #作业：有一张 (720, 1280, 3) 的 uint8 图像，
# # 把它变成模型输入 (1, 3, 720, 1280)、float32、值域 0~1，
# # 然后再还原回 (720, 1280, 3)，每一步打印 shape 和 dtype。
img1=np.random.randint(0,256,(720,1280,3),dtype=np.uint8)
img2=np.transpose(img1,(2,0,1))   #(3,720,1280)
img3=np.expand_dims(img2,axis=0)     #(1,3,720,1280)
img4=img3.astype(np.float32)/255.0    #这一行出错了 ⚠️
print(img4.shape)
print(img4.dtype)
img5=np.squeeze(img4,axis=0)   #(3,720,1280)
img6=np.transpose(img5,(1,2,0))    #(720,1280,3)
print(img6.shape)    ##(720,1280,3)
print(img6.dtype)   #float32






