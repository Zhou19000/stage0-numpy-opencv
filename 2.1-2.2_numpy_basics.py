#day1
import numpy as np
#
# a=np.array([1,2,3])
# b=np.array([[1,2,3],
#             [4,5,6]])
# print("a:",a.shape,a.dtype,a.ndim,a.size)
# print("b:",b.shape,b.dtype,b.ndim,b.size)
#
# print(np.zeros((2,3)))
# print(np.ones((3,)))
# print(np.full((2,2),7))
# print(np.arange(6))
# print(np.linspace(0,1,5))
# print(np.random.rand(2,3))
#
#
# img=np.zeros((480,640,3),dtype=np.uint8)
# print("img",img.shape,img.dtype,img.ndim,img.size)

#day01-practice

c=np.ones((3,4))
print("c:",c.shape,c.dtype,c.size)
d=np.random.randint(0,256,(640,480,3),dtype=np.uint8())
print("d:",d.shape,d.dtype,d.size)