#!/usr/bin/env python
# encoding:utf-8
import string
import re
import os
import sys
import glob
import pickle
import shutil
import json


class Base(object):
    def __init__(self):
        object.__init__(self)
        self.cache = {}

    def pri(self, i):
        print '    ' * i,


def withcache(F):
    # return F
    def new_F(self, *a):
        d = self.cache
        name = F.__name__
        if not d.has_key(name):
            d[name] = {}
        d = d[name]
        for e in a:
            if not d.has_key(e):
                d[e] = {}
            d = d[e]

        if d.has_key(0):
            return d[0]

        r = F(self, *a)
        d[0] = r
        return r
    return new_F


def invalidatecache(F):
    def new_F(self, *a):
        r = F(self, *a)
        self.cache = {}
        return r
    return new_F


def withpickle(F):
    def new_F(self, *a):
        if not GetConfig().with_pickle:
            d = self.cache
            name = F.__name__
            if not d.has_key(name):
                d[name] = {}
            d = d[name]
            for e in a:
                if not d.has_key(e):
                    d[e] = {}
                d = d[e]

            if d.has_key(0):
                return d[0]

            r = F(self, *a)
            d[0] = r
            return r

        if not os.path.isdir('pkl'):
            os.mkdir('pkl')
        filename = 'pkl/'
        filename += '__' + F.__name__ + '.' + '.'.join([str(e) for e in a])

        if self.cache.has_key(filename):
            return self.cache[filename]

        pklfilename = filename + '.pkl'
        #logging.debug('pickle: %s', filename)
        try:
            pkl_file = file(pklfilename, 'rb')
            #logging.debug('pickle found: %s', pklfilename)
            data = pickle.load(pkl_file)
            pkl_file.close()
            self.cache[filename] = data
            return data
        except:
            #logging.debug('pickle new: %s', filename)
            data = F(self, *a)
            #logging.debug('after call: %s', F)
            logging.debug(data)
            self.cache[filename] = data
            try:
                #logging.debug('pickle write: %s', pklfilename)
                pkl_file = file(pklfilename, 'wb')
                pickle.dump(data, pkl_file)
                pkl_file.close()
            except:
                try:
                    os.remove(pklfilename)
                except:
                    pass
            return data
    return new_F


def withpicklepath(path):
    def wrapper(F):
        def new_F(*a):
            if os.path.isfile(path):
                logging.debug("f name: %s, load begin: %s", F.__name__, path)
                pkl_file = file(path, 'rb')
                data = pickle.load(pkl_file)
                pkl_file.close()
                logging.debug("f name: %s, load end: %s", F.__name__, path)
            else:
                logging.debug("f name: %s, dump begin: %s", F.__name__, path)
                data = F(*a)
                pkl_file = file(path, 'wb')
                pickle.dump(data, pkl_file)
                pkl_file.close()
                logging.debug("f name: %s, dump end: %s", F.__name__, path)
            return data
        return new_F
    return wrapper
