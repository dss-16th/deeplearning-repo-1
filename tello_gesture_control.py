from djitellopy import Tello
import os
import cv2
import datetime


speed = 20
class TelloGestureController:
    def __init__(self, tello: Tello):
        self.tello = tello
        self._is_landing = False

        # RC control velocities
        self.forward_backward_vel = 0
        self.left_right_vel = 0
        self.up_down_vel = 0
        self.yaw_vel = 0
        
    def gesture_control(self, gesture_buffer):
        gesture_id = gesture_buffer.get_gesture()
        print("GESTURE : ", gesture_id)

        if not self._is_landing:
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
                self.onoff_tello_video()
                return
            if gesture_id == 6:
                self.onoff_tello_video()
                return

    def send_tello_control(self):
        self.tello.send_rc_control(self.left_right_velocity, 
                                   self.forw_back_velocity,
                                   self.up_down_velocity, 
                                   self.yaw_velocity)

    def take_tello_photo(self):
        photo = self.tello.get_frame_read().frame
        photo_dir = 'Photos'
        if not os.path.isdir(photo_dir):
            os.mkdir(photo_dir)
            print ('=======> MAKE A DIRECTORY!')

        status = cv2.imwrite(photo_dir + '/tello_photo_{}.jpg'.format(
            str(datetime.datetime.now()).split('.')[0].replace(':','-').replace(' ','-')), photo)
        print('IMAGE SAVEING DONE!', status)

    def onoff_tello_video(self):
        print('TODO : ONOFF TELLO VIDEO!!!')
