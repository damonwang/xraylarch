#!/usr/bin/env python

import sys
import unittest
from larch.symboltable import GroupAlias

class TestGroupAlias(unittest.TestCase):

    def test_create(self):
        '''construct a group from an object instance'''

        # get a useful backtrace
        sys.setrecursionlimit(35)
        ga = GroupAlias({})

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGroupAlias)
    unittest.TextTestRunner(verbosity=2).run(suite)
