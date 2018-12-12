#!/usr/bin/env python
# encoding:utf-8

from Base import *
from GraphicsState import *
from Aperture import *
from ApertureTemplate import *
from GraphicsObject import *
from Level import *

class Processor(GraphicsState):
    def __init__(self):
        GraphicsState.__init__(self)
        self._apertureTemplateDict = {}
        self._apertureDict = {}
        self._commandList = []
        self._levelList = []

    def commandList(self):
        return self._commandList
                
    def appendCommand(self, command):
        command = command.create()
        command.attachProcessor(self)
        self.commandList().append(command)

    def appendCommandList(self, commandList):
        for command in commandList:
            self.appendCommand(command)

    def levelList(self):
        return self._levelList
        
    def appendLevel(self, level):
        self.levelList().append(level)

    def levelNum(self):
        return len(self.levelList())
    
    def firstLevel(self):
        assert self.levelNum() > 0
        return self.levelList()[0]
            
    def lastLevel(self):
        assert self.levelNum() > 0
        return self.levelList()[-1]

    def printGraphicsObject(self):
        print
        for level in self.levelList():
            level.pr(0)

        print
        jsonObject = self.jsonObject()
        print json.dumps(jsonObject, indent=4, ensure_ascii=False, sort_keys=True, encoding='gbk')
        

    def jsonObject(self):
        return {
            'class': 'image',
            'list': [level.jsonObject() for level in self.levelList()],
        }
        
    def run(self):
        for command in self.commandList():
            print command
            command.run()
    
        self.printGraphicsObject()
        
    def x(self, x):
        if x is None:
            return self.currentPoint().x()
        return x

    def y(self, y):
        if y is None:
            return self.currentPoint().y()
        return y
        
    def putApertureTemplate(self, dcode, apertureTemplate):
        self._apertureTemplateDict[dcode] = apertureTemplate
    
    def getApertureTemplate(self, dcode):
        if not self._apertureTemplateDict.has_key(dcode):
            assert False
            return None
        return self._apertureTemplateDict[dcode]
        
    def putAperture(self, dcode, aperture):
        self._apertureDict[dcode] = aperture
        
    def getAperture(self, dcode):
        if not self._apertureDict.has_key(dcode):
            assert False
            return None
        return self._apertureDict[dcode]

    # invoked by doXXX
    def lastContour(self):
        level = self.lastLevel()
        region = level.lastGraphicsObject()
        assert region.isRegion()
        if region.contourNum() == 0:
            contour = Contour()
            region.appendContour(contour)
        else:
            contour = region.lastContour()
        return contour
        
    def makeLinearContourSegment(self, x, y):
        print 'makeLinearContourSegment', x, y
        contour = self.lastContour()
        segment = LinearSegment(self.currentPoint(), Point(x, y))
        contour.appendSegment(segment)
                
    def makeCircularContourSegment(self, x, y, i, j):
        print 'makeCircularContourSegment', x, y, i, j 
        contour = self.lastContour()
        segment = CircularSegment(self.currentPoint(), Point(x, y), Point(i, j))
        contour.appendSegment(segment)

    def makeDraw(self, x, y):
        print 'makeDraw', x, y
        level = self.lastLevel()
        gobject = Draw(self.currentAperture(), self.currentPoint(), Point(x, y))
        level.appendGraphicsObject(gobject)
        
    def makeArc(self, x, y, i, j):
        print 'makeArc', x, y, i, j
        level = self.lastLevel()
        gobject = Arc(self.currentAperture(), self.currentPoint(), Point(x, y), Point(i, j))
        level.appendGraphicsObject(gobject)
        
    def closeContour(self, x, y):
        contour = self.lastContour()
        segment = LinearSegment(self.currentPoint(), Point(x, y))
        contour.appendSegment(segment)
        
    def flash(self, x, y):
        print 'flash', x, y
        level = self.lastLevel()
        gobject = Flash(self.currentAperture(), Point(x, y))
        level.appendGraphicsObject(gobject)

    # command
    def doD01(self, x, y, i, j):
        print 'doD01', x, y, i, j
        x = self.x(x)
        y = self.y(y)
        
        if self.isRegionModeOn():
            if self.isInterpolationModeLinear():
                self.makeLinearContourSegment(x, y)
            elif self.isInterpolationModeCircular():
                self.makeCircularContourSegment(x, y, i, j)
            else:
                assert False
        elif self.isRegionModeOff():
            if self.isInterpolationModeLinear():
                self.makeDraw(x, y)
            elif self.isInterpolationModeCircular():
                self.makeArc(x, y, i, j)
            else:
                assert False
        else:
            assert False
            
        self.currentPoint(Point(x,y))

    def doD02(self, x, y):
        print 'doD02', x, y
        x = self.x(x)
        y = self.y(y)
        
        if self.isRegionModeOn():
            self.closeContour(x, y)
            
        self.currentPoint(Point(x, y))

    def doD03(self, x, y):
        print 'doD03', x, y
        x = self.x(x)
        y = self.y(y)
        if self.isRegionModeOn():
            assert False
        elif self.isRegionModeOff():
            self.flash(x, y)
        else:
            assert False
            
    def doDnn(self, dcode):
        print 'doDnn',dcode
        aperture = self.getAperture(dcode)
        assert aperture is not None
        self.setCurrentAperture(aperture)
        
    def doG01(self):
        print 'doG01'
        self.setInterpolationModeLinear()
        
    def doG02(self):
        print 'doG02'
        self.setInterpolationModeClockwise()
        
    def doG03(self):
        print 'doG03'
        self.setInterpolationModeCounterclockwise()
        
    def doG74(self):
        print 'doG74'
        self.setQuadrantModeSingle()

    def doG75(self):
        print 'doG75'
        self.setQuadrantModeMulti()

    def doG36(self):
        print 'doG36'
        self.setRegionModeOn()
        level = self.lastLevel()
        region = Region()
        level.appendGraphicsObject(region)
        
    def doG37(self):
        print 'doG37'
        self.setRegionModeOff()
        
    def doG04(self, comment):
        print 'doG04', comment
        
    def doM02(self):
        print 'doM02'

    def doFS(self, xformat, yformat):
        assert xformat == yformat
        self.setCoordinateFormat(xformat)

    def doMO(self, unit):
        self.setUnit(unit)

    def doAD(self, dcode, name, modifiers):
        print 'doAD', dcode, name, modifiers
        aperture = Aperture(name, modifiers)
        self.putAperture(dcode, aperture)

    def doAM(self, name, content):
        print 'doAM', name, content
        apertureTemplate = ApertureTemplate(name, content)
        self.putApertureTemplate(name, apertureTemplate)
        
    def doSR(self, xrepeat, yrepeat, xstep, ystep):
        print 'doSR', xrepeat, yrepeat, xstep, ystep

    def doLP(self, polarity):
        print 'doLP', polarity
        level = Level(polarity)
        self.appendLevel(level)

    def doTF(self, name, value):
        print 'doTF', name, value
        
    def doTA(self, name, value):
        print 'doTA', name, value
        
    def doTD(self, name):
        print 'doTD', name

    def doIN(self, name):
        print 'doIN', name
        
    def doG54(self, dcode):
        print 'doG54', dcode
        aperture = self.getAperture(dcode)
        assert aperture is not None
        self.setCurrentAperture(aperture)