#!/usr/bin/env python
# encoding:utf-8
from Base import *


class GraphicsObject(Base):
    def __init__(self):
        Base.__init__(self)
        self._level = None

    def __repr__(self):
        return 'GraphicsObject()'

    def pr(self, i):
        self.pri(i)
        print self

    def jsonObject(self):
        return {
            'class': 'GraphicsObject'
        }

    def level(self, level):
        if level is None:
            assert self._level is not None
            return self._level
        self._level = level

    def getType(self):
        assert False

    def isDraw(self):
        return self.getType() == 'Draw'

    def isArc(self):
        return self.getType() == 'Arc'

    def isFlash(self):
        return self.getType() == 'Flash'

    def isRegion(self):
        return self.getType() == 'Region'


class Draw(GraphicsObject):
    def __init__(self, aperture, start, end):
        GraphicsObject.__init__(self)
        self._aperture = aperture
        self._start = start
        self._end = end

    def __repr__(self):
        return 'Draw(%s, %s, %s)' % (self.aperture(), self.start(), self.end())

    def pr(self, i):
        self.pri(i)
        print self

    def jsonObject(self):
        return {
            'class': 'Draw',
            'aperture': self.aperture().jsonObject(),
            'start': self.start().jsonObject(),
            'end': self.end().jsonObject(),
        }

    def aperture(self, aperture=None):
        if aperture is None:
            assert self._aperture is not None
            return self._aperture
        self._aperture = aperture

    def start(self, start=None):
        if start is None:
            assert self._start is not None
            return self._start
        self._start = start

    def end(self, end=None):
        if end is None:
            assert self._end is not None
            return self._end
        self._end = end

    def getType(self):
        return 'Draw'


class Arc(GraphicsObject):
    def __init__(self, aperture, start, end, offset):
        GraphicsObject.__init__(self)
        self._aperture = aperture
        self._start = start
        self._end = end
        self._offset = offset

    def __repr__(self):
        return 'Arc(%s, %s, %s, %s)' % (self.aperture(), self.start(), self.end(), self.offset())

    def pr(self, i):
        self.pri(i)
        print self

    def jsonObject(self):
        return {
            'class': 'Arc',
            'aperture': self.aperture().jsonObject(),
            'start': self.start().jsonObject(),
            'end': self.end().jsonObject(),
            'offset': self.offset().jsonObject(),
        }

    def aperture(self, aperture=None):
        if aperture is None:
            assert self._aperture is not None
            return self._aperture
        self._aperture = aperture

    def start(self, start=None):
        if start is None:
            assert self._start is not None
            return self._start
        self._start = start

    def end(self, end=None):
        if end is None:
            assert self._end is not None
            return self._end
        self._end = end

    def offset(self, offset=None):
        if offset is None:
            assert self._offset is not None
            return self._offset
        self._offset = offset

    def getType(self):
        return 'Ar'


class Flash(GraphicsObject):
    def __init__(self, aperture, point):
        GraphicsObject.__init__(self)
        self._aperture = aperture
        self._point = point

    def __repr__(self):
        return 'Flash(%s, %s)' % (self.aperture(), self.point())

    def pr(self, i):
        self.pri(i)
        print self

    def jsonObject(self):
        return {
            'class': 'Flash',
            'aperture': self.aperture().jsonObject(),
            'point': self.point().jsonObject(),
        }

    def aperture(self, aperture=None):
        if aperture is None:
            assert self._aperture is not None
            return self._aperture
        self._aperture = aperture

    def point(self, point=None):
        if point is None:
            assert self._point is not None
            return self._point
        self._point = point

    def getType(self):
        return 'Flash'


class Segment(Base):
    def __init__(self, start, end):
        Base.__init__(self)
        self._start = start
        self._end = end

    def __repr__(self):
        return 'Segment(%s, %s)' % (self.start(), self.end())

    def pr(self, i):
        self.pri(i)
        print self

    def jsonObject(self):
        return {
            'class': 'Segment',
            'start': self.start().jsonObject(),
            'end': self.end().jsonObject(),
        }

    def start(self, start=None):
        if start is not None:
            self._start = start
        return self._start

    def end(self, end=None):
        if end is not None:
            self._end = end
        return self._end


class LinearSegment(Segment):
    def __init__(self, start, end):
        Segment.__init__(self, start, end)

    def __repr__(self):
        return 'LinearSegment(%s, %s)' % (self.start(), self.end())

    def pr(self, i):
        self.pri(i)
        print self

    def jsonObject(self):
        return {
            'class': 'LinearSegment',
            'start': self.start().jsonObject(),
            'end': self.end().jsonObject(),
        }


class CircularSegment(Segment):
    def __init__(self, start, end, offset):
        Segment.__init__(self, start, end)
        self._offset = offset

    def __repr__(self):
        return 'CircularSegment(%s, %s, %s)' % (self.start(), self.end(), self.offset())

    def pr(self, i):
        self.pri(i)
        print self

    def offset(self, offset=None):
        if offset is None:
            assert self._offset is not None
            return self._offset
        self._offset = offset

    def jsonObject(self):
        return {
            'class': 'CircularSegment',
            'start': self.start().jsonObject(),
            'end': self.end().jsonObject(),
            'offset': self.offset().jsonObject(),
        }


class Contour(Base):
    def __init__(self):
        Base.__init__(self)
        self._segmentList = []

    def __repr__(self):
        return 'Contour(%s)' % (self.segmentList(),)

    def pr(self, i):
        self.pri(i)
        print 'Contour'
        for segment in self.segmentList():
            segment.pr(i+1)

    def jsonObject(self):
        return {
            'class': 'Contour',
            'list': [segment.jsonObject() for segment in self.segmentList()]
        }

    def segmentList(self):
        return self._segmentList

    def appendSegment(self, segment):
        self.segmentList().append(segment)

    def segmentNum(self):
        return len(self.segmentList())

    def firstSegment(self):
        assert self.segmentNum() > 0
        return self.segmentList()[0]

    def lastSegment(self):
        assert self.segmentNum() > 0
        return self.segmentList()[-1]


class Region(GraphicsObject):
    def __init__(self):
        GraphicsObject.__init__(self)
        self._contourList = []

    def __repr__(self):
        return 'Region(%s)' % (self.contourList(),)

    def pr(self, i):
        self.pri(i)
        print 'Region'
        for contour in self.contourList():
            contour.pr(i+1)

    def jsonObject(self):
        return {
            'class': 'Region',
            'list': [contour.jsonObject() for contour in self.contourList()]
        }

    def getType(self):
        return 'Region'

    def contourList(self):
        return self._contourList

    def appendContour(self, contour):
        self.contourList().append(contour)

    def contourNum(self):
        return len(self.contourList())

    def lastContour(self):
        assert self.contourNum() > 0
        return self.contourList()[-1]

    def firstContour(self):
        assert self.contourNum() > 0
        return self.contourList[-1]
