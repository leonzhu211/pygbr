#!/usr/bin/env python
# encoding:utf-8

from Base import *
from DataBlock import *
from GraphicsObject import *

class Command(Base):
    r_class = re.compile("<class 'Command.(?P<name>[^']*)'>")
    
    def __init__(self, block = None):
        Base.__init__(self)
        self._processor = None
        self._blockList = []
        self._groupDict = None
        if block is not None:
            self.appendBlock(block)
        
    def __repr__(self):
        return '%s(%s)' % (self.className(), self.blockList())

    def className(self):
        m = self.r_class.match(str(self.__class__))
        return m.group('name')
        
    def processor(self):
        return self._processor

    def groupDict(self):
        assert self._groupDict is not None
        return self._groupDict
        
    def graphicsState(self):
        return self.processor().graphicsState()

    def blockList(self):
        return self._blockList

    def attachProcessor(self, processor):
        self._processor = processor

    def graphicsState(self):
        assert self._processor is not None
        return self._processor.graphicsState()
                
    def blockNum(self):
        return len(self.blockList())
        
    def appendBlock(self, block):
        self.blockList().append(block)

    def first(self):
        assert self.blockNum() > 0
        return self.blockList()[0]
    
    def last(self):
        assert self.blockNum() > 0
        return self.blockList()[-1]

    def isExtented(self):
        if self.blockNum() == 0:
            return False
        return self.first().isExtentedStart() and self.last().isExtentedEnd()
        
    def stripExtentedStartEnd(self):
        if not self.isExtented():
            return
        self.first().stripExtentedStart()
        self.last().stripExtentedEnd()
            
    def commandList(self):
        return [D01,D02,D03,Dnn,G01,G02,G03,G74,G75,G36,G37,G04,M02,FS,MO,AD,AM,SR,LP,TF,TA,TD,IN,G54]
        
    def getClass(self):
        assert self.blockNum() > 0
        self.stripExtentedStartEnd()
        
        for cls in self.commandList():
            if cls.r.match(self.first().content()):
                return cls

        return None
        
    def create(self):
        cls = self.getClass()
        #print
        #print self.first()
        #print 'cls:', cls
        if cls is None:
            print self.blockList()
        assert cls is not None
        command = cls()
        for block in self.blockList():
            command.appendBlock(block.clone())
        command.createGroupDict()
        return command

    def reg(self):
        return self.r
        
    def createGroupDict(self):
        assert self.blockNum() > 0
        m = self.reg().match(self.first().content())
        assert m is not None
        self._groupDict = m.groupdict()

    def parseCoordinate(self, val):
        return self.processor().parseCoordinate(val)
        
    def arg(self, name):
        if self.groupDict().has_key(name):
            return self.groupDict()[name]
        return None

    def coordinate(self, name):
        return self.parseCoordinate(self.arg(name))
    
    def integer(self, name):
        return int(self.arg(name),10)
        
    def run(self):
        print self
        print '!!!run failed. virtual method should not be invoked'
        #assert False

class Operation(Command):
    def __init__(self):
        Command.__init__(self)
    
    def g(self):
        return self.arg('g')

    def grun(self):
        if self.g() is None:
            return
        g = self.g()
        if g == '1' or g == '01':
            self.processor().doG01()
        if g == '2' or g == '02':
            self.processor().doG02()
        if g == '3' or g == '03':
            self.processor().doG03()
                
class D01(Operation):
    r = re.compile('(G(?P<g>(1|01|2|02|3|03)))?(X(?P<x>\d+))?(Y(?P<y>\d+))?(I(?P<i>-?\d+))?(J(?P<j>-?\d+))?(D01)?\*')
    def __init__(self):
        Command.__init__(self)

    def x(self):
        return self.coordinate('x')

    def y(self):
        return self.coordinate('y')
        
    def i(self):
        return self.coordinate('i')
        
    def j(self):
        return self.coordinate('j')
        
    def run(self):
        self.grun()
        self.processor().doD01(self.x(), self.y(), self.i(), self.j())

class D02(Operation):
    r = re.compile('(G(?P<g>(1|01|2|02|3|03)))?(X(?P<x>\d+))?(Y(?P<y>\d+))?D02\*')
    def __init__(self):
        Command.__init__(self)

    def g(self):
        return self.arg('g')
        
    def x(self):
        return self.coordinate('x')

    def y(self):
        return self.coordinate('y')
        
    def run(self):
        self.grun()
        self.processor().doD02(self.x(), self.y())
        
class D03(Operation):
    r = re.compile('(G(?P<g>(1|01|2|02|3|03)))?(X(?P<x>\d+))?(Y(?P<y>\d+))?D03\*')
    def __init__(self):
        Command.__init__(self)

    def x(self):
        return self.coordinate('x')
        
    def y(self):
        return self.coordinate('y')
        
    def run(self):
        self.grun()
        self.processor().doD03(self.x(), self.y())
            
class Dnn(Command):
    r = re.compile('D(?P<dcode>\d+)\*')
    def __init__(self):
        Command.__init__(self)

    def dcode(self):
        return self.integer('dcode')
        
    def run(self):
        self.processor().doDnn(self.dcode())

class G01(Command):
    r = re.compile('G01\*')
    def __init__(self):
        Command.__init__(self)
        
    def run(self):
        self.processor().doG01()

class G02(Command):
    r = re.compile('G02\*')
    def __init__(self):
        Command.__init__(self)
    
    def run(self):
        self.processor().doG02()
            
class G03(Command):
    r = re.compile('G03\*')
    def __init__(self):
        Command.__init__(self)

    def run(self):
        self.processor().doG03()

class G74(Command):
    r = re.compile('G74\*')
    def __init__(self):
        Command.__init__(self)

    def run(self):
        self.processor().doG74()
        
class G75(Command):
    r = re.compile('G75\*')
    def __init__(self):
        Command.__init__(self)

    def run(self):
        self.processor().doG75()
        
class G36(Command):
    r = re.compile('G36\*')
    def __init__(self):
        Command.__init__(self)

    def run(self):
        self.processor().doG36()
        
class G37(Command):
    r = re.compile('G37\*')
    def __init__(self):
        Command.__init__(self)

    def run(self):
        self.processor().doG37()
        
class G04(Command):
    r = re.compile('G04(?P<comment>[^\*]*)\*')
    def __init__(self):
        Command.__init__(self)

    def comment(self):
        return self.arg('comment')
                
    def run(self):
        self.processor().doG04(self.comment())

class M02(Command):
    r = re.compile('M02\*')
    def __init__(self):
        Command.__init__(self)
        
    def run(self):
        self.processor().doM02()

class FS(Command):
    r = re.compile('FSLAX(?P<xformat>\d\d)Y(?P<yformat>\d\d)\*')
    def __init__(self):
        Command.__init__(self)

    def xformat(self):
        return self.arg('xformat')
        
    def yformat(self):
        return self.arg('yformat')
        
    def run(self):
        self.processor().doFS(self.xformat(), self.yformat())
        
class MO(Command):
    r = re.compile('MO(?P<unit>IN|MM)\*')
    def __init__(self):
        Command.__init__(self)

    def unit(self):
        return self.arg('unit')
        
    def run(self):
        self.processor().doMO(self.unit())
        
class AD(Command):
    r = re.compile('ADD(?P<dcode>\d+)(?P<name>[^,]+)(,(?P<modifiers>[^\*]+))?\*')
    def __init__(self):
        Command.__init__(self)

    def dcode(self):
        return self.integer('dcode')
        
    def name(self):
        return self.arg('name')
        
    def modifiers(self):
        return self.arg('modifiers')
        
    def run(self):
        self.processor().doAD(self.dcode(), self.name(), self.modifiers())
        
class AM(Command):
    r = re.compile('AM(?P<name>[^\*]+)\*(?P<content>.*)')
    def __init__(self):
        Command.__init__(self)

    def name(self):
        return self.arg('name')
        
    def content(self):
        return self.arg('content')
        
    def run(self):
        self.processor().doAM(self.name(), self.content())
        
class SR(Command):
    r = re.compile('SR(X(?P<xrepeat>\d+)Y(?P<yrepeat>\d+)I(?P<xstep>[\d\.]+)J(?P<ystep>[\d\.]+))?\*')
    def __init__(self):
        Command.__init__(self)

    def xrepeat(self):
        return self.arg('xrepeat')
        
    def yrepeat(self):
        return self.arg('yrepeat')
        
    def xstep(self):
        return self.arg('xstep')
        
    def ystep(self):
        return self.arg('ystep')
        
    def run(self):
        self.processor().doSR(self.xrepeat(), self.yrepeat(), self.xstep(), self.ystep())
        
class LP(Command):
    r = re.compile('LP(?P<polarity>C|D)\*')
    def __init__(self):
        Command.__init__(self)
        
    def polarity(self):
        return self.arg('polarity')

    def run(self):
        return self.processor().doLP(self.polarity())
        
class TF(Command):
    r = re.compile('TF(?P<name>[^,]+)(,(?P<value>[^\*]+))?\*')
    def __init__(self):
        Command.__init__(self)

    def name(self):
        return self.arg('name')
    
    def value(self):
        return self.arg('value')
            
    def run(self):
        self.processor().doTF(self.name(), self.value())
        
class TA(Command):
    r = re.compile('TA(?P<name>[^,]+)(,(?P<value>[^\*]+))?\*')
    def __init__(self):
        Command.__init__(self)
    
    def name(self):
        return self.arg('name')
    
    def value(self):
        return self.arg('value')
        
    def run(self):
        self.processor().doTA(self.name(), self.value())
            
class TD(Command):
    r = re.compile('TD(?P<name>[^,]+)\*')
    def __init__(self):
        Command.__init__(self)

    def name(self):
        return self.arg('name')

    def run(self):
        self.processor().doTD(self.name())

class IN(Command):
    r = re.compile('IN(?P<name>[^\*]+)\*')
    def __init__(self):
        Command.__init__(self)
    
    def name(self):
        return self.arg('name')

    def run(self):
        self.processor().doIN(self.name())
        
class G54(Command):
    r = re.compile('G54D(?P<dcode>[^\*]+)\*')
    def __init__(self):
        Command.__init__(self)
        
    def dcode(self):
        return self.integer('dcode')
        
    def run(self):
        self.processor().doG54(self.dcode())
        
if __name__ == '__main__':
    c = M02()
    print c