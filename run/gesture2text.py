import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
import json

def gesture_to_text():
    model_dict = pickle.load(open('./slangai.p', 'rb')) #do ./run/slangai.p if testing this script
    model = model_dict['model']

    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    # Get the number of features expected by the model
    num_features = model.n_features_in_

    # labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    #             10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
    #             19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
    with open (r'./data/gesture_labels.json') as f:
        labels_dict = json.load(f)
        labels_dict = {int(key): value for key, value in labels_dict.items()}


    sentence = ""
    stable_predicted_letter = None
    letter_stable_start_time = 0

    while True:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()
        cv2.putText(frame, 'Press Q when done! :)', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)


        (H,W, _) = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    mp_hands.HAND_CONNECTIONS,  # hand connections
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction = model.predict([np.asarray(data_aux)])

            # If data_aux has more features, truncate it to match the model's expected number of features
            if len(data_aux) > num_features:
                data_aux = data_aux[:num_features]

            # If data_aux has fewer features, pad it with zeros to match the model's expected number of features
            elif len(data_aux) < num_features:
                while len(data_aux) < num_features:
                    data_aux.append(0)

            predicted_character = labels_dict[int(prediction[0])]

            # Create a black background rectangle for the sentence
            bg_height = 60
            bg_x = 20
            bg_y = H - bg_height - 10
            bg_width = int(cv2.getTextSize(sentence, cv2.FONT_HERSHEY_SIMPLEX, 1.3, 3)[0][0]) + 20

            cv2.rectangle(frame, (bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height), (0, 0, 0), -1)

            # Add the sentence in white letters on the black background
            cv2.putText(frame, sentence, (bg_x + 10, bg_y + bg_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3, cv2.LINE_AA)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)
            # Check if the prediction remains the same for about 1.5 seconds
            if stable_predicted_letter == predicted_character:
                if time.time() - letter_stable_start_time >= 2:
                    sentence += predicted_character
                    letter_stable_start_time = time.time()
            else:
                stable_predicted_letter = predicted_character
                letter_stable_start_time = time.time()

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return sentence #remove if testing this script

# gesture_to_text() #for testing this script, use function in streamlit to test GUI