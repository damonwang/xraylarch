#!/usr/bin/env python

import unittest
import code
import ast
import numpy
import os

import larch
from unittest_util import *

class TestLarchEval(TestCase):
    '''testing evaluation of larch code'''

    default_search_groups = ['_sys', '_builtin', '_math']

    def test_while(self):
        '''while loops'''

        self.eval('''
n=0
while n < 8:
    n += 1
''')

        self.assertTrue(self.li.symtable.n == 8)

    def test_for(self):
        '''for loops'''

        self.eval('''
n=0
for i in arange(10):
    n += i
''')

        self.assertTrue(self.li.symtable.n == 45)

    def test_print(self):
        '''print a string'''

        self.eval("print 1")

        self.stdout.close()
        
        with open(self.stdout.name) as inf:
            self.assert_(inf.read() == '1\n')

    def test_cmp(self):
        '''numeric comparisons'''

        self.true("3 == 3")
        self.true("3.0 == 3")
        self.true("3.0 == 3.0")
        self.true("3 != 4")
        self.true("3.0 != 4")
        self.true("3 >= 1")
        self.true("3 >= 3")
        self.true("3 <= 3")
        self.true("3 <= 5")
        self.true("3 < 5")
        self.true("5 > 3")

        self.false("3 == 4")
        self.false("3 > 5")
        self.false("5 < 3")

    def test_bool(self):
        '''boolean logic'''

        self.li('''
yes = True
no = False
nottrue = False
a = arange(7)''')

        self.true("yes")
        self.false("no")
        self.false("nottrue")
        self.false("yes and no or nottrue")
        self.false("yes and (no or nottrue)")
        self.false("(yes and no) or nottrue")
        self.true("yes or no and nottrue")
        self.true("yes or (no and nottrue)")
        self.false("(yes or no) and nottrue")
        self.true("yes or not no")
        self.true("(yes or no)")
        self.false("not (yes or yes)")
        self.false("not (yes or no)")
        self.false("not (no or yes)")
        self.true("not no or yes")
        self.false("not yes")
        self.true("not no")

    def test_bool_coerce(self):
        '''coercion to boolean'''

        self.true("1")
        self.false("0")

        self.true("'1'")
        self.false("''")

        self.true("[1]")
        self.false("[]")

        self.true("(1)")
        self.true("(0,)")
        self.false("()")

        self.true("dict(y=1)")
        self.false("{}")

    def test_assign(self):
        '''variables assignment?'''
        self.li('n = 5')

        self.assertTrue(self.li.symtable.n == 5)

    def test_function_call(self):
        '''built-in functions'''
        self.li('n = [11]')

        self.assertTrue(isinstance(self.n(), numpy.ndarray))
        self.assertTrue(len(self.li.symtable.n) == len([11]))
        self.assertTrue(self.li.symtable.n[0] == 11)

    def test_convenience_imports(self):
        '''convenience imports

        imported functions like math.sqrt into the top level?'''

        self.li('n = sqrt(4)')

        self.assertTrue(self.li.symtable.n == 2)

class TestParse(TestCase):
    '''testing parsing of larch code to ASTs'''

    def test_while(self):
        '''while loops'''

        larchcode = 'n = 5'

        self.assertTrue(ast.dump(ast.parse(larchcode)) == 
                ast.dump(self.li.compile(larchcode)))


if __name__ == '__main__':  # pragma: no cover
    for suite in (TestParse, TestLarchEval):
        suite = unittest.TestLoader().loadTestsFromTestCase(suite)
        unittest.ColoredTextTestRunner(verbosity=2).run(suite)
