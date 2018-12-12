#!/usr/bin/env python
# encoding:utf-8
from Base import *
from Point import *


class GraphicsState(Base):
    def __init__(self):
        Base.__init__(self)
        self._coordinateFormat = None
        self._unit = None
        self._currentAperture = None
        self._quadrantMode = None
        self._interpolationMode = None
        self._currentPoint = Point(0.0, 0.0)
        self._stepRepeat = (1, 1, 0, 0)
        self._levelPolarity = 'dark'
        self._regionMode = 'off'

    def coordinateFormat(self, fmt=None):
        if fmt is None:
            assert self._coordinateFormat is not None
            return self._coordinateFormat

        # it is allowed to be set only once
        assert self._coordinateFormat is None
        self._coordinateFormat = fmt

    def unit(self, unit=None):
        if unit is None:
            assert self._unit is not None
            return self._unit
        self._unit = unit

    def currentAperture(self, aperture=None):
        if aperture is None:
            assert self._currentAperture is not None
            return self._currentAperture
        self._currentAperture = aperture

    def quadrantMode(self, mode=None):
        if mode is None:
            assert self._quadrantMode is not None
            return self._quadrantMode
        self._quadrantMode = mode

    def interpolationMode(self, mode=None):
        if mode is None:
            assert self._interpolationMode is not None
            return self._interpolationMode
        self._interpolationMode = mode

    def currentPoint(self, point=None):
        if point is None:
            assert self._currentPoint is not None
            return self._currentPoint
        self._currentPoint = point

    def stepRepeat(self, stepRepeat=None):
        if stepRepeat is None:
            assert self._stepRepeat is not None
            return self._stepRepeat
        self._stepRepeat = stepRepeat

    def levelPolarity(self, polartity=None):
        if polartity is None:
            assert self._levelPolarity is not None
            return self._levelPolarity
        self._levelPolarity = polartity

    def regionMode(self, mode=None):
        if mode is None:
            assert self._regionMode is not None
            return self._regionMode
        self._regionMode = mode

    def setPolarityDark(self):
        self.polarity('dark')

    def setPolarityClear(self):
        self.polarity('clear')

    def isPolarityDark(self):
        return self.polarity() == 'dark'

    def isPolarityClear(self):
        return self.polarity() == 'clear'

    def setRegionModeOn(self):
        self.regionMode('on')

    def setRegionModeOff(self):
        self.regionMode('off')

    def isRegionModeOn(self):
        return self.regionMode() == 'on'

    def isRegionModeOff(self):
        return self.regionMode() == 'off'

    def setInterpolationModeLinear(self):
        self.interpolationMode('linear')

    def setInterpolationModeClockwise(self):
        self.interpolationMode('clockwise')

    def setInterpolationModeCounterclockwise(self):
        self.interpolationMode('counterclockwise')

    def isInterpolationModeLinear(self):
        return self.interpolationMode() == 'linear'

    def isInterpolationModeClockwise(self):
        return self.interpolationMode() == 'clockwise'

    def isInterpolationModeCounterclockwise(self):
        return self.interpolationMode() == 'counterclockwise'

    def isInterpolationModeCircular(self):
        return self.isInterpolationModeClockwise() or self.isInterpolationModeCounterclockwise()

    def setQuadrantModeSingle(self):
        self.quadrantMode('single')

    def setQuadrantModeMulti(self):
        self.quadrantMode('multi')

    def isQuadrantModeSingle(self):
        return self.quadrantMode() == 'single'

    def isQuadrantModeMulti(self):
        return self.quadrantMode() == 'multi'

    def setCurrentAperture(self, aperture):
        self.currentAperture(aperture)

    def setCoordinateFormat(self, fmt):
        self.coordinateFormat(fmt)

    def setUnit(self, unit):
        self.unit(unit)

    @withcache
    def getIntegerDecimalLen(self):
        fmt = self.coordinateFormat()
        assert len(fmt) == 2
        integerLen = int(fmt[0])
        decimalLen = int(fmt[1])
        return (integerLen, decimalLen)

    def parseCoordinate(self, val):
        if val is None:
            return None

        sign = False
        if val[0] == '-':
            sign = True
            val = val[1:]

        integerLen, decimalLen = self.getIntegerDecimalLen()
        totalLen = integerLen + decimalLen
        valLen = len(val)
        paddingVal = '0' * (totalLen - valLen) + val
        intergerPart = paddingVal[0:integerLen]
        decimalPart = paddingVal[integerLen:]
        i = 1.0 * int(intergerPart, 10)
        d = 1.0 * int(decimalPart, 10) / (10 ** decimalLen)
        ret = i + d
        if sign:
            ret *= -1
        return ret


if __name__ == '__main__':
    gs = GraphicsState()
    gs.setCoordinateFormat('24')
    print gs.parseCoordinate('015')
