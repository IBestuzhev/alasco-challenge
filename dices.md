# Dices task

I think this is more task on calculating possible probabilities, so it can be solved with analysis, not simulation.

First of all, let's calculate how many ways we can get each result


```python
import itertools
from collections import defaultdict

res_dict = defaultdict(list)

for dices in itertools.product(range(1, 7), repeat=2):
    res_dict[sum(dices)].append(dices)
    
dict(res_dict)
```




    {2: [(1, 1)],
     3: [(1, 2), (2, 1)],
     4: [(1, 3), (2, 2), (3, 1)],
     5: [(1, 4), (2, 3), (3, 2), (4, 1)],
     6: [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1)],
     7: [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)],
     8: [(2, 6), (3, 5), (4, 4), (5, 3), (6, 2)],
     9: [(3, 6), (4, 5), (5, 4), (6, 3)],
     10: [(4, 6), (5, 5), (6, 4)],
     11: [(5, 6), (6, 5)],
     12: [(6, 6)]}



Now let's calculate the chance of each result. For single dice each side has `1/6` probability.

For pair of dices it's `(1/6) * (1/6)`.


```python
chance = (1 / 6) ** 2

chance_dict = {k: len(v) * chance for k, v in res_dict.items()}

chance_dict
```




    {2: 0.027777777777777776,
     3: 0.05555555555555555,
     4: 0.08333333333333333,
     5: 0.1111111111111111,
     6: 0.1388888888888889,
     7: 0.16666666666666666,
     8: 0.1388888888888889,
     9: 0.1111111111111111,
     10: 0.08333333333333333,
     11: 0.05555555555555555,
     12: 0.027777777777777776}



Let's be sure we are correct in our calculations by this simple check


```python
sum(chance_dict.values())
```




    1.0000000000000002



So let's calculate chances of win, loose, or draw


```python
win = [10, 11, 12]
draw = [7, 8, 9]
loose = [2, 3, 4, 5, 6]

print(f'Win:   {100 * sum(chance_dict[d] for d in win):.2f}%')
print(f'Draw:  {100 * sum(chance_dict[d] for d in draw):.2f}%')
print(f'Loose: {100 * sum(chance_dict[d] for d in loose):.2f}%')
```

    Win:   16.67%
    Draw:  41.67%
    Loose: 41.67%
    

Now it's visible that you are less likely to win.
