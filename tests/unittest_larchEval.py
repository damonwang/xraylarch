#!/usr/bin/env python

import unittest
import larch
import code
import ast
import numpy

class TestLarchEval(unittest.TestCase):
    '''testing evaluation of larch code'''

    default_search_groups = ['_sys', '_builtin', '_math']

    def true(self, expr):
        '''assert that larch evaluates expr to True'''

        return self.assertTrue(self.li(expr))

    def false(self, expr):
        '''assert that larch evaluates expr to False'''

        return self.assertFalse(self.li(expr))

    def setUp(self):
        self.li = larch.Interpreter()
        self.n = lambda : self.li.symtable.n

    def test_while(self):
        '''while loops'''

        self.li('''
n = 0
while n < 8:
    n += 1
''')
        self.li('n+=1')

        print self.li.symtable.n
        self.assertTrue(self.li.symtable.n == 8)

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

class TestParse(unittest.TestCase):
    '''testing parsing of larch code to ASTs'''

    def setUp(self):
        self.li = larch.Interpreter()

    def test_while(self):
        '''while loops'''

        larchcode = 'n = 5'

        self.assertTrue(ast.dump(ast.parse(larchcode)) == 
                ast.dump(self.li.compile(larchcode)))


if __name__ == '__main__':
    for suite in (TestParse, TestLarchEval):
        suite = unittest.TestLoader().loadTestsFromTestCase(suite)
        unittest.ColoredTextTestRunner(verbosity=2).run(suite)
