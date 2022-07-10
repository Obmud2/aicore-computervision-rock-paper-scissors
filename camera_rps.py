from manual_rps import Rps
import cv2
from keras.models import load_model
import numpy as np
import math
from time import time

model = load_model('KerasModel/keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def get_prediction():
    """Get user rps input from camera based on Keras model"""
    confidence_lim = 0.5;
    
    cap = cv2.VideoCapture(0)

    init_time = time()
    time_diff = 0
    last_time = None
    countdown_duration = 3

    while (time_diff < countdown_duration): 
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        time_diff = math.floor(time() - init_time)
        if time_diff != last_time:
            last_time = time_diff
            if countdown_duration != time_diff:
                print(countdown_duration - time_diff)
            else:
                print("GO!")
    
    # Get prediction from frozen camera display
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data, verbose=0)[0]

    # Compare prediction to confidence limit
    if prediction[0] > confidence_lim and sum(prediction) - prediction[0] < confidence_lim:
        result = Rps.ROCK
    elif prediction[1] > confidence_lim and sum(prediction) - prediction[1] < confidence_lim:
        result = Rps.PAPER
    elif prediction[2] > confidence_lim and sum(prediction) - prediction[2] < confidence_lim:
        result = Rps.SCISSORS
    else:
        result = None

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    return result