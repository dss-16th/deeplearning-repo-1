"""
sample code from face_recognition github :
https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py

"""
import face_recognition as fr
import cv2
import os
from os import path
import numpy as np


class FaceRecognition:
    def __init__(self):
        self.tello_owner_list, self.tello_owner_names = self.load_model()

    def load_model(self):
        # Load images
        img_dir = 'model/face_recognition/target_img'
        img_ext = ['.jpeg', '.jpg', '.png']
        img_files = [file for file in os.listdir(img_dir) if path.splitext(file)[1] in img_ext]

        # find face in the image with 'HOG'
        load_images = list(map(lambda x: fr.load_image_file(path.join(img_dir, x)), img_files))
        # TODO : sometimes cant find face, needs handling errors. 
        # update argument fr._raw_face_locations(model='cnn')
        tello_owner_list = list(map(lambda x: fr.face_encodings(x)[0], load_images))
        tello_owner_names = list(map(lambda x: path.splitext(x)[0], img_files))

        return tello_owner_list, tello_owner_names

    def recognize(self, frame):
        # Init
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the tello_owner_list
                matches = fr.compare_faces(self.tello_owner_list, face_encoding)
                name = "Unknown"

                # Use the known face with the smallest distance to the new face
                face_distances = fr.face_distance(self.tello_owner_list, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.tello_owner_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Return the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            return top, right, bottom, left, name
