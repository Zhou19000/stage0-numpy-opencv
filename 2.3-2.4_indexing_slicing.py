import numpy as np

a=np.arange(10)*10
print("原数组",a)

print("a[0]:",a[0])            #0
print("a[-1]:",a[-1])           #90
print("a[2:5]:",a[2:5])           #(20,30,40)
print("a[:3]:",a[:3])           #(0,10,20)
print("a[7:]:",a[7:])           #(70,80,90)
print("a[::3]:",a[::3])           #(0,30,60,90)
print("a[::-1]:",a[::-1])           #(90,80,70,60,50,40,30,20,10,0)

img=np.random.randint(0,256,(480,640,3),dtype=np.uint8)
print("img.shape:",img.shape)      #(480,640,3)
pixel=img[100,300]
print("单个像素:",pixel,pixel.shape)       #shape是(3,)
row=img[100]
print("整行:",row.shape)   #shape是(640,3)
col=img[:,300]
print("整列：",col.shape)    #(480,3)
roi=img[100:200,300:400]
print("ROI:",roi.shape)   #(100,100,3)
blue=img[:,:,0]
print("B通道：",blue.shape)   #(480,640)
corner=img[-100:,-100:]
print("右下角：",corner.shape)  #(100,100,3)
print("add  :", img[None, ...].shape)     #(1,480,640,3)

#注意：
print(img[:, :, 0].shape)   #(480,640)
print(img[:, :, 0:1].shape)  #(480,640,1)




#作业
#1、从 b = np.arange(20) 里取出下标 5 到 12（含 12）
# 想一想，b[5:12] 对不对？该写成什么？
#不对 要写成b[5:13]
#2、用上面的 img，裁出画面正中央的 100×100 区域，打印它的 shape
# （提示：中心点的行是 240、列是 320，然后用切片表达"从哪到哪"）；
#corner1=img[190:290,270:370]
#print(corner1,corner1.shape)     shape是（100,100,3）
#3、预测 应该是被改成白色了。