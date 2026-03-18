import random
import time
import argparse

class Die:
    def __init__(self):
        self.sides = 6

    def roll(self):
        return random.randint(1, self.sides)

class Player:
    def __init__(self, name):
        self.name = name
        self.total = 0

    def decide(self, turn_total):
        choice = input("(r)oll or (h)old? ").lower()
        while choice not in ("r", "h"):
            choice = input("Please enter r or h: ").lower()
        return choice


class ComputerPlayer(Player):
    def decide(self, turn_total):
        hold_limit = min(25, 100 - self.total)

        if turn_total >= hold_limit:
            print(f"{self.name} decides to hold.")
            return "h"
        else:
            print(f"{self.name} decides to roll.")
            return "r"


class PlayerFactory:
    @staticmethod
    def create_player(kind, name):
        if kind == "human":
            return Player(name)
        elif kind == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Player type must be 'human' or 'computer'.")


class PigGame:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.die = Die()
        self.current = 0
        random.seed(0)

    def play(self):
        print("Welcome to Pig! First to 100 wins.")
        while True:
            player = self.players[self.current]
            turn_total = 0
            print(f"\n--- {player.name}'s turn ---")

            while True:
                choice = player.decide(turn_total)

                if choice == "r":
                    roll = self.die.roll()
                    print(f"{player.name} rolled {roll}")

                    if roll == 1:
                        print("Rolled a 1! Turn over, no points added.")
                        turn_total = 0
                        break
                    else:
                        turn_total += roll
                        print(f"Turn total: {turn_total}, Game total: {player.total}")

                else:  
                    player.total += turn_total
                    print(f"Holding. {player.name}'s new total: {player.total}")
                    break

            if player.total >= 100:
                print(f"\n*** {player.name} wins with {player.total} points! ***")
                return player.name

            
            self.current = 1 - self.current


class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play(self):
        print("Timed game activated (1 minute limit).")
        while True:
            if time.time() - self.start_time > 60:
                print("\nTime is up! Determining winner...")
                p1, p2 = self.game.players
                if p1.total > p2.total:
                    print(f"{p1.name} wins with {p1.total} points!")
                    return p1.name
                elif p2.total > p1.total:
                    print(f"{p2.name} wins with {p2.total} points!")
                    return p2.name
                else:
                    print("It's a tie!")
                    return "tie"

            winner = self.game.play()
            return winner


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", default="human", choices=["human", "computer"])
    parser.add_argument("--player2", default="human", choices=["human", "computer"])
    parser.add_argument("--timed", action="store_true")

    args = parser.parse_args()

    p1 = PlayerFactory.create_player(args.player1, "Player 1")
    p2 = PlayerFactory.create_player(args.player2, "Player 2")

    game = PigGame(p1, p2)

    if args.timed:
        game = TimedGameProxy(game)

    game.play()