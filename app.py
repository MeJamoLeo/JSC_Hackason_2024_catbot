import numpy as np
import cv2 as cv
from cnn import model  # Correct import

# Initialize webcam
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is not captured correctly
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Resize the frame to match model input size (e.g., 48x48)
    resized_frame = cv.resize(gray, (48, 48))
    
    # Normalize the pixel values to range [0, 1]
    normalized_frame = resized_frame / 255.0

    # Reshape to match the model input shape (e.g., [1, 48, 48, 1])
    input_frame = np.expand_dims(normalized_frame, axis=0)
    input_frame = np.expand_dims(input_frame, axis=-1)

    # Emotion mapping dictionary
    emotions = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
    
    # Predict emotion using the model
    predictions = model.predict(input_frame)
    predicted_emotion_index = np.argmax(predictions)  # Get the emotion with the highest probability
    predicted_emotion = emotions[predicted_emotion_index]  # Map the index to the emotion label

    # Add the prediction to the frame for display
    emotion_text = f"Emotion: {predicted_emotion}"
    cv.putText(frame, emotion_text, (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

    # Display the resulting frame with emotion
    cv.imshow('Emotion Detection', frame)

    # Break loop on 'q' key press
    if cv.waitKey(1) == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
