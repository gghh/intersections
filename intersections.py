def flatten(listlist):
    return [elem for list_ in listlist for elem in list_]

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

def intersLookup(sets):
    toInters = flatten(allsubsets(sets.keys()))
    def inters_n(names):
        acc = sets[names[0]]
        for name in names[1:]:
            acc = acc.intersection(sets[name])
        return acc
    lookup = {}
    for sequence in toInters:
        cardinality = len(inters_n(sequence))
        lookup[frozenset(sequence)] = cardinality
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

def explode(allNames, allInters, threshold=1):
    explosion = []
    for level in allsubsets(allNames):
        tmp = []
        for elem in level:
            tmp.append([frozenset(elem),
                        inclusionexclusion(elem,
                                           complem(allNames, elem),
                                           allInters)])
        explosion.append(tmp)
    explosion.reverse()
    if threshold == 1:
        return dict(flatten(explosion))
    elif threshold > 1:
        fromprevious = []
        cleanexplosion = []
        for level in explosion:
            updatedlevel, fromprevious = clean(level, fromprevious, threshold)
            cleanexplosion.append(updatedlevel)
        return dict(flatten(cleanexplosion))

def clean(level, fromprevious, threshold):
    updatedlevel = []
    tonext = []
    tmplevel = dict(level)
    # first stage: spread fromprevious on current level
    for elem, size in fromprevious:
        subsets = [(x, y) for (x, y) in level if x.issubset(elem)]
        nsubsets = len(subsets)
        q, r = size / nsubsets, size % nsubsets
        for cnt, (subelem, subelemsize) in enumerate(subsets):
            tmplevel[subelem] += q
            if cnt + 1 <= r:
                tmplevel[subelem] += 1
    # second stage: check if tmplevel elements pass threshold
    for elem, size in tmplevel.iteritems():
        if size < threshold:
            updatedlevel.append([elem, 0])
            tonext.append([elem, size])
        else:
            updatedlevel.append([elem, size])
    return updatedlevel, tonext

if __name__ == '__main__':
    sets = {'a': ['apple', 'banana'],
            'b': ['orange', 'apple', 'watermelon'],
            'c': ['peach', 'plum', 'pear', 'apple', 'orange']}
    allInters = intersLookup(sets)
    e = explode(sets.keys(), allInters)
    print 'Sets:', sets
    print 'Exploded:', e
