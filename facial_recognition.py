import cv2
import dlib
from scipy.spatial import distance as dist
import time
import requests

BASE_URL = 'http://127.0.0.1:5000'

# Function to compute the Eye Aspect Ratio (EAR)
def calculate_ear(eye):
    # Compute the euclidean distances between the two sets of vertical eye landmarks (y-coordinates)
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmark (x-coordinates)
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear


# Load dlib's pre-trained face detector and the facial landmarks predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Eye landmark indices from the facial landmarks predictor
LEFT_EYE_LANDMARKS = list(range(42, 48))
RIGHT_EYE_LANDMARKS = list(range(36, 42))

# Constants
EAR_THRESHOLD = 0.2  # Eye Aspect Ratio threshold to detect a blink
CONSECUTIVE_FRAMES = 2 # Number of consecutive frames below EAR threshold to consider a blink

# Blink counters
blink_counter = 0
total_blinks = 0

# Start webcam capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale for better performance in face/eye detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_detector(gray_frame)

    for face in faces:
        # Detect facial landmarks
        landmarks = landmark_predictor(gray_frame, face)

        # Get coordinates for left and right eyes
        left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in LEFT_EYE_LANDMARKS]
        right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in RIGHT_EYE_LANDMARKS]
        
        # get size of head
        head_width = face.width()
        head_height = face.height()
        head_size = head_width * head_height

        try:
            response = requests.post(BASE_URL + '/api/head_size', json={"head_size": head_size})
            response.raise_for_status()  # Check for successful request
        except requests.RequestException as e:
            print(f"Error sending data to Flask API: {e}")


        # Calculate the EAR for both eyes
        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)

        # Average EAR of both eyes
        ear = (left_ear + right_ear) / 2.0

        # Check if EAR is below the blink threshold
        if ear < EAR_THRESHOLD:
            blink_counter += 1
        else:
            # If EAR is above the threshold and we've counted enough consecutive frames, it's a blink
            if blink_counter >= CONSECUTIVE_FRAMES:
                total_blinks += 1
            blink_counter = 0

        # Display the EAR on the frame
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Blinks: {total_blinks}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Head Size: {head_size} px", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw the eyes on the frame
        for (x, y) in left_eye + right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('Face Detection', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()