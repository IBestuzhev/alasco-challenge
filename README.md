# alasco-challenge
Test task for Alasco backend developer

## Rectangles

Determine if 2 rectangles intersect

### Solution 

I implemented the code with Python 3.7. 
Earlier version will not work as I used `@dataclass` decorator.

I added both `Pipfile` and `requirements.txt`.
I prefer to use `pipenv` as it does more things at once, like requirements and venv management and custom scripts.

However first 2 task does not need any external dependencies.

You need `pipenv sync` or `pipenv install` only for 3rd task. If you use script like `pipenv run [command]` it will create virtualenv for you, but will not install packages. So maybe it's good to run `pipenv sync` at the start.

Anyway, `pipenv` is optional and I describe both ways.

Task solution is in `rectangles.py` file.

To run it you need to pass it 8 integers. These are 4 points for 2 rectangles - top-left and bottom-right point for each.

Example of run:

```bash
> python rectangles.py 0 10 10 0 -2 6 12 4
Rectangle(top_left=Point(x=0, y=10), bottom_right=Point(x=10, y=0))
Rectangle(top_left=Point(x=-2, y=6), bottom_right=Point(x=12, y=4))
Overlap True

> python rectangles.py -5 10 -3 0 -2 6 12 4
Rectangle(top_left=Point(x=-5, y=10), bottom_right=Point(x=-3, y=0))
Rectangle(top_left=Point(x=-2, y=6), bottom_right=Point(x=12, y=4))
Overlap False
```

or you can run via `pipenv`:

```bash
> pipenv run rectangles 0 10 10 0 -2 6 12 4
Rectangle(top_left=Point(x=0, y=10), bottom_right=Point(x=10, y=0))
Rectangle(top_left=Point(x=-2, y=6), bottom_right=Point(x=12, y=4))
Overlap True
```

For this task there are also unit tests.

Launch them with

```
> pipenv run rect_test
```

or
```
> python -m unittest rectangles
```


## Dice

We should check if we have a good chance of winning in a game with two dice. The values of
the dice are added. We start the game with 50c. The profit is computed with the following table

| Sum       | Payback    | Profit     |
| --------- | ---------- | ---------- |
| 12        | 4x input   | +1,50 Euro |
| 11        | 3x input   | +1,00 Euro |
| 10        | 2x input   | +0,50 Euro |
| 7,8,9     | input back | +0,00 Euro |
| 2,3,4,5,6 | none       | -0,50 Euro |

Is it good to take part in this game? Try in a loop with 1000 iterations, if you lose or win in the long run. You can simulate the dice with random numbers.

### Solution

This solution has no external dependencies to install with `pip` or `pipenv`.

To run the simulation use

```
pipenv run dices
```

or

```
python dices.py
```

Also I'd like to point out that this looks like task for probabilities calculations. And so it can be solved with analysis instead of emulation.

I added 2 files - IPython notebook `dices.ipynb` and the same notebook in markdown format - [dices.md](dices.md).

There are calculations to show that chance of winning each round is 16.67% only, while chance to lose is 41.67%.

## Currency converter

1. Draw a design of the user interface for a simple currency converter, which can convert Euro, Dollar and Yen in all directions.
2. Implement a server-side currency converter, which converts Euro, Dollars and Yen in all directions. Use a Python Framework of your choice.

Please use html for the general markup, css for styling and javascript for frontend logic if needed.

If you have enough time, use exchange rates of an API of your choice.
Please add documentation to your code.


### Solution (TODO)

I have much more experience with `Django`. But this task looks like API proxy mostly. And I am sure that async frameworks are way better for this kind of tasks.

The server is built with `aiohttp`.

You need to install dependencies with `pipenv sync`. Or you can use `pip install -r requirements.txt`. Be sure to use `venv` if you are not using `pipenv`.

To run the server us

```
pipenv run currency
```

or

```
python currency.py
```

By default it runs the server on `8080`. You can customize it via `PORT` environment variable.

Now you can open http://localhost:8080/ in browser and check the currency converter.

Also you can check the list of API endpoints (only one for now) [via swagger](http://localhost:8080/api/doc/).

The frontend is done with `vue.js`. There are some notes what I would like to implement in future if this would be a longer challenge or real project.

For API to get rates I use [exchangeratesapi.io](https://exchangeratesapi.io/)