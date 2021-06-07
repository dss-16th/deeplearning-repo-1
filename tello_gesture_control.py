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

        #recording status
        self.keepRecording = True
        self.canRecord = True
        
    def gesture_control(self, gesture_buffer):
        gesture_id = gesture_buffer.get_gesture()

        # Stop
        if gesture_id == 0:
            print('STOP')
            self.forward_backward_vel = self.left_right_vel = \
                self.up_down_vel = self.yaw_vel = 0
            self.send_tello_control()
            return
        # Back
        if gesture_id == 1:
            print('BACK')
            self.forward_backward_vel = -speed
            self.send_tello_control()
            return
        # Forward
        if gesture_id == 2:
            print('FORWARD')
            self.forward_backward_vel = speed
            self.send_tello_control()
            return
        # Land
        if gesture_id == 3:
            print('LAND')
            self.forward_backward_vel = self.left_right_vel = \
                self.up_down_vel = self.yaw_vel = 0
            self.send_tello_control()
            self.tello.land()
            return
        # Photo
        if gesture_id == 4:
            print('PHOTO')
            self.take_tello_photo()
            return
        # Video
        if gesture_id == 5:
            print('RECORD THE VIDEO!')
            self.onoff_tello_video(gesture_id=5)
            return
        if gesture_id == 6:
            self.onoff_tello_video(gesture_id=6)
            print('VIDEO SAVING DONE!')
            return
        # Rock Rock Rock
        if gesture_id == 7:
            print('Rock Rock Rock')
            return

    def send_tello_control(self):
        self.tello.send_rc_control(self.left_right_vel, 
                                   self.forward_backward_vel,
                                   self.up_down_vel, 
                                   self.yaw_vel)
        print('============================== send tello control')

    def take_tello_photo(self):
        photo = self.tello.get_frame_read().frame
        photo_dir = 'Photos'
        if not os.path.isdir(photo_dir):
            os.mkdir(photo_dir)
            print('=======> MAKE A PHOTO DIRECTORY!')

        status = cv2.imwrite(photo_dir + '/tello_photo_{}.jpg'.format(
            str(datetime.datetime.now()).split('.')[0].replace(':','-').replace(' ','_')), photo)
        print('IMAGE SAVING DONE!', status)

    def videoRecorder(self):
        # create a VideoWrite object, recoring to ./video.mp4
        frame_read = self.tello.get_frame_read()
        height, width, _ = frame_read.frame.shape
        
        global video
        # video_file = f"Videos/tello_video_{datetime.datetime.now().strftime('%d-%m-%Y-%I-%M-%S-%p')}.mp4"
        video_file = f"Videos/tello_video_{str(datetime.datetime.now()).split('.')[0].replace(':','-').replace(' ','_')}.mp4"
        video = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

        while self.keepRecording:
            video.write(frame_read.frame)
            time.sleep(1 / 30)

        video.release()

    def onoff_tello_video(self, gesture_id):
        global recorder

        video_dir = 'Videos'
        if not os.path.isdir(video_dir):
            os.mkdir(video_dir)
            print('=======> MAKE A VIDEO DIRECTORY!')

        if gesture_id == 5:
            if self.canRecord:
                self.canRecord = False
                self.keepRecording = True
                recorder = Thread(target=self.videoRecorder)
                recorder.start()

        if gesture_id == 6:
            if not self.canRecord:
                self.keepRecording = False
                recorder.join()
                self.canRecord = True