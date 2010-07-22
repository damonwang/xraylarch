#!/usr/bin/env python

import unittest
import larch

class TestSymbolTable(unittest.TestCase):

    default_search_groups = ['_sys', '_builtin', '_math']

    def setUp(self):
        self.s = larch.SymbolTable()
        self.g = self.s.create_group(name='g0', x=1, y=2)
        self.s.set_symbol(self.g.__name__, self.g)

    def test_searchGroups(self):
        for g in self.default_search_groups:
            self.assertTrue(hasattr(self.s, g))
        self.assertTrue(self.default_search_groups == 
                self.s.get_symbol('_sys.searchGroups'))

    def test_getSymbol(self):
        self.assertTrue(self.s.g0 == self.s.get_symbol('g0'))

    def test_addTempGroup(self):
        self.assertFalse(self.g.__name__ in self.s._sys.searchGroups)
        self.assertTrue(self.g.__name__ in self.s._subgroups())

    def test_make_group(self):
        self.assertTrue(larch.symboltable.isgroup(self.g))
        self.assertTrue(self.g.__name__ == 'g0')
        self.assertTrue(self.g.x == 1 and self.g.y == 2)

    def test_make_group_with_attr(self):
        self.s.new_group('g1', s='a string', en=722)
        self.assertTrue(self.s.g1.s == 'a string')
        self.assertTrue(self.s.g1.en == 722)

    def test_set_symbol(self):
        for k,v in dict(int_=1, float_=1.0, str_='value of b', 
                dict_={'yes': 1, 'no': 0}, tuple_=(1,2,3),
                func_=lambda x: 1).items():
            self.s.set_symbol('_main.%s' % k, value=v)
            self.assertTrue(self.s.get_symbol('_main.%s' % k) == v)

        # do this separately because == on lists is undefined
        self.s.set_symbol('_main.list_', value=[1, 2, 3])
        for a, b in zip([1, 2, 3], self.s.list_):
            self.assertTrue(a == b)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSymbolTable)
    unittest.TextTestRunner(verbosity=2).run(suite)
