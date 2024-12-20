import face_recognition
import os
import pickle
import time

import socketio
# from flask_socketio import SocketIO
# from api_base import socketio
def train_data():
    print('hello')
    try:
        # start_time = time.time()
        def load_images_from_folder(folder):
            images = []
            labels = []
            for filename in os.listdir(folder):
                img_path = os.path.join(folder, filename)
                if img_path.endswith(".jpg") or img_path.endswith(".png"):
                    images.append(face_recognition.load_image_file(img_path))
                    labels.append(os.path.splitext(filename)[0])

            print(images, labels,'images, labels')
            return images, labels

        def train_face_recognition(data_folder):
            known_faces = []
            known_labels = []

            # total_images = sum(len(files) for _, _, files in os.walk(data_folder))
            # images_processed = 0

            for person_folder in os.listdir(data_folder):
                
                person_path = os.path.join(data_folder, person_folder)
                if os.path.isdir(person_path):
                    images, labels = load_images_from_folder(person_path)
                    for img, label in zip(images, labels):
                        face_encodings = face_recognition.face_encodings(img)
                        if len(face_encodings) > 0:
                            face_encoding = face_encodings[0]
                            known_faces.append(face_encoding)
                            known_labels.append(label)
                        else:
                            print(f"No face found in the image: {label}")
                        # images_processed += 1
                        # progress_percentage = (images_processed / total_images) * 100
                        # socketio.emit('training_progress', {'progress': progress_percentage})
                    
            print(known_faces, known_labels,'known_faces, known_labels')
            return known_faces, known_labels

        # if __name__ == "__main__":
        training_data_folder = os.path.join(os.getcwd(),'datafolder')  #"C:/Users/LENOVO/Desktop/Smart_Attendence_System/datafolder/"
        known_faces, known_labels = train_face_recognition(training_data_folder)
        if known_faces and known_labels:
            with open("trained_data.pkl", "wb") as f:
                pickle.dump((known_faces, known_labels), f)

            print('Training successful')
            return ("Training successful.")
        else:
            print('No training data available.')
            return "No training data available."
  
    except Exception as e:
        return f"Error during training: {str(e)}"


