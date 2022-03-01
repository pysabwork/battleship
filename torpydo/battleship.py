import os
import platform
import random

import colorama
from colorama import Fore, Style

from torpydo.game_controller import GameController
from torpydo.ship import Letter, Position
from torpydo.telemetryclient import TelemetryClient


class Game:
    def __init__(self):
        self.rows = 8
        self.lines = 8
        self.my_fleet = []
        self.enemy_fleet = []

    def main(self):
        print("Starting...")

        TelemetryClient.init()
        TelemetryClient.trackEvent('ApplicationStarted', {'custom_dimensions': {'Technology': 'Python'}})
        colorama.init()
        print(Fore.YELLOW + r"""
                                        |__
                                        |\/
                                        ---
                                        / | [
                                 !      | |||
                               _/|     _/|-++'
                           +  +--|    |--|--|_ |-
                         { /|__|  |/\__|  |--- |||__/
                        +---------------___[}-_===_.'____                 /\
                    ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
     __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
    |                        Welcome to Battleship                         BB-61/
     \_________________________________________________________________________|""" + Style.RESET_ALL)

        self.initialize_game()
        self.start_game()

    @staticmethod
    def display_canon():
        print(Fore.YELLOW + r'''
                              __
                             /  \
                       .-.  |    |
               *    _.-'  \  \__/
                \.-'       \
               /          _/
               |      _  /
               |     /_\
                \    \_/
                 """"""""''' + Style.RESET_ALL)

    @staticmethod
    def display_explosion():
        print(Fore.RED + r'''
            \          .  ./
          \   .:"";'.:..""   /
             (M^^.^~~:.'"").
        -   (/  .    . . \ \)  -
           ((| :. ~ ^  :. .|))
        -   (\- |  \ /  |  /)  -
             -\  \     /  /-
               \  \   /  /''' + Style.RESET_ALL)

    def start_game(self):
        # clear the screen
        cmd = 'cls' if platform.system().lower() == "windows" else 'clear'
        os.system(cmd)

        self.display_canon()

        turn = 1
        while True:
            print()

            # Player turn
            print(f"[Turn={turn}] Player -> it's your turn (Game board from A to H and 1 to {self.lines})")
            user_input = input(f"[Turn={turn}] Player -> Enter coordinates for your shot or 'Q' to quit: ")

            if user_input == 'Q':
                print('BYE!')
                break

            position = self.parse_position(user_input)
            is_hit = GameController.check_is_hit(self.enemy_fleet, position)
            if is_hit:
                self.display_explosion()
                print(Fore.RED + f"[Turn={turn}] Player -> Yeah ! Nice hit !" + Style.RESET_ALL)
            else:
                print(Fore.BLUE + f"[Turn={turn}] Player -> {position} Miss" + Style.RESET_ALL)

            TelemetryClient.trackEvent('Player_ShootPosition',
                                       {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

            # Computer turn
            position = self.get_random_position()
            is_hit = GameController.check_is_hit(self.my_fleet, position)
            print()
            print(f"\t[Turn={turn}] Computer -> Shot in {str(position)}")
            if is_hit:
                print(Fore.RED + f"\t[Turn={turn}] Computer -> Hits your ship!" + Style.RESET_ALL)
                self.display_explosion()
            else:
                print(Fore.BLUE + f"\t[Turn={turn}] Computer -> {str(position)} miss" + Style.RESET_ALL)

            TelemetryClient.trackEvent('Computer_ShootPosition',
                                       {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

            print()
            print('*' * 50)
            turn += 1

    @staticmethod
    def parse_position(user_input: str):
        letter = Letter[user_input.upper()[:1]]
        number = int(user_input[1:])
        position = Position(letter, number)

        return position

    def get_random_position(self):
        letter = Letter(random.randint(1, self.lines))
        number = random.randint(1, self.rows)
        position = Position(letter, number)

        return position

    def initialize_game(self):
        self.initialize_my_test_fleet()
        self.initialize_enemy_fleet()

    def initialize_my_fleet(self):
        self.my_fleet = GameController.initialize_ships()

        print("Please position your fleet (Game board has size from A to H and 1 to 8) :")

        for ship in self.my_fleet:
            print()
            print(f"Please enter the positions for the {ship.name} (size: {ship.size})")

            for i in range(ship.size):
                position_input = input(f"Enter position {i + 1} of {ship.size} (i.e A3):")
                ship.add_position(position_input)
                TelemetryClient.trackEvent('Player_PlaceShipPosition', {
                    'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})

    def initialize_enemy_fleet(self):
        self.enemy_fleet = GameController.initialize_ships()

        self.enemy_fleet[0].positions.append(Position(Letter.B, 4))
        self.enemy_fleet[0].positions.append(Position(Letter.B, 5))
        self.enemy_fleet[0].positions.append(Position(Letter.B, 6))
        self.enemy_fleet[0].positions.append(Position(Letter.B, 7))
        self.enemy_fleet[0].positions.append(Position(Letter.B, 8))

        self.enemy_fleet[1].positions.append(Position(Letter.E, 6))
        self.enemy_fleet[1].positions.append(Position(Letter.E, 7))
        self.enemy_fleet[1].positions.append(Position(Letter.E, 8))
        self.enemy_fleet[1].positions.append(Position(Letter.E, 9))

        self.enemy_fleet[2].positions.append(Position(Letter.A, 3))
        self.enemy_fleet[2].positions.append(Position(Letter.B, 3))
        self.enemy_fleet[2].positions.append(Position(Letter.C, 3))

        self.enemy_fleet[3].positions.append(Position(Letter.F, 8))
        self.enemy_fleet[3].positions.append(Position(Letter.G, 8))
        self.enemy_fleet[3].positions.append(Position(Letter.H, 8))

        self.enemy_fleet[4].positions.append(Position(Letter.C, 5))
        self.enemy_fleet[4].positions.append(Position(Letter.C, 6))

    def initialize_my_test_fleet(self):
        self.my_fleet = GameController.initialize_ships()

        self.my_fleet[0].positions.append(Position(Letter.A, 4))
        self.my_fleet[0].positions.append(Position(Letter.A, 5))
        self.my_fleet[0].positions.append(Position(Letter.A, 6))
        self.my_fleet[0].positions.append(Position(Letter.A, 7))
        self.my_fleet[0].positions.append(Position(Letter.A, 8))

        self.my_fleet[1].positions.append(Position(Letter.B, 6))
        self.my_fleet[1].positions.append(Position(Letter.B, 7))
        self.my_fleet[1].positions.append(Position(Letter.B, 8))
        self.my_fleet[1].positions.append(Position(Letter.B, 9))

        self.my_fleet[2].positions.append(Position(Letter.C, 3))
        self.my_fleet[2].positions.append(Position(Letter.C, 4))
        self.my_fleet[2].positions.append(Position(Letter.C, 5))

        self.my_fleet[3].positions.append(Position(Letter.D, 1))
        self.my_fleet[3].positions.append(Position(Letter.D, 2))
        self.my_fleet[3].positions.append(Position(Letter.D, 3))

        self.my_fleet[4].positions.append(Position(Letter.C, 5))
        self.my_fleet[4].positions.append(Position(Letter.C, 6))


if __name__ == '__main__':
    game = Game
