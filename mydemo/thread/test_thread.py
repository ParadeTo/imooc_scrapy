# -*- coding: utf-8 -*-

import _thread as thread, time, random
def threadFunc(a = None, b = None, c = None, d = None):
    print (time.strftime('%H:%M:%S', time.localtime()), a)
    time.sleep(1)
    print (time.strftime('%H:%M:%S', time.localtime()), b)
    time.sleep(1)
    print (time.strftime('%H:%M:%S', time.localtime()), c)
    time.sleep(1)
    print (time.strftime('%H:%M:%S', time.localtime()), d)
    time.sleep(1)
    print (time.strftime('%H:%M:%S', time.localtime()), 'over')

# thread.start_new_thread(threadFunc, (3, 4, 5, 6))	# 创建线程，并执行threadFunc函数。
# time.sleep(5)

# import thread, time, random

count = 0
lock = thread.allocate_lock()  # 创建一个琐对象


def threadTest():
    global count, lock
    lock.acquire()  # 获取琐

    for i in range(10000):
        count += 1

    lock.release()  # 释放琐


for i in range(10):
    thread.start_new_thread(threadTest, ())
time.sleep(3)
print (count)