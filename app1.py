'''
class over_loading:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        x = self.x + other.y
        y = self.y + other.x
        return tuple([x,y])

ob1 = over_loading(3, 4)
ob2 = over_loading(5, 8)
print(ob1+ob2)

# creating iterator using __iter__ and __next__
class itr:
    def __iter__(self):
        self.n = 0
        return self
    def __next__(self):
        self.n+=1
        return (self.n*3)%7
ob = itr()
it = iter(ob)
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))

a = [i*2 for i in range(5)]
print(a)

b = list(filter(lambda x:x%3==1 , a))
print(b)
print(issubclass(list,object))

import re
string = "a football"
patten = "\bhow"
x = re.match("foo",string)
if x:
    print("pattern exist")
else:
    print("Not exist")

print(list(map(lambda x:2**x, range(8))))
Sachin's Repo
'''
import redis
from time import sleep

r = redis.Redis(host='localhost', port=6379, db=0)
r.set("foo", "bar")
r.setex("key1", 10, "sahr")
r.hmset("h1:firsst", {"sac": "saha", "class": 2})
print(r.hget("h1:firsst", 'class'))
print(r.get("foo"))
print(r.dbsize())
print(r.ttl("key1"))
sleep(3)
print(r.ttl("key1"))







