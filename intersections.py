def flatten(listlist):
    return [elem for list_ in listlist for elem in list_]

def _perm():
    memo = {}
    def inner(sequence):
        if len(sequence) == 0:
            return [[]]
        elif frozenset(sequence) in memo:
            return memo[frozenset(sequence)]
        else:
            out = []
            for cnt, elem in enumerate(sequence):
                out += map(lambda x: [elem] + x,
                           perm(sequence[:cnt] + sequence[(cnt+1):]))
            memo[frozenset(sequence)] = out
            return out
    return inner

perm = _perm()

def choose_n(n, srcList):
    if n == 0:
        return [[]]
    else:
        out = []
        for cnt, elem in enumerate(srcList):
            out += map(lambda x: [elem] + x,
                       choose_n(n-1, srcList[(cnt+1):]))
        return out

def complem(universe, ensemble):
    return list(set(universe) - set(ensemble))

def allsubsets(srcList):
    out = []
    tot = len(srcList)+1
    complSrcList = lambda ensemble: complem(srcList, ensemble)
    for i in range(1, tot):
        if i > tot / 2: # integer division
            yield map(complSrcList, choose_n(tot - (i + 1), srcList))
        else:
            yield choose_n(i, srcList)

def intersLookup(lists):
    toInters = flatten(allsubsets(lists.keys()))
    def inters_n(names):
        return reduce(lambda s, t: set(s).intersection(set(t)),
                      [lists[name] for name in names[1:]],
                      lists[names[0]])
    lookup = {}
    for sequence in toInters:
        cardinality = len(inters_n(sequence))
        for variant in perm(sequence):
            lookup[frozenset(variant)] = cardinality
    return lookup

def subints(elem, compl):
    for thing in allsubsets(compl):
        yield map(lambda x: elem + x, thing)

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
    currentInters = allInters[frozenset(elem)]
    sign = flip()
    subintValue = \
        sum(map(lambda (sign, value): sign * value,
                zip(sign,
                    map(o(sum, (lambda nodes: 
                                map(lambda node: allInters[frozenset(node)],
                                    nodes))),
                        subints(elem, compl)))))
    return currentInters - subintValue

def explode(allNames, allInters):
    out = []
    for cardinality in allsubsets(allNames):
        tmp = []
        for elem in cardinality:
            tmp.append([frozenset(elem),
                        inclusionexclusion(elem,
                                           complem(allNames, elem),
                                           allInters)])
        out.append(tmp)
    out.reverse()
    return dict(flatten(out))

if __name__ == '__main__':
    sets = {'a': ['apple', 'banana'],
            'b': ['orange', 'apple', 'watermelon'],
            'c': ['peach', 'plum', 'pear', 'apple', 'orange']}
    allInters = intersLookup(sets)
    e = explode(sets.keys(), allInters)
    print 'Sets:', sets
    print 'Exploded:', e
