#!/usr/bin/env python
# encoding:utf-8
from Base import *


class Aperture(Base):
    def __init__(self, name, modifiers):
        Base.__init__(self)
        self._name = name
        self._modifiers = modifiers
        
    def __repr__(self):
        return "Aperture(%s, %s)" % (self.name(), self.modifiers())

    def jsonObject(self):
        return {
            'class': 'Aperture',
            'name': self.name(),
            'modifiers': self.modifiers(),
        }
        
    def name(self, name = None):
        if name is None:
            assert self._name is not None
            return self._name
        self._name = name
        
    def modifiers(self, modifiers = None):
        if modifiers is None:
            assert self._modifiers is not None
            return self._modifiers
        self._modifiers = modifiers
        
class Circle(Aperture):
    r = re.compile('C,(?P<diameter>\d+)(X(?P<holediameter>\d+))?')
    def __init__(self):
        Aperture.__init__(self)
        
class Rectangle(Aperture):
    r = re.compile('R,(?P<xsize>\d+)X(?P<ysize>\d+)(X(?P<holediameter>\d+))?')
    def __init__(self):
        Aperture.__init__(self)
        
class Obround(Aperture):
    r = re.compile('O,(?P<xsize>\d+)X(?P<ysize>\d+)(X(?P<holediameter>\d+))?')
    def __init__(self):
        Aperture.__init__(self)
        
class Polygon(Aperture):
    r = re.compile('O,(?P<outerdiameter>\d+)X(?P<numberofvertices>\d+)(X(?P<rotation>\d+)(X(?P<holediameter>\d+))?)?')
    def __init__(self):
        Aperture.__init__(self)