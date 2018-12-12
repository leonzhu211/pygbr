#!/usr/bin/env python
# encoding:utf-8

from Base import *
from DataBlock import *
from Command import *

class Parser(Base):
    def __init__(self, stream):
        Base.__init__(self)
        self._stream = stream

    def stream(self):
        assert self._stream is not None
        return self._stream
        
    def read(self, n):
        return self.stream().read(n)

    def seek(self, offset):
        return self.stream().seek(offset)

    def tell(self):
        return self.stream().tell()
        
    def char(self):
        return self.read(1)
    
    def peek(self):
        pos = self.tell()
        c = self.char()
        self.seek(pos)
        return c        
        
    def stripLineFeed(self):
        while True:
            c = self.peek()
            if len(c) == 0:
                break
            if not c in '\r\n':
                break
            self.char()
            
    def peekBlock(self, inExtented):
        block = DataBlock()
        while True:
            self.stripLineFeed()
            c = self.char()
            if len(c) == 0:
                break
            
            block.appendContent(c)
            if c == '*':
                if inExtented or block.isExtentedStart():
                    self.stripLineFeed()
                    if self.peek() == '%':
                        block.appendContent(self.char())
                break
                
        return block

    def blockList(self):
        self.seek(0)
        inExtented = False
        
        while True:
            block = self.peekBlock(inExtented)
            if block.isEmpty():
                break
                
            if not inExtented:
                if block.isExtentedStart() and not block.isExtentedEnd():
                    inExtented = True
            elif inExtented:
                if block.isExtentedEnd():
                    inExtented = False
            
            if not block.isEmpty() and not block.isBlank():
                yield block

    def commandList(self):
        command = None
        
        for block in self.blockList():
            print 'block is:', block
            if block.isExtentedStart():
                print 'command is:', command
                assert command is None
                command = Command(block)
                if block.isExtentedEnd():
                    yield command
                    command = None
                    
            elif block.isExtentedEnd():
                assert command is not None
                command.appendBlock(block)
                yield command
                command = None
            
            else:
                if command is not None:
                    command.appendBlock(block)
                else:
                    command = Command(block)
                    yield command
                    command = None
                
            
    def printBlock(self):
        for block in self.blockList():
            print block

    def printCommand(self):
        for command in self.commandList():
            print command.create()
        
if __name__ == '__main__':
    f = file('../case/1.gbr')
    p = Parser(f)
    p.printCommand()
    