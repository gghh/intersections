nice_people = ['charline', 'martin', 'benedikt', 'camilla']
rich_people = ['sebastian', 'camilla']
smart_people = ['larry', 'camilla', 'charline', 'gustavo', 'audrey']
tall_people = ['matt', 'sebastian']

def flatten(listlist):
    return [elem for list_ in listlist for elem in list_]

flatten([['a', 'b'], ['c', 'd', 'e']])

def perm(sequence):
    if len(sequence) == 0:
        return [[]]
    else:
        out = []
        for cnt, elem in enumerate(sequence):
            out += map(lambda x: [elem] + x,
                       perm(sequence[:cnt] + sequence[(cnt+1):]))
        return out

perm(['a', 'b', 'c'])

def choose_n(n, srcList):
    if n == 0:
        return [[]]
    else:
        out = []
        for cnt, elem in enumerate(srcList):
            out += map(lambda x: [elem] + x,
                       choose_n(n-1, srcList[(cnt+1):]))
        return out

choose_n(2, ['a', 'b', 'c'])

def allChoices(srcList):
    out = []
    tot = len(srcList)+1
    complem = lambda universe, ensemble: \
        list(set(universe) - set(ensemble))
    complSrcList = lambda ensemble: complem(srcList, ensemble)
    for i in range(1, tot):
        if i > tot / 2: # integer division
            yield map(complSrcList, choose_n(tot - (i + 1), srcList))
        else:
            yield choose_n(i, srcList)

list(allChoices(['a', 'b', 'c']))

def intersLookup(lists):
    toInters = flatten(allChoices(lists.keys()))
    def inters_n(names):
        return reduce(lambda s, t: set(s).intersection(set(t)),
                      [lists[name] for name in names[1:]],
                      lists[names[0]])
    count = lambda (names, inters): (names, len(inters))
    lookup = {}
    for sequence in toInters:
        cardinality = len(inters_n(sequence))
        for variant in perm(sequence):
            lookup['&'.join(variant)] = cardinality
    return lookup

intersLookup({'a': ['apple', 'banana'],
              'b': ['orange', 'apple', 'watermelon'],
              'c': ['peach', 'plum', 'pear', 'apple', 'orange']})


    
g = allChoices(['a', 'b', 'c'])
g.next()
g.next()
g.next()
g.next()

def subints(elem, compl):
    for thing in allChoices(compl):
        yield map(lambda x: elem + x, thing)

g = subints(['a'], ['b', 'c', 'd'])
g.next() # add
g.next() # subtract
g.next() # add
g.next() # it's over

si =  subints(['a', 'c'], ['b', 'd'])
si.next()
si.next()
si.next()

def flip():
    curr = 1
    while True:
        yield curr
        curr *= -1

def o(f, g):
    # function composition
    def helper(x):
        return f(g(x))
    return helper

def inclusionexclusion(elem, compl, allInters):
    currentInters = allInters['&'.join(elem)]
    sign = flip()
    subintValue = \
        sum(map(lambda (sign, value): sign * value,
                zip(sign,
                    map(o(sum, (lambda nodes: 
                                map(lambda node: allInters['&'.join(node)],
                                    nodes))),
                        subints(elem, compl)))))
    return currentInters - subintValue

allInters = intersLookup({'a': ['apple', 'banana'],
                          'b': ['orange', 'apple', 'watermelon'],
                          'c': ['peach', 'plum', 'pear', 'apple', 'orange']})

inclusionexclusion(['a', 'b'], ['c'], allInters)
inclusionexclusion(['a', 'b', 'c'], [], allInters)
inclusionexclusion(['a'], ['b', 'c'], allInters)




for elem in subints(['a'], ['b', 'c']):
    print elem
    print '&'.join(elem)






choose_n(1, ['a', 'b', 'c', 'd'])
choose_n(2, ['a', 'b', 'c', 'd'])
choose_n(3, ['a', 'b', 'c', 'd'])
choose_n(4, ['a', 'b', 'c', 'd'])
