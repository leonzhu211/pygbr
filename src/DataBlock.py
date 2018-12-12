#!/usr/bin/env python
# encoding:utf-8
from Base import *


class DataBlock(Base):
    r_space = re.compile('^\s*$')
    
    def __init__(self, content=''):
        Base.__init__(self)
        self._content = None
        self.content(content)

    def __repr__(self):
        return 'DataBlock("%s")' % (self.content(),)

    def content(self, content = None):
        if content is not None:
            self._content = str(content)
        return self._content
                
    def isEmpty(self):
        return len(self.content()) == 0
        
    def isBlank(self):
        return len(self.content())==1 and self.content()[0] == '*'
        
    def isExtentedStart(self):
        return not self.isEmpty() and self.content()[0] == '%'

    def stripExtentedStart(self):
        if not self.isExtentedStart():
            return
        self.content(self.content()[1:])

    def isExtentedEnd(self):
        return not self.isEmpty() and self.content()[-1] == '%'

    def stripExtentedEnd(self):
        if not self.isExtentedEnd():
            return
        self.content(self.content()[:-1])
            
    def appendContent(self, c):
        self.content(self.content() + c)
        
    def clone(self):
        return DataBlock(self.content())

    def isEmpty(self):
        return self.r_space.match(self.content()) is not None