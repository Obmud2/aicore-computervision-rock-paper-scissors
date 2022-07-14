import math
from time import time
from PIL import Image, ImageDraw
import cv2
from keras.models import load_model
import numpy as np
from manual_rps import Rps, Player, get_computer_choice, get_winner

def play():
    """Play RPS game using camera prediction of user selection"""
    # Game variables
    user_wins = 0
    computer_wins = 0
    max_wins = 3
    countdown_duration = 3
    ready = False

    # Keras model
    model = load_model('KerasModel/keras_model.h5')

    # Load camera
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        I1 = ImageDraw.Draw(frame)
        I1.text((28, 36), "hello world", fill=(255, 0, 0))
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            ready = True
            init_time = time()
            continue

        if ready is True and (time() - init_time < countdown_duration):
            print(countdown_duration - math.floor(time() - init_time))
        elif ready is True:
            user_choice = get_prediction(frame, model)
            computer_choice = get_computer_choice()

            if user_choice is None:
                print("Failed prediction, try again")
            else:
                print(f"You have selected {user_choice.name}. Computer has selected {computer_choice.name}.")
                winner = get_winner(user_choice, computer_choice)

            if winner == Player.USER:
                user_wins += 1
            elif winner == Player.COMPUTER:
                computer_wins += 1

            print(f"User: {user_wins}, Computer: {computer_wins}")

            ready = False

        if user_wins == max_wins:
            print("Congrats, you win!")
            break
        elif computer_wins == max_wins:
            print("Game over, you lose")
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def get_prediction(frame, model):
    """Get user rps input from camera based on Keras model"""
    confidence_lim = 0.5
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Get prediction from frozen camera display
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data, verbose=0)[0]

    print(prediction)

    # Compare prediction to confidence limit
    if prediction[0] > confidence_lim and sum(prediction) - prediction[0] < confidence_lim:
        return Rps.ROCK
    elif prediction[1] > confidence_lim and sum(prediction) - prediction[1] < confidence_lim:
        return Rps.PAPER
    elif prediction[2] > confidence_lim and sum(prediction) - prediction[2] < confidence_lim:
        return Rps.SCISSORS
    else:
        return None
