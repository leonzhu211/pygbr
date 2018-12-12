#!/usr/bin/env python
# encoding:utf-8
from Base import *


class ApertureTemplate(Base):
    def __init__(self, name, content):
        Base.__init__(self)
        self._name = name
        self._content = content
        