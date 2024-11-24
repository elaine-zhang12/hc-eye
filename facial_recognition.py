import cv2
import dlib
from scipy.spatial import distance as dist
import time
import requests

BASE_URL = 'http://127.0.0.1:5000'

HEAD_SIZE_LEVELS = {
    "tiny": 5000,
    "small": 7000,       
    "medium": 10000,   
    "large": 15000    
}

HEAD_SIZE_FONTS = {
    "tiny": 32,
    "small": 26,       
    "medium": 21,   
    "large": 16
}

def get_head_size_level(head_size):
    if head_size < HEAD_SIZE_LEVELS["small"]:
        return "tiny"
    elif head_size < HEAD_SIZE_LEVELS["medium"]:
        return "small"
    elif head_size < HEAD_SIZE_LEVELS["large"]:
        return "medium"
    else:
        return "large"


# Load dlib's pre-trained face detector and the facial landmarks predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# track time for head size
head_size_tracking = {}

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

    current_time = time.time()

    for face in faces:
        # Detect facial landmarks
        landmarks = landmark_predictor(gray_frame, face)
        
        # get size of head
        head_width = face.width()
        head_height = face.height()
        head_size = head_width * head_height

        # Determine the level of the current head size
        current_level = get_head_size_level(head_size)

        face_id = (face.left(), face.top(), face.right(), face.bottom())
        if face_id not in head_size_tracking:
            head_size_tracking[face_id] = {
                "level": current_level,
                "last_change_time": current_time
            }

        # Check if the level has changed
        tracked_data = head_size_tracking[face_id]
        if tracked_data["level"] != current_level:
            # Level has changed; reset the timer
            head_size_tracking[face_id] = {
                "level": current_level,
                "last_change_time": current_time
            }
        else:
            # Level remains stable; check duration
            duration = current_time - tracked_data["last_change_time"]
            if duration > 10:  # Level stable for more than 10 seconds
                # Send data to the endpoint
                try:
                    response = requests.post(BASE_URL + '/api/head_size', json={
                        "head_size": head_size,
                        "level": current_level,
                        "font_size": HEAD_SIZE_FONTS[current_level]
                    })
                    response.raise_for_status()
                    print(f"Posted head size: {head_size}, Level: {current_level}")
                except requests.RequestException as e:
                    print(f"Error sending data to Flask API: {e}")

                # Update last_change_time to prevent repeated posts
                head_size_tracking[face_id]["last_change_time"] = current_time

        cv2.putText(frame, f"Head Size: {head_size} px", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()