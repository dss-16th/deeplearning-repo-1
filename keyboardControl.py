"""
OVERRIDE == True : 
    직접 조정 모드
OVERRIDE == False : 
    세팅 변경 모드

"""
from djitellopy import Tello


class KeyboardControler:
    def __init__(self, tello:Tello):
        self.tello = tello
        self.OVERRIDE = False

        self.for_back_velocity = 0
        self.yaw_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0

        self.speed_point = 1

    def update_override(self):
        """
        Press Delete for controls OVERRIDE
        """
        if not self.OVERRIDE:
            self.OVERRIDE = True
            print("================= OVERRIDE ENABLED 🕹 =================")
        else:
            self.OVERRIDE = False
            print("================= OVERRIDE DISABLED 🆖 =================")
        
        return self.OVERRIDE

    def set_distance(self, key):
        """
        OVERRIDE == False

        set distance between tello and target
        """
        if self.OVERRIDE:
            print("Disable distance setting : OVERRIDE == False")
        else:
            target_distance = int(chr(key))
            if target_distance not in range(1,7):
                print("not available distance : set to default")
                target_distance = 3
            print("================= DISTANCE = {} =================".format(target_distance))

        return target_distance

    def set_speed(self, key):
        """
        OVERRIDE == True
        
        set tello speed
        """
        if not self.OVERRIDE:
            print("Disable override")
        else:
            self.speed_point = int(chr(key))
            if self.speed_point not in range(1,4):
                print("not available speed : set to default")
                self.speed_point = 1
            print("================= SPEED = {} =================".format(self.speed_point))

        return self.speed_point

    def control(self, key, *args):
        # speed unit
        S = 20

        if key == ord('t'):
            print("================= Taking Off 🛫 =================")
            if not args.debug:
                self.tello.takeoff()
                self.tello.get_battery()

        if key == ord('l'):
            print("================= Landing 🛬 =================")
            if not args.debug:
                self.tello.land()  

        if not self.OVERRIDE:
            print("Disable control : Override == False")
        else:
            # S & W to fly forward & back
            if key == ord('w'):
                self.for_back_velocity = int(S * self.speed_point)
            elif key == ord('s'):
                self.for_back_velocity = -int(S * self.speed_point)
            else:
                self.for_back_velocity = 0

            # a & d to pan left & right
            if key == ord('d'):
                self.yaw_velocity = int(S * self.speed_point)
            elif key == ord('a'):
                self.yaw_velocity = -int(S * self.speed_point)
            else:
                self.yaw_velocity = 0

            # Q & E to fly up & down
            if key == ord('e'):
                self.up_down_velocity = int(S * self.speed_point)
            elif key == ord('q'):
                self.up_down_velocity = -int(S * self.speed_point)
            else:
                self.up_down_velocity = 0

            # c & z to fly left & right
            if key == ord('c'):
                self.left_right_velocity = int(S * self.speed_point)
            elif key == ord('z'):
                self.left_right_velocity = -int(S * self.speed_point)
            else:
                self.left_right_velocity = 0

        self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity, self.yaw_velocity)
        