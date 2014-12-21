intersections
=============

Computes intersection explosions.

# How to use it

```
import intersections

sets = {'a': ['apple', 'banana'],
        'b': ['orange', 'apple', 'watermelon'],
        'c': ['peach', 'plum', 'pear', 'apple', 'orange']}
allInters = intersections.intersLookup(sets)
print intersections.explode(sets.keys(), allInters)
```
gives
```
{frozenset(['a', 'c', 'b']): 1,
 frozenset(['a', 'b']): 0,
 frozenset(['a', 'c']): 0,
 frozenset(['c', 'b']): 1,
 frozenset(['a']): 1,
 frozenset(['b']): 1,
 frozenset(['c']): 3}
```
See http://gghh.name/dibtp/?p=565 for more details.