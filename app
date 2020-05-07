from math import *
'''
a = "xy"
print(int(3.455))
print(a.__len__())
print("hello World")
print("hey", 40, "hello")
#name = input("Enter your name: ")
#print(name)
li = ["a", "b", ["x", "y"]]
li.append(5)
print(li[2][1])
def f1():
    print("my first function")
f1()
arr = [1, 2, 3, 4]
for i in range(arr.__len__()):
    print(arr[i])
    try:
    #a = 10/0
    print(int(input("Enter a number: ")))
except ZeroDivisionError as err:
    print(err)
except ValueError as err:
    print(err)
    
    
    #global a
a=1
def inc_a():
    #global a
    a=1
    a+=1
    print(a)
    def x():
        a=4
        print(a)
    x()
    print(a)
inc_a()
s = "sachin"
print(s.index('hi'))
'''
import os
a = {2,3,1,4,'fhf'}
b={2,1,'fhf',5,'sach'}
c=a.difference(b)
print(c)
try:
    d = {2:'hello',5:'hii'}
    print(d[0])
except KeyError as err:
    print("Invalid Key", err)
print(os.getcwd())
os.chdir("C:\\Users\\HP\\PycharmProjects\\P1")
print(os.getcwd())
try:
    t=t*3
except NameError as err:
    print(err)

