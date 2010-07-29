#!/usr/bin/env python

import sys
import unittest
import optparse
from larch.symboltable import GroupAlias
from unittest_larchEval import TestLarchEval
from unittest_SymbolTable import TestSymbolTable
import larch

class TestGroupAlias(unittest.TestCase):

    def test_create(self):
        '''construct a group from an object instance'''

        # get a useful backtrace
        # must restore recursion limit or later tests will be VERY odd
        rec_lim = sys.getrecursionlimit()
        sys.setrecursionlimit(35)
        ga = GroupAlias({})
        sys.setrecursionlimit(rec_lim)

#------------------------------------------------------------------------------

class TestLarchImport(unittest.TestCase):

    def true(self, expr):
        '''assert that larch evaluates expr to True'''

        return self.assertTrue(self.li(expr))

    def false(self, expr):
        '''assert that larch evaluates expr to False'''

        return self.assertFalse(self.li(expr))

    def setUp(self):
        '''creates a larch interpreter'''

        self.li = larch.interpreter.Interpreter()

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

        self.li("import random")

        self.assert_(hasattr(self.li.symtable, 'random'))
        self.assert_(hasattr(self.li.symtable.random, 'weibull'))
        # make sure we didn't take the Python random module
        self.assert_(not hasattr(self.li.symtable.random, 'gauss'))

    def test_larch_from_import(self):
        '''import larch submodule'''

        self.li('from random import weibull')

        self.assert_(hasattr(self.li.symtable, 'weibull'))
        self.assert_(hasattr(self.li.symtable.weibull, '__call__'))

    def test_larch_from_import_as(self):
        '''import larch submodule as other name'''

        self.li('from random import weibull as wb')

        self.assert_(hasattr(self.li.symtable, 'wb'))
        self.assert_(hasattr(self.li.symtable.wb, '__call__'))


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
