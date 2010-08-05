#!/usr/bin/env python

from __future__ import with_statement, print_function
import os
import sys
import unittest
import optparse
import code
import tempfile
import pdb
from contextlib import contextmanager
from larch.symboltable import GroupAlias
from unittest_larchEval import TestLarchEval, TestParse
from unittest_SymbolTable import TestSymbolTable
from unittest_util import *
import larch

#------------------------------------------------------------------------------

class TestGroupAlias(TestCase):

    def test_create(self):
        '''construct a group from an object instance'''

        # get a useful backtrace
        # must restore recursion limit or later tests will be VERY odd
        rec_lim = sys.getrecursionlimit()
        sys.setrecursionlimit(35)
        ga = GroupAlias({})
        sys.setrecursionlimit(rec_lim)

#------------------------------------------------------------------------------

class TestLarchImport(TestCase):

    def test_import(self):
        '''import entire python module'''

        self.li("import unittest")

        self.assert_(hasattr(self.li.symtable, 'unittest'))
        self.assert_(hasattr(self.li.symtable.unittest, 'TestCase'))

    def test_import_as(self):
        '''import entire python module as other name'''

        self.li("import unittest as test")

        self.assert_(hasattr(self.li.symtable, 'test'))
        self.assert_(hasattr(self.li.symtable.test, 'TestCase'))

    def test_from_import(self):
        '''import python submodule'''

        self.li("from unittest import TestCase")

        self.assert_(hasattr(self.li.symtable, 'TestCase'))
        self.assert_(hasattr(self.li.symtable.TestCase, 'assert_'))

    def test_from_import_as(self):
        '''import python submodule as other name'''

        self.li("from unittest import TestCase as tc")

        self.assert_(hasattr(self.li.symtable, 'tc'))
        self.assert_(hasattr(self.li.symtable.tc, 'assert_'))

    def test_larch_import(self):
        '''import entire larch module'''

        self.li("import l_random")

        self.assert_(hasattr(self.li.symtable, 'l_random'))
        self.assert_(hasattr(self.li.symtable.l_random, 'weibull'))
        # make sure we didn't take the Python random module
        self.assert_(not hasattr(self.li.symtable.l_random, 'gauss'))

    def test_larch_from_import(self):
        '''import larch submodule'''

        self.li('from l_random import weibull')

        self.assert_(hasattr(self.li.symtable, 'weibull'))
        self.assert_(hasattr(self.li.symtable.weibull, '__call__'))

    def test_larch_from_import_as(self):
        '''import larch submodule as other name'''

        self.li('from l_random import weibull as wb')

        self.assert_(hasattr(self.li.symtable, 'wb'))
        self.assert_(hasattr(self.li.symtable.wb, '__call__'))

    def test_larch_import_error(self):
        '''import larch module with error'''

        larchcode = '''
a =
'''
        with tempfile.NamedTemporaryFile(prefix='larch', delete=False) as outf:
            print(larchcode, file=outf)
            fname = outf.name

        self.assert_(self.li.eval_file(fname))

#------------------------------------------------------------------------------

class TestLarchSource(TestCase):
    '''interpreter can source larch code from strings, files, etc.'''

    def test_push_expr(self):
        '''push expression'''

        self.assert_(self.li.push("1"))

    def test_push_statement(self):
        '''push a statement'''

        self.assert_(self.li.push("a = 1"))

    def test_push_incomplete(self):
        '''push an incomplete construct'''

        self.assert_(not self.li.push("a = "))
        self.assert_(self.li.push("1"))
        #code.interact(local=locals())
        self.assert_(self.li.symtable.a == 1)

    def test_push_SyntaxError(self):
        '''push a syntax error'''

        self.assertRaises(SyntaxError, self.li.push, "1 = a")

    def test_push_buf_local(self):
        '''push buffer is local to larch interpreter instance'''

        li2 = larch.interpreter.Interpreter()
        self.li.push("a = ")

        self.assert_(not hasattr(li2, 'push_buf'))
    
    def test_push_no_indent(self):
        '''non-Pythonic indentation'''

        # FIXME can't handle non-Python indentation yet
        larchcode = '''a = 0
for i in arange(10):
a += i
#endfor'''.splitlines()

        self.assert_(self.li.push(larchcode[0]))
        self.assert_(not self.li.push(larchcode[1]))
        self.li.push(larchcode[2])
        #self.assert_(not self.li.push(larchcode[2]))
        self.assert_(self.li.push(larchcode[3]))

    def test_eval_file(self):
        '''eval a larch file'''

        # FIXME can't handle non-Python indentation yet
        larchcode = '''
a = 0
for i in arange(10):
    a += i
#endfor'''

        fname="testingtmp"
        with open(fname, "w") as outf:
            print(larchcode, file=outf)

        self.assert_(self.li.eval_file(fname))
        self.assert_(self.li.symtable.a == 45)

        os.unlink(fname)

#------------------------------------------------------------------------------

def get_args():
    op = optparse.OptionParser()
    op.add_option('-v', '--verbose', action='count', dest="verbosity")
    options, args = op.parse_args()
    return dict(verbosity=options.verbosity, tests=args)

def run_tests(verbosity=0, tests=[]):
    tests = [ unittest.TestLoader().loadTestsFromTestCase(v) 
            for k,v in globals().items() 
            if k.startswith("Test") and (tests == [] or k in tests)]
    unittest.TextTestRunner(verbosity=verbosity).run(unittest.TestSuite(tests))

if __name__ == '__main__':
    run_tests(**get_args())
