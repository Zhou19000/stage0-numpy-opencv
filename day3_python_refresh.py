# def scale(x,factor=2):
#     return int(x*factor)       #y=2x
#
# print(scale(5))        #10
# print(scale(5,3))       #15
#
# nums=[1,2,3,4,5]
# squares=[n**2 for n in nums]    #[2,4,6,8,10]
# evens=[n for n in nums if n%2==0]   #[2,4]
# square2=[]
# for n in nums:
#     square2.append(n**2)  #往末尾塞一个元素
#
# class Dog:
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age
#
#     def bark(self):
#         return f"{self.name}汪！"
# d=Dog("旺财",3)
# print(d.name)
# print(d.bark())
#
# import numpy as np
# from numpy import array
# import numpy
#
#     #写
# with open("test.txt","w",encoding="utf-8")as f:
#     f.write("你好，小哈。\n")
#
# with open("test.txt","r",encoding="utf-8")as f:
#     content=f.read()
# print(content)


#测试题：
def area(w,h=640):
    return w*h

print("area(480)=",area(480))       #307200
print("area(480,800)=",area(480,800))  #384000

nums=list(range(1,21))
multiples3=[n for n in nums if n%3==0]   #[3,6,9,12,15,18]
print("1~20 中 3 的倍数：", multiples3)    #[3,6,9,12,15,18]  有6个数


class Rect:
    def __init__(self,width,height):
        self.width=width
        self.height=height

    def area(self):
        return self.width*self.height

r=Rect(100,200)
print("r.width=",r.width)    #100
print("r面积",r.area())     #20000

import numpy as np
print("numpy版本:",np.__version__)
print("np.zeros((2,3)):\n",np.zeros((2,3)))

with open("day3_note.txt","w",encoding="utf-8") as f:
    f.write("Day3 Python 补缺 完成！\n")
with open("day3_note.txt","r",encoding="utf-8") as f:
    content=f.read()
print(content)
