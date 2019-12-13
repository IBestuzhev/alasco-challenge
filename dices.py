from random import randint


class GameOver(Exception):
    pass


class Game:

    # TODO: Add docstrings
    # TODO: Add note why int
    amount: int  # cents

    def __init__(self, start_amount: int = 50):
        self.amount = start_amount

    def roll(self) -> int:
        return randint(1, 6) + randint(1, 6)

    def get_prize(self, dices: int, stake: int = 50):
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

    def play(self, stake: int = 50):
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
    print(f'You win and have now {game.amount / 100:.2f} Euros')


if __name__ == '__main__':
    main()
