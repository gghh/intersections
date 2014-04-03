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
{'a': 1, 'a&c&b': 1, 'c': 3, 'b': 1, 'c&b': 1, 'a&b': 0, 'a&c': 0}
```
See http://gghh.name/dibtp/?p=565 for more details.