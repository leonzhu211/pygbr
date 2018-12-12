#!/usr/bin/env python
# encoding:utf-8
from Base import *

class Point(Base):
    def __init__(self, x, y):
        Base.__init__(self)
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y
        
    def __repr__(self):
        return 'Point(%s,%s)' % (self.x(), self.y())    
        
    def jsonObject(self):
        return {
            'class': 'Point',
            'x': self.x(),
            'y': self.y(),
        }