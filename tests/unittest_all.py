#!/usr/bin/env python

import sys
import unittest
from larch.symboltable import GroupAlias
from unittest_larchEval import TestLarchEval
from unittest_SymbolTable import TestSymbolTable

class TestGroupAlias(unittest.TestCase):

    def test_create(self):
        '''construct a group from an object instance'''

        # get a useful backtrace
        sys.setrecursionlimit(35)
        ga = GroupAlias({})

if __name__ == '__main__':
    possibles = locals().keys()
    for test in [ t for t in possibles if t.startswith("Test") ]:
        suite = unittest.TestLoader().loadTestsFromTestCase(locals()[test])
        unittest.TextTestRunner(verbosity=2).run(suite)
