"""
Rock paper scissors game
"""

import random
from enum import IntEnum, Enum

class Rps(IntEnum):
    """Storage of rps options"""
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Player(Enum):
    """Player types"""
    USER = 1
    COMPUTER = 2

def get_winner(user_choice, computer_choice):
    """Selects the winner based on user choice and computer choice, and returns a string"""
    if user_choice == computer_choice:
        print("Draw")
        return None
    elif (user_choice - computer_choice) % len(Rps) == 1:
        print("You win!")
        return Player.USER
    elif (computer_choice - user_choice) % len(Rps) == 1:
        print("Computer wins!")
        return Player.COMPUTER
    else:
        return None

def get_computer_choice():
    """Choses a random selection from rock paper scissors and returns an enum"""
    return Rps(random.randint(1,3))

def get_user_choice():
    """Asks user for input from rock paper scissors, or r p s, and returns an enum"""
    while True:
        print("Rock, paper or scissors?")
        user_choice = input()
        user_choice.lower()
        if user_choice in ("r", "rock"):
            return Rps.ROCK
        elif user_choice in ("p", "paper"):
            return Rps.PAPER
        elif user_choice in ("s", "scissors"):
            return Rps.SCISSORS
        else:
            print("Wrong input, try again.")

def play():
    """Play rps based on user input"""
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    print(f"You have selected {user_choice.name}. Computer has selected {computer_choice.name}.")
    get_winner(user_choice, computer_choice)
