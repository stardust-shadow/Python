#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-05 10:31
# @Author  : tang
# @File    : test.py
# @Software: PyCharm


class Test:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def methd():
        print "mthe"


class Aests(Test):
    def eat(self):
        print("eat happy %s" % self.a)

    def dee(self, x):
        print(self.b, x)


xxx = Test(1, 2, 3)

mytest = Aests(1, 2, 3)

mytest.eat()
mytest.dee("bbbbb")
