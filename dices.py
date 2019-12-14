from random import randint
from decimal import Decimal


class GameOver(Exception):
    """When user is out of money"""
    pass


class Game:
    """
    This class holds current game state (amount of money left),
    and provides an interface to play next round.
    """
    # We start with 50 cents, so it looks like we can store `0.5`
    # Usually it's not a good design to use `float` for money field
    # There are some precission issues, like `.1 + .2`
    # So for money we can either use `int` and store cents
    # Or use special class `Decimal`
    amount: Decimal

    def __init__(self, start_amount: Decimal = Decimal('0.50')):
        self.amount = start_amount

    def roll(self) -> int:
        """
        Get a result of sum of 2 dices.
        """
        return randint(1, 6) + randint(1, 6)

    def get_prize(self, dices: int, stake: Decimal = Decimal('0.50')):
        """
        Calculate user returns based on his stake and dices result
        """
        modifier = 0
        if 7 <= dices <= 9:
            modifier = 1
        elif dices == 10:
            # We can calculate it like `dices - 8`
            # But I think this is less code and also less readable
            modifier = 2
        elif dices == 11:
            modifier = 3
        elif dices == 12:
            modifier = 4

        return stake * modifier

    def play(self, stake: Decimal = Decimal('0.50')):
        """
        Do the next round of game

        1. Make a stake
        2. Roll the dice
        3. Get the winnings

        Raises `GameOver` error if there are no money left.
        """
        self.amount -= min(stake, self.amount)
        dice_result = self.roll()
        self.amount += self.get_prize(dice_result, stake)
        if self.amount <= 0:
            raise GameOver()


def main():
    game = Game()
    for x in range(1, 1001):
        try:
            game.play()
        except GameOver:
            print(f'You lost all your money on {x} iteration.')
            return
    print(f'You win and have now {game.amount:.2f} Euros')


if __name__ == '__main__':
    main()
