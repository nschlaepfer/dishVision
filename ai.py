import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from debug_window import update_counters

# Disable eager execution
tf.compat.v1.disable_eager_execution()

def load_and_preprocess_frame(frame, height, width):
    # Resize the frame
    frame = cv2.resize(frame, (height, width))

    # Convert the frame to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Normalize the pixel values to be in the range [0, 1]
    frame = frame / 255.0

    return frame

def main():
    # Load the I3D model from TensorFlow Hub
    module = hub.Module("https://tfhub.dev/deepmind/i3d-kinetics-400/1")

    # Set the height and width to 224 as the model expects
    height = 224
    width = 224

    # Load the action names from a file
    with open('actions.txt', 'r') as f:
        action_names = [line.strip() for line in f]

    num_frames = 30

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Initialize a list to hold the sequence of frames
    frames = []

    # Initialize counters and previous prediction
    washing_hands_counter = 0
    washing_dishes_counter = 0
    other_actions_counter = 0
    previous_prediction = ""
    predicted_action_name = ""  # Initialize predicted_action_name

    # Open a file for writing the log
    log_file = open('predictions_log.txt', 'w')

    with tf.compat.v1.Session() as sess:  # Use tf.compat.v1.Session() instead of tf.Session()
        sess.run(tf.compat.v1.global_variables_initializer())
        while True:
            # Capture a frame from the webcam
            ret, frame = cap.read()

            # Preprocess the frame
            frame = load_and_preprocess_frame(frame, height, width)

            # Add the frame to the sequence
            frames.append(frame)

            # If we have enough frames, make a prediction
            if len(frames) == num_frames:
                # Convert the list of frames to a numpy array and add an extra dimension for the batch size
                frames_array = np.expand_dims(np.array(frames), axis=0)

                # Pass the preprocessed frames to the model
                logits = module(frames_array)

                # Convert logits to probabilities
                probabilities = tf.nn.softmax(logits)

                # Identify the action with the highest probability
                predicted_action = tf.argmax(probabilities, axis=1)

                # Run the session to compute probabilities and predicted_action
                probabilities_val, predicted_action_val = sess.run([probabilities, predicted_action])

                # Map the predicted action index to its name
                predicted_action_name = action_names[predicted_action_val[0]]

                # Store the current prediction as the previous prediction
                previous_prediction = predicted_action_name

                # Get the probability of the predicted action
                predicted_probability = probabilities_val[0, predicted_action_val[0]]

                # Display the current prediction and its probability on the webcam feed
                cv2.putText(frame, f'{predicted_action_name} ({predicted_probability:.2f})', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Display the previous prediction on the webcam feed
                cv2.putText(frame, f'Previous: {previous_prediction}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # Increment counters if the predicted action is 'washing hands' or 'washing dishes'
                if predicted_action_name == 'washing hands':
                    washing_hands_counter += 1
                elif predicted_action_name == 'washing dishes':
                    washing_dishes_counter += 1
                else:
                    other_actions_counter += 1

                # Update the counters and the debug window
                update_counters(washing_hands_counter, washing_dishes_counter, other_actions_counter, predicted_probability)

                # Clear the frames list to start a new sequence
                frames = []


            # Display the frame
            cv2.imshow('Video', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Close the log file
    log_file.close()

    # Release the webcam and close the windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
