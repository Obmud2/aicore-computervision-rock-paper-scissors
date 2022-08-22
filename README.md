# AiCore Project 1: Computer Vision Rock Paper Scissors

Rock paper scissors game using ML computer vision:
- 

Keras model created using webcam and Teachable Machine.
https://teachablemachine.withgoogle.com

## Set up
Refer to "requirements.txt" for list of dependencies.

## How to play
Run "play.ipynb" file to play. This will import the rps game class and load the two options of play.

### Manual Play
Manual play using keyboard input is initiated with the following command.
``rps.play_manual()``
Select Rock, Paper or Scissors through keyboard input. The game accepts user inputs of, for example, 'r' or 'rock' to select an option.

### ML Play
Machine Learning play using webcam input from the Keras model is initiated with the following command.
``rps.play_ml()``
Follow the instructions on the webcam frame to play. The user input is selected based on the Keras model's confidence according to 4 classifications; Rock, Paper, Scissors or Nothing. The game results are output in the terminal.
The following criteria for selecting the model result is used:
Confidence > 50% AND sum of all other confidence < 50%

## Technologies used:
- Command line
- Git & GitHub
- Python Keras, Conda

## Future improvements
- Improved on-screen messages, including:
    - results of each round
    - computer selection
    - hide webcam between rounds
- Improved Keras model training with greater diversity in training set