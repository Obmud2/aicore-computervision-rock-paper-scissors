import random
import math
from time import time
from enum import IntEnum, Enum
from keras.models import load_model
import cv2
import numpy as np

class RpsGame():
    """Module for RPS game initialisation"""
    def __init__(self):
        # Game variables
        self.user_wins = 0
        self.computer_wins = 0
        self.max_wins = 3 # Game will end when user or player reaches max wins
        self.countdown_duration = 3 # Number of seconds for timer countdown
        #self.ready = False # Flag to determine whether a round is underway

    class Rps(IntEnum):
        """Storage of rps options"""
        ROCK = 1
        PAPER = 2
        SCISSORS = 3
    class Player(Enum):
        """Player types"""
        USER = 1
        COMPUTER = 2

    def __get_winner(self, user_choice, computer_choice):
        """Selects the winner based on user choice and computer choice,
        and returns a string"""
        if user_choice == None or computer_choice == None:
            print("No choice selected")
            return None

        print(f"You have selected {user_choice.name}. Computer has selected {computer_choice.name}.")     
        if user_choice == computer_choice:
            print("Draw")
            return None
        elif (user_choice - computer_choice) % len(self.Rps) == 1:
            print("You win!")
            return self.Player.USER
        elif (computer_choice - user_choice) % len(self.Rps) == 1:
            print("Computer wins!")
            return self.Player.COMPUTER
        else:
            return None
    def __get_computer_choice(self):
        """Choses a random selection from rock paper scissors and returns an
        enum"""
        return self.Rps(random.randint(1,3))
    def __get_user_choice_manual(self):
        """Asks user for input from rock paper scissors, or r p s, and returns
        an enum"""
        while True:
            print("Rock, paper or scissors?")
            user_choice = input()
            user_choice.lower()
            if user_choice in ("r", "rock"):
                return self.Rps.ROCK
            elif user_choice in ("p", "paper"):
                return self.Rps.PAPER
            elif user_choice in ("s", "scissors"):
                return self.Rps.SCISSORS
            else:
                print("Wrong input, try again.")
    def __get_user_choice_prediction(self, frame, model):
        """Get user rps input from camera based on Keras model"""
        confidence_lim = 0.5
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Get prediction from frozen camera display
        resized_frame = cv2.resize(frame, (224, 224),
                                        interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        # Normalize the image
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image
        prediction = model.predict(data, verbose=0)[0]

        print("Rock: " + "{:.2f}".format(prediction[0]) +
              "  Paper: " + "{:.2f}".format(prediction[1]) +
              "  Scissors: " + "{:.2f}".format(prediction[2]) +
              "  Nothing: " + "{:.2f}".format(prediction[3]))

        # Compare prediction to confidence limit
        if (prediction[0] > confidence_lim and
            sum(prediction) - prediction[0] < confidence_lim):
            return self.Rps.ROCK
        elif (prediction[1] > confidence_lim and
              sum(prediction) - prediction[1] < confidence_lim):
            return self.Rps.PAPER
        elif (prediction[2] > confidence_lim and
              sum(prediction) - prediction[2] < confidence_lim):
            return self.Rps.SCISSORS
        else:
            return None
    def __add_score(self, winner):
        """Add score to game total and check for overall winner. Returns True
        and resets scores if maximum score is reached."""
        # Add score
        if winner == self.Player.USER:
            self.user_wins += 1
        elif winner == self.Player.COMPUTER:
            self.computer_wins += 1
        print(f"User: {self.user_wins}, Computer: {self.computer_wins}")
        
        # Check for winner
        if self.user_wins == self.max_wins:
            print("Congratulations, you win!")
            self.user_wins = 0
            self.computer_wins = 0
            return True
        elif self.computer_wins == self.max_wins:
            print("Game over, you lose")
            self.user_wins = 0
            self.computer_wins = 0
            return True
        else:
            return False

    def play_ml(self):
        """Play rps using ml keras model for user input"""
        # Keras model
        model = load_model('KerasModel/keras_model.h5')

        # Load camera
        cap = cv2.VideoCapture(0)

        ready = False
        init_time = None

        while True:
            frame = cap.read()[1]

            if ready:
                cv2.putText(img=frame, text=str(math.ceil(counter)), org=(150, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=6, color=(0, 255, 0),thickness=3)
                counter = self.countdown_duration - (time() - init_time)
            else:
                cv2.putText(img=frame, text="Press 's' to continue", org=(150, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 0),thickness=3)
            
            cv2.imshow('frame', frame)

            # Use 's' key to start round
            if cv2.waitKey(1) & 0xFF == ord('s'):
                ready = True
                counter = self.countdown_duration
                init_time = time()

            # Play round when counter hits 0
            if ready and counter <= 0:
                ready = False
                user_choice = self.__get_user_choice_prediction(frame, model)
                computer_choice = self.__get_computer_choice()
                winner = self.__get_winner(user_choice, computer_choice)
                if self.__add_score(winner):
                    break #if maximum score is reached

        # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

    def play_manual(self):
        """Play rps based on user input"""
        while True:
            user_choice = self.__get_user_choice_manual()
            computer_choice = self.__get_computer_choice()
            winner = self.__get_winner(user_choice, computer_choice)
            if self.__add_score(winner):
                break #if maximum score is reached
