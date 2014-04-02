import unittest
from intersections import *

class testFlatten(unittest.TestCase):
    def test_flatten(self):
        self.assertTrue(flatten([['a', 'b'], ['c', 'd', 'e']]) ==
                        ['a', 'b', 'c', 'd', 'e'])


class testPerm(unittest.TestCase):
    def test_perm(self):
        p = perm(['a', 'b', 'c'])
        
        self.assertTrue(len(p) == 6)
        self.assertTrue(['a', 'b', 'c'] in p)
        self.assertTrue(['a', 'c', 'b'] in p)
        self.assertTrue(['b', 'a', 'c'] in p)
        self.assertTrue(['b', 'c', 'a'] in p)
        self.assertTrue(['c', 'a', 'b'] in p)
        self.assertTrue(['c', 'b', 'a'] in p)
                    

class testChoice(unittest.TestCase):
    def test_choice(self):
        c2 = choose_n(2, ['a', 'b', 'c'])
        
        self.assertTrue(len(c2) == 3)
        self.assertTrue(['a', 'b'] in c2)
        self.assertTrue(['a', 'c'] in c2)
        self.assertTrue(['b', 'c'] in c2)


class testAllChoices(unittest.TestCase):
    def test_allChoices(self):
        ac = list(allChoices(['a', 'b', 'c']))
        
        self.assertTrue(len(ac) == 3)

        self.assertTrue(map(len, ac) == [3, 3, 1])

        self.assertTrue(['a'] in ac[0])
        self.assertTrue(['b'] in ac[0])
        self.assertTrue(['c'] in ac[0])

        self.assertTrue(['a', 'b'] in ac[1])
        self.assertTrue(['a', 'c'] in ac[1])
        self.assertTrue(['b', 'c'] in ac[1])

        self.assertTrue(['a', 'c', 'b'] in ac[2])

class testIntersLookup(unittest.TestCase):
    def test_intersLookup(self):
        lookup = intersLookup({'a': ['apple', 'banana'],
                               'b': ['orange', 'apple', 'watermelon'],
                               'c': ['peach', 'plum', 'pear', 'apple', 'orange']})
        self.assertTrue(lookup == 
                        {'a': 2, 'c': 5, 'b': 3, 
                         'a&b&c': 1, 'b&c&a': 1, 'c&b&a': 1,
                         'a&c&b': 1, 'b&a&c': 1, 'c&a&b': 1,
                         'b&a': 1, 'a&b': 1,
                         'b&c': 2, 'c&b': 2,
                         'c&a': 1, 'a&c': 1})

class testSubints(unittest.TestCase):
    def test_subints_1(self):
        si = list(subints(['a'], ['b', 'c', 'd']))
        
        self.assertTrue(len(si) == 3)

        self.assertTrue(map(len, si) == [3, 3, 1])

        self.assertTrue(['a', 'b'] in si[0])
        self.assertTrue(['a', 'c'] in si[0])
        self.assertTrue(['a', 'd'] in si[0])

        self.assertTrue(['a', 'b', 'c'] in si[1])
        self.assertTrue(['a', 'b', 'd'] in si[1])
        self.assertTrue(['a', 'c', 'd'] in si[1])

        self.assertTrue(['a', 'c', 'b', 'd'] in si[2])

    def test_subints_2(self):
        si = list(subints(['a', 'c'], ['b', 'd']))

        self.assertTrue(len(si) == 2)

        self.assertTrue(map(len, si) == [2, 1])

        self.assertTrue(['a', 'c', 'b'] in si[0])
        self.assertTrue(['a', 'c', 'd'] in si[0])

        self.assertTrue(['a', 'c', 'b', 'd'] in si[1])
        

class testInclusionExclusion(unittest.TestCase):
    def setUp(self):
        self.allInters = intersLookup({'a': ['apple', 'banana'],
                                       'b': ['orange', 'apple', 'watermelon'],
                                       'c': ['peach', 'plum', 'pear', 'apple', 'orange']})

    def test_inclusionexclusion_1(self):
        self.assertTrue(inclusionexclusion(['a', 'b'],
                                           ['c'],
                                           self.allInters) == 0)

    def test_inclusionexclusion_2(self):
        self.assertTrue(inclusionexclusion(['a', 'b', 'c'],
                                           [],
                                           self.allInters) == 1)

    def test_inclusionexclusion_3(self):
        self.assertTrue(inclusionexclusion(['a'],
                                           ['b', 'c'],
                                           self.allInters) == 1)


if __name__ == '__main__':
    unittest.main()
