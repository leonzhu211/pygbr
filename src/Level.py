#!/usr/bin/env python
# encoding:utf-8
from Base import *

class Level(Base):
    def __init__(self, polarity = 'dark'):
        Base.__init__(self)
        
        if polarity.lower() == 'd':
            polarity = 'dark'
        elif polarity.lower() == 'c':
            polarity = 'clear'

        assert polarity.lower() in ('dark', 'clear')
        
        self._polarity = polarity
        self._graphicsObjectList = []

    def __repr__(self):
        return 'Level(%s)' % (self.polarity(),)

    def pr(self, i):
        self.pri(i)
        print self
        for gobject in self.graphicsObjectList():
            gobject.pr(i+1)
        
    def jsonObject(self):
        return {
            'class': 'Level',
            'list': [gobject.jsonObject() for gobject in self.graphicsObjectList()]
        }
        
    def polarity(self, polarity = None):
        if polarity is None:
            return self._polarity
        self._polarity = polarity

    def graphicsObjectList(self):
        return self._graphicsObjectList
        
    def appendGraphicsObject(self, graphicsObject):
        graphicsObject.level(self)
        self.graphicsObjectList().append(graphicsObject)
        
    def graphicsObjectNum(self):
        return len(self.graphicsObjectList())

    def lastGraphicsObject(self):
        assert self.graphicsObjectNum() > 0
        return self.graphicsObjectList()[-1]