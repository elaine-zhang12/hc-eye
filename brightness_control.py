import cv2
import dlib
from scipy.spatial import distance as dist
import time
import requests
import screen_brightness_control as sbc

BASE_URL = 'http://127.0.0.1:5000'

# set initial brightness to 100%
sbc.set_brightness(100)

# Function to compute the Eye Aspect Ratio (EAR)
def calculate_ear(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# Load dlib's pre-trained face detector and facial landmarks predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Eye landmark indices
LEFT_EYE_LANDMARKS = list(range(42, 48))
RIGHT_EYE_LANDMARKS = list(range(36, 42))

# Constants
EAR_THRESHOLD = 0.2
CONSECUTIVE_FRAMES = 2

# Blink counters
blink_counter = 0
total_blinks = 0
previous_blinks = 0

# Timer settings
last_timer_check = time.time()
TIMER_INTERVAL = 300  # 5 minutes
prior_brightness = 100

# Start webcam capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray_frame)

    for face in faces:
        landmarks = landmark_predictor(gray_frame, face)

        # Get coordinates for left and right eyes
        left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in LEFT_EYE_LANDMARKS]
        right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in RIGHT_EYE_LANDMARKS]

        # Calculate EAR for both eyes
        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Check if EAR is below the blink threshold
        if ear < EAR_THRESHOLD:
            blink_counter += 1
        else:
            if blink_counter >= CONSECUTIVE_FRAMES:
                total_blinks += 1
            blink_counter = 0

        # Display EAR and blink count on the frame
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Blinks: {total_blinks}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Timer check for 5-minute intervals
    current_time = time.time()
    if current_time - last_timer_check >= TIMER_INTERVAL:
        # Check if blink count has significantly decreased
        if previous_blinks > 0 and total_blinks < 0.5 * previous_blinks:
            if prior_brightness <= 25:
                brightness = 25
            else:
                brightness = prior_brightness - 15
                prior_brightness = brightness

            sbc.set_brightness(brightness)

        # Update previous blink count and reset current count
        previous_blinks = total_blinks
        total_blinks = 0
        last_timer_check = current_time

    # Show the frame
    cv2.imshow('Blink Detection and Brightness Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()









# # importing the module
# import screen_brightness_control as sbc

# # get current brightness value
# current_brightness = sbc.get_brightness()
# print(current_brightness)

# # # get the brightness of the primary display
# # primary_brightness = sbc.get_brightness(display=0)
# # print(primary_brightness)

# #set brightness to 50%
# sbc.set_brightness(25)
 
# print(sbc.get_brightness())