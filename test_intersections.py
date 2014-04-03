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

class testExplode(unittest.TestCase):
    def test_explode_3sets(self):
        sets = {'a': ['apple', 'banana'],
                'b': ['orange', 'apple', 'watermelon'],
                'c': ['peach', 'plum', 'pear', 'apple', 'orange']}
        
        allInters = intersLookup(sets)
        e = explode(sets.keys(), allInters)
        self.assertTrue(e ==
                        {'a': 1, 'a&c&b': 1, 'c': 3, 'b': 1,
                         'c&b': 1, 'a&b': 0, 'a&c': 0})

    def test_explode_4sets(self):
        liA = []
        liB = []
        liC = []
        liD = []
        
        liA += [1]
        liB += [1]
        liC += [1]
        liD += [1]
        
        liA += range(2,4)
        liB += range(2,4)
        liC += range(2,4)
        
        liA += range(4,7)
        liB += range(4,7)
        liD += range(4,7)
        
        liA += range(7,11)
        liC += range(7,11)
        liD += range(7,11)
        
        liB += range(11,16)
        liC += range(11,16)
        liD += range(11,16)
        
        liA += range(16,22)
        liB += range(16,22)
        
        liA += range(22, 29)
        liC += range(22, 29)
        
        liA += range(29, 37)
        liD += range(29, 37)
        
        liB += range(37, 46)
        liC += range(37, 46)
        
        liB += range(46, 56)
        liD += range(46, 56)
        
        liC += range(56, 67)
        liD += range(56, 67)
        
        liA += range(67, 79)
        
        liB += range(79, 92)
        
        liC += range(92, 106)
        
        liD += range(106, 121)
        
        allInters = intersLookup({'a': liA, 'b': liB,
                                  'c': liC, 'd': liD})
        e = explode(['a', 'b', 'c', 'd'], allInters)
        self.assertTrue(sorted(e.iteritems(), key=lambda x: x[1]) ==
                        [('a&c&b&d',   1),
                         ('a&c&b',     2),
                         ('a&b&d',     3),
                         ('a&c&d',     4),
                         ('c&b&d',     5),
                         ('a&b',       6),
                         ('a&c',       7),
                         ('a&d',       8),
                         ('b&c',       9),
                         ('b&d',      10),
                         ('c&d',      11),
                         ('a',        12),
                         ('b',        13),
                         ('c',        14),
                         ('d',        15)])

if __name__ == '__main__':
    unittest.main()
