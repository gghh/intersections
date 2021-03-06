import unittest
from intersections import *

def fs(*elems):
    return frozenset(elems)

class testFlatten(unittest.TestCase):
    def test_flatten(self):
        self.assertTrue(flatten([['a', 'b'], ['c', 'd', 'e']]) ==
                        ['a', 'b', 'c', 'd', 'e'])


class testChoice(unittest.TestCase):
    def test_choice(self):
        c2 = choose_n(2, ['a', 'b', 'c'])
        
        self.assertTrue(len(c2) == 3)
        self.assertTrue(['a', 'b'] in c2)
        self.assertTrue(['a', 'c'] in c2)
        self.assertTrue(['b', 'c'] in c2)


class testSubsets(unittest.TestCase):
    def test_allsubsets(self):
        ac = list(allsubsets(['a', 'b', 'c']))
        
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
        lookup = intersLookup({'a': set(['apple', 'banana']),
                               'b': set(['orange', 'apple', 'watermelon']),
                               'c': set(['peach', 'plum', 'pear', 'apple', 'orange'])})
        self.assertTrue(lookup == 
                        {fs('a'): 2, fs('c'): 5, fs('b'): 3, 
                         fs('a','b','c'): 1,
                         fs('a','b'): 1,
                         fs('b','c'): 2, 
                         fs('a','c'): 1})

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
        self.allInters = intersLookup({'a': set(['apple', 'banana']),
                                       'b': set(['orange', 'apple', 'watermelon']),
                                       'c': set(['peach', 'plum', 'pear', 'apple', 'orange'])})

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

class testClean(unittest.TestCase):
    def test_clean3(self):
        level = [[fs('a', 'b'), 42],
                 [fs('b', 'c'), 42],
                 [fs('a', 'c'), 42]]
        fromprevious = [[fs('a', 'b', 'c'), 5]]
        threshold = 44
        updatedlevel, tonext = clean(level, fromprevious, threshold)

        # updatedlevel: 5 items from previous level are spread among
        # elements of current level. Two of them make it to the threshold,
        # the third one doesn't and it's updated to 0.
        self.assertTrue(len(updatedlevel) == len(level))
        self.assertTrue([fs('a', 'b'), 44] in updatedlevel)
        self.assertTrue([fs('b', 'c'), 44] in updatedlevel)
        self.assertTrue([fs('a', 'c'), 0] in updatedlevel)
        
        self.assertTrue(len(tonext) == 1)
        self.assertTrue([fs('a', 'c'), 43] in tonext)

    def test_clean4(self):
        level = [[fs('a', 'b'), 42],
                 [fs('a', 'c'), 42],
                 [fs('a', 'd'), 42],
                 [fs('b', 'c'), 42],
                 [fs('b', 'd'), 42],
                 [fs('c', 'd'), 42]]
        fromprevious = [[fs('a', 'b', 'c'), 5]]
        threshold = 44
        updatedlevel, tonext = clean(level, fromprevious, threshold)

        self.assertTrue(len(updatedlevel) == len(level))
        self.assertTrue([fs('a', 'b'), 44] in updatedlevel)
        self.assertTrue([fs('a', 'c'), 44] in updatedlevel)
        self.assertTrue([fs('a', 'd'), 0] in updatedlevel)
        self.assertTrue([fs('b', 'd'), 0] in updatedlevel)
        self.assertTrue([fs('c', 'b'), 0] in updatedlevel)
        self.assertTrue([fs('c', 'd'), 0] in updatedlevel)

        self.assertTrue(len(tonext) == 4)
        self.assertTrue([fs('a', 'd'), 42] in tonext)
        self.assertTrue([fs('b', 'd'), 42] in tonext)
        self.assertTrue([fs('c', 'b'), 43] in tonext)
        self.assertTrue([fs('c', 'd'), 42] in tonext)

class testExplode(unittest.TestCase):
    def setUp(self):
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

        self.sets = {'a': set(liA), 'b': set(liB), 'c': set(liC), 'd': set(liD)}

    def test_explode_3sets(self):
        sets = {'a': set(['apple', 'banana']),
                'b': set(['orange', 'apple', 'watermelon']),
                'c': set(['peach', 'plum', 'pear', 'apple', 'orange'])}
        
        allInters = intersLookup(sets)
        e = explode(sets.keys(), allInters)
        self.assertTrue(e ==
                        {fs('a'): 1, fs('a','c','b'): 1, fs('c'): 3, fs('b'): 1,
                         fs('c','b'): 1, fs('a','b'): 0, fs('a','c'): 0})

    def test_explode_4sets(self):
        allInters = intersLookup(self.sets)
        e = explode(['a', 'b', 'c', 'd'], allInters)
        self.assertTrue(sorted(e.iteritems(), key=lambda x: x[1]) ==
                        [(fs('a','c','b','d'),   1),
                         (fs('a','c','b'),       2),
                         (fs('a','b','d'),       3),
                         (fs('a','c','d'),       4),
                         (fs('c','b','d'),       5),
                         (fs('a','b'),           6),
                         (fs('a','c'),           7),
                         (fs('a','d'),           8),
                         (fs('b','c'),           9),
                         (fs('b','d'),          10),
                         (fs('c','d'),          11),
                         (fs('a'),              12),
                         (fs('b'),              13),
                         (fs('c'),              14),
                         (fs('d'),              15)])

    def test_explode_4sets_threshold(self):
        allInters = intersLookup(self.sets)
        e = explode(['a', 'b', 'c', 'd'], allInters, threshold=10)
        self.assertTrue(sorted(e.iteritems(),
                               key = lambda x: ''.join(list(x[0]))) ==
                        [(fs('a'),                 16),
                         (fs('a', 'b'),             0),
                         (fs('a', 'b', 'd'),        0),
                         (fs('a', 'c'),            10),
                         (fs('a', 'c', 'b'),        0),
                         (fs('a', 'c', 'b', 'd'),   0),
                         (fs('a', 'c', 'd'),        0),
                         (fs('a', 'd'),            10),
                         (fs('b'),                 17),
                         (fs('b', 'd'),            13),
                         (fs('c'),                 14),
                         (fs('c', 'b'),            11),
                         (fs('c', 'b', 'd'),        0),
                         (fs('c', 'd'),            14),
                         (fs('d'),                 15)])

if __name__ == '__main__':
    unittest.main()
