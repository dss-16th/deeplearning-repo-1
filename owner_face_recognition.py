import face_recognition
import cv2
import numpy as np
from djitellopy import Tello

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

class FaceRecognition:
    def __init__(self):
        self.tello_owner_list, self.tello_owner_names = self.load_model()

    def load_model(self):
        mieyghanj_image = face_recognition.load_image_file("model/face_recognition/target_img/mieyhgnaj.jpg")
        mieyghanj_encoding = face_recognition.face_encodings(mieyghanj_image)[0]

        dockyum_image = face_recognition.load_image_file("model/face_recognition/target_img/dockyum_2015.jpeg")
        dockyum_encoding = face_recognition.face_encodings(dockyum_image)[0]

        # Create owner
        tello_owner_list = [
            mieyghanj_encoding,
            dockyum_encoding
        ]
        tello_owner_names = [
            "mieyhgnaj",
            "dockyum_2015"
        ]

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
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.tello_owner_list, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.tello_owner_list, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.tello_owner_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            return top, right, bottom, left, name
