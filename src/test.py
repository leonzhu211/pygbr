#!/usr/bin/env python
# encoding:utf-8

import string
import re
import os
import sys
import glob
import pickle
import shutil

from Processor import *
from Parser import *


def test_file(filename):
    print '=' * 60
    print filename
    f = file(filename, 'rb')
    xparser = Parser(f)
    xprocessor = Processor()
    xprocessor.appendCommandList(xparser.commandList())
    xprocessor.run()
    f.close()

# test_file('../case/1.gbr')


# for gbr in glob.glob("../case/*/*.gbr"):
for gbr in glob.glob("../case/2211Gerber File/*.pho"):
    test_file(gbr)
