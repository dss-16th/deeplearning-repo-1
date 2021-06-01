from djitellopy import Tello
import os
import time, cv2
from threading import Thread
import datetime
from owner_face_recognition import FaceRecognition


speed = 20
class TelloGestureController:
    def __init__(self, tello: Tello):
        self.tello = tello

        # RC control velocities
        self.forward_backward_vel = 0
        self.left_right_vel = 0
        self.up_down_vel = 0
        self.yaw_vel = 0
        
    def gesture_control(self, gesture_buffer):
        gesture_id = gesture_buffer.get_gesture()
        if gesture_id != None :
            print("GESTURE : ", gesture_id, type(gesture_id))

        # Stop
        if gesture_id == 0:
            self.forward_backward_vel = self.left_right_vel = \
                self.up_down_vel = self.yaw_vel = 0
            self.send_tello_control()
            return
        # Back
        if gesture_id == 1:
            self.forward_backward_vel = -speed
            self.send_tello_control()
            return
        # Forward
        if gesture_id == 2:
            self.forward_backward_vel = speed
            self.send_tello_control()
            return
        # Land
        if gesture_id == 3: 
            self.forward_backward_vel = self.left_right_vel = \
                self.up_down_vel = self.yaw_vel = 0
            self.send_tello_control()
            self.tello.land()
            return
        # Photo
        if gesture_id == 4:
            self.take_tello_photo()
            return
        # Video
        if gesture_id == 5:
            keepRecording = True
            self.onoff_tello_video(gesture_id=5, keepRecording=keepRecording)
            return
        if gesture_id == 6:
            recorder.join()
            keepRecording = False
            print('VIDEO SAVEING DONE!')
            # self.onoff_tello_video()
            # keepRecording = False
            # recorder = Thread(target=self.onoff_tello_video)
            # recorder.join()
            # return
        # Rock paper scissors
        if gesture_id == 7:
            print('================== 👊🏻👊🏼👊🏽👊🏾👊🏿')
            return


    def send_tello_control(self):
        self.tello.send_rc_control(self.left_right_vel, 
                                   self.forward_backward_vel,
                                   self.up_down_vel, 
                                   self.yaw_vel)
        print('==============================send tello control')


    def take_tello_photo(self):
        photo = self.tello.get_frame_read().frame
        photo_dir = 'Photos'
        if not os.path.isdir(photo_dir):
            os.mkdir(photo_dir)
            print('=======> MAKE A PHOTO DIRECTORY!')

        status = cv2.imwrite(photo_dir + '/tello_photo_{}.jpg'.format(
            str(datetime.datetime.now()).split('.')[0].replace(':','-').replace(' ','-')), photo)
        print('IMAGE SAVEING DONE!', status)

    def onoff_tello_video(self, gesture_id, keepRecording):
        if (gesture_id == 5) & (keepRecording == True):
            global video
            frame_read = self.tello.get_frame_read()
            video = frame_read.frame
            video_dir = 'Videos'
            if not os.path.isdir(video_dir):
                os.mkdir(video_dir)
                print('=======> MAKE A VIDEO DIRECTORY!')

                height, width, _ = frame_read.frame.shape
                video_file = video_dir + f"/tello_video_{datetime.datetime.now().strftime('%d-%m-%Y_%I-%M-%S_%p')}.mp4"
                video = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'MP4V'), 30, (width, height))

                while keepRecording:
                    video.write(frame_read.frame)
                    time.sleep(1 / 30)

                video.release()
            
            global recorder
            recorder = Thread(target=self.onoff_tello_video(gesture_id=5, keepRecording=keepRecording))
            recorder.start()

        # elif (gesture_id == 6) & (keepRecording == True):
        #     keepRecording = False
        #     recorder.join()
        #     print('VIDEO SAVEING DONE!')
            
            # while True:
            #     if gesture_id == 6:
            #         keepRecording = False
            #         recorder.join()
            #         print('VIDEO SAVEING DONE!')
