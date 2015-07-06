#!/bin/python
import re
from dt import *
import operator
import os
import pdb
b=pdb.set_trace

DICT='/usr/share/dict/words'
DIR='/home/jhogan/tmp/gut'

  
class book:
    def __init__(self, path):
        self._path=path
        self._title=''
        self._author=''
        self._editor=''
        self._rdate=''
        self._lang=''
        self._cset=''

        self.load()

    def load(self):
        file=open(self._path)
        while True:
            lines=file.readlines(50)
            if not lines:break

            for line in lines:
                if line.startswith('***'): return
                line=line.lower().strip()
                arr=line.split(':', 1)
                if len(arr) >= 2:
                    key=arr[0].strip(); val=arr[1].strip()
                    if key == 'title': self._title=val
                    if key == 'author': self._author=val
                    if key == 'editor': self._editor=val
                    if key == 'release date': self._rdate=val
                    if key == 'language': self._lang=val
                    if key == 'character set encoding': self._cset=val

    def title(self): return self._title
    def author(self): return self._author
    def editor(self): return self._editor
    def rdate(self): return self._rdate
    def lang(self): return self._lang
    def cset(self): return self._cset
    def path(self): return self._path

    def __repr__(self):
        r =  self.title() + '\t' + self.author() + '\t' + \
                self.editor() + '\t' + self.rdate() + '\t' + \
                self.lang() + '\t' + self.cset() + '\t'    
        if r.strip() == '': return ''
        return r
        
class books(col):
    def __init__(self, path, onadd):
        col.__init__(self)
        self._onadd=onadd
        i=0
        for r,d,fs in os.walk(path):
            # if i == 100: return
            for f in fs:
                f=os.path.join(r,f)
                if not f.endswith('.txt'): continue
                if f.endswith('-8.txt'): continue
                if f.endswith('-0.txt'): continue
                self.add(f)
            i+=1

    def add(self, o):
        if type(o) == str:
            o=book(o)
        col.add(self, o)
        self._onadd(o)

    def __repr__(self):
        bs=''
        for b in self: bs += repr(b) + '\n'
        return  bs
            
def books_add(b):
    print repr(b)
    

def maketable(f):
    bs = books(DIR, onadd=books_add)


def wordcount():
    d={}
    hyph=None

    for word in open(DICT): d[word.strip().lower()]=0

    for r,d0,fs in os.walk(DIR):
        for f in fs:
            f=os.path.join(r,f)
            if not f.endswith('.txt'): continue
            if f.endswith('-8.txt'): continue
            if f.endswith('-0.txt'): continue
            try: 
                if book(f).lang() != 'english': continue
                file = open(f)
                print f
            except:
                print "ERR: %s" % f
                continue
            while 1:
                lines = file.readlines(100000)
                if not lines: break

                for line in lines:
                        
                    words= [w.lower().replace('_', '') for w in re.findall("\w+", line)]

                    i=0; cnt=len(words)
                    for word in words:
                        if i+1==cnt:
                            if word.endswith('-'):
                                hyph=word.replace('-','')
                                b()
                            else: hyth=None

                        if i==0 and hyph != None:
                            word = hyph + word
                            
                        try:             
                            d[word] += 1
                        except KeyError: 
                            pass

    for kvp in sorted(d.iteritems(), key=operator.itemgetter(1)):
        print kvp

maketable('/home/jhogan/tmp/guttbl')
