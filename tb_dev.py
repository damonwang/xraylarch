from __future__ import print_function
import sys
import inspect
import traceback
import pdb
import larch
import os
import tempfile

reload(larch.interpreter)

def f():
    li = larch.interpreter.Interpreter()
    larchcode = '''
def f(x, *args, **kwargs):
    if x < 0:
        raise ValueError
    #endif
    return f(x-1, x, last=x)
#enddef

f(10)'''
    
    with tempfile.NamedTemporaryFile(prefix='larch', delete=False) as outf:
        print(larchcode, file=outf)
        fname = outf.name

    with open(fname) as inf:
        larchcode = inf.readlines()
        print(''.join([ "%s %s" % (i + 1, line) 
            for i, line in enumerate(larchcode)]))
        li(''.join(larchcode), fname=fname)

    os.unlink(fname)
    

f()
#print t
#traceback.print_list(traceback.extract_tb(e[2]))
