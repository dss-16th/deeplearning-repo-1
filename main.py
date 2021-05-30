from djitellopy import Tello
import cv2
import numpy as np
import argparse
from tello_keyboard_control import KeyboardControler
from tello_withoutmask_tracking import MaskTracking


# standard argparse stuff
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='** = required')
parser.add_argument('-d', '--distance', type=int, default=3,
                    help='use -d to change the distance of the drone. Range 0-6')
parser.add_argument('-sx', '--saftey_x', type=int, default=100,
                    help='use -sx to change the saftey bound on the x axis . Range 0-480')
parser.add_argument('-sy', '--saftey_y', type=int, default=55,
                    help='use -sy to change the saftey bound on the y axis . Range 0-360')
parser.add_argument('-os', '--override_speed', type=int, default=1,
                    help='use -os to change override speed. Range 0-3')
parser.add_argument('-ss', "--save_session", action='store_true',
                    help='add the -ss flag to save your session as an image sequence in the Sessions folder')
parser.add_argument('-D', "--debug", action='store_true',
                    help='add the -D flag to enable debug mode. No need drone. Only print commands')
parser.add_argument('-m', '--mode', type=str, default='m',
                    help='set start mode. k : keyboard control, m : mask detecting & tracking, g : gesture handing')                    
args = parser.parse_args()


# Speed of the drone
S = 20
# S2 = 5
UDOffset = 150

# this is just the bound box sizes that openCV spits out *shrug*
faceSizes = [1026, 684, 456, 304, 202, 136, 90]

# These are the values in which kicks in speed up mode, as of now, this hasn't been finalized or fine tuned so be careful
# Tested are 3, 4, 5
acc = [500, 250, 250, 150, 110, 70, 50]

# Frames per second of the pygame window display
FPS = 25
dimensions = (960, 720)


# # If we are to save our sessions, we need to make sure the proper directories exist
# if args.save_session:
#     ddir = "Sessions"
#
#     if not os.path.isdir(ddir):
#         os.mkdir(ddir)
#
#     ddir = "Sessions/Session {}".format(str(datetime.datetime.now()).replace(':','-').replace('.','_'))
#     os.mkdir(ddir)


class FrontEnd(object):

    def __init__(self):
        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()
        self.tello_mode = args.mode

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        # drone status 
        self.send_rc_control = False
        self.IS_FLYING = False

        # mask status
        self.all_with_mask_time = 0


    def select_mode(self, key):
        """
        k : keyboard control, 
        m : mask detecting & tracking, 
        g : gesture handing
        """
        if key == ord('k'):
            self.tello_mode = 'k'
        if key == ord('m'):
            self.tello_mode = 'm'
        if key == ord('g'):
            self.tello_mode = 'g'


    def run(self):
        try:
            self.tello.connect()
        except:
            print("================= Tello not connected =================")
            return
            
        try:
            self.tello.streamon()
        except:
            print("================= Could not start video stream =================")
            return

        width, height = 1050, 700

        # init controllers
        keyboardController = KeyboardControler(self.tello)
        maskDetector = MaskTracking(width, height, self.tello.takeoff, self.tello.send_rc_control, 0.6)

        # frame read
        frame_read = self.tello.get_frame_read()

        OVERRIDE = False # 이게 True면 키보드 조종이 가능한 상태
        oSpeed = args.override_speed
        tDistance = args.distance
        self.tello.get_battery()

        # Safety Zone X, Y
        szX, szY = args.saftey_x, args.saftey_y

        if args.debug:
            print("================= DEBUG MODE ENABLED! =================")

       
        while True:
            self.update()

            if frame_read.stopped:
                frame_read.stop()
                break

            frame = cv2.resize(frame_read.frame, (width, height))

            # Listen for key presses
            k = cv2.waitKey(10)

            # Quit the software
            if k == 27:
                break

            # 'Spacebar' to enter select mode 
            if k == 32:
                self.select_mode()

            ## ==> KEYBOARD CONTROL MODE !!
            if self.tello_mode == 'k':
                keyboardController.control(k)
                # 'delete' to override: 
                if k == 127:
                    OVERRIDE = keyboardController.update_override()

                # Press 0~6 to set distance
                if k in list(map(lambda num : ord(str(num)), range(0,7))):
                    if OVERRIDE:
                        oSpeed = keyboardController.set_speed(k)
                    else:
                        tDistance = keyboardController.set_distance(k)

            ## ==> MASK DETECTING MODE !!
            if self.tello_mode == 'm':
                maskDetector.detect_mask(frame, szX, szY)


            dCol = lerp(np.array((0, 0, 255)), np.array((255, 255, 255)), tDistance + 1 / 7)

            if OVERRIDE:
                show = "OVERRIDE: {}".format(oSpeed) # default = 1
                dCol = (255, 255, 255)
            else:
                show = "AI: {}".format(str(tDistance)) # default = 3

            # Draw the distance choosen
            cv2.putText(frame, show, (32, 664), cv2.FONT_HERSHEY_SIMPLEX, 1, dCol, 2)

            # Display the resulting frame
            cv2.imshow(f'Tello Tracking 🧟 ....', frame)

        # On exit, print the battery
        self.tello.get_battery()

        # When everything done, release the capture
        cv2.destroyAllWindows()

        # Call it always before finishing. I deallocate resources.
        self.tello.end()

    def battery(self):
        return self.tello.get_battery()[:2]

    def update(self):
        """Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)


def lerp(a, b, c):
    return a + c * (b - a)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()