# from djitellopy import Tello 
import cv2
import numpy as np
import time


dimensions = (960, 720)

target_size = 456
frame_center_x = int(dimensions[0] / 2)
frame_center_y = int(dimensions[1] / 2)

speed = 20

class MaskTracking:
    def __init__(self, frame_width, frame_height, takeoff, send_rc_control, confidence=0.5):
        self.takeoff = takeoff
        self.send_rc_control = send_rc_control
        self.confidence = confidence

        self.width = frame_width
        self.height = frame_height
        
        self.all_with_mask_time = 0
        self.is_flying = False

        self.forward_backward_vel = 0
        self.yaw_vel = 0
        self.up_down_vel = 0
        self.left_right_vel = 0
        

        # yolov3 net
        self.net = cv2.dnn.readNet('model/object_detection/yolov3_train_last.weights', 'model/object_detection/yolov3_masks.cfg')
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        print("🛰🛰🛰 net is working")

        self.classes = []
        with open('model/object_detection/masks.names','r') as f:
            self.classes = f.read().splitlines()
        print("====> classes :",self.classes)

        # settings
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def is_with_mask(class_ids):
        return 1 not in class_ids

    def is_without_mask(class_ids):
        return 1 in class_ids

    def detect_mask(self, frame, szX, szY):
        start_time = time.time()

        boxes = []
        confidences = []
        class_ids = []

        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320), (0,0,0), swapRB=True, crop=False)
        self.net.setInput(blob)

        output_layers_names = self.net.getUnconnectedOutLayersNames()
        layerOutputs = self.net.forward(output_layers_names)

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]

                if scores.max() > self.confidence:
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    x = int((detection[0] - detection[2]/2) * self.width)
                    y = int((detection[1] - detection[3]/2) * self.height)
                    w = int(detection[2] * self.width)
                    h = int(detection[3] * self.height)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)


        if len(class_ids) == 0:
            print("====> DETECTED NOTHING !!")

        else:
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                confidence = str(round(confidences[i], 2))
                color = self.colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label + " " + confidence, (x, y+20), self.font, 2, (255, 255, 255), 2)


            # 대기 상태
            if not self.is_flying:
                if self.is_without_mask():
                    print('🚀🚀🚀 DRONE TAKES OFF !!')
                    self.takeoff()
                    self.is_flying = True

            else:
                if self.is_with_mask():
                    iter_time = time.time() - start_time
                    self.all_with_mask_time += iter_time
                    print('all with_mask duration :',round(self.all_with_mask_time, 3))
                    # self.tello.send_rc_control(0,0,0,0)

                    if self.all_with_mask_time > 10:
                        print('🪂🪂🪂 DRONE LANDS !!')
                        # me.land()
                        self.all_with_mask_time = 0
                        self.is_flying = False
                        time.sleep(2)

                # without_mask가 감지되었을 경우
                else:
                    self.all_with_mask_time = 0

                    for i in indexes.flatten() : 
                        if class_ids[i] == 1 :
                            x, y, w, h = boxes[i]

                            targ_cord_x = int(((x+w) + x)/2)
                            targ_cord_y = int(((y+h) + y)/2)

                            vTrue = np.array((frame_center_x,frame_center_y,target_size))
                            vTarget = np.array((targ_cord_x, targ_cord_y, w*2))
                            vDistance = vTrue-vTarget

                            # for turning
                            if vDistance[0] < -szX:
                                self.yaw_vel = speed
                            elif vDistance[0] > szX:
                                self.yaw_vel = -speed
                            else:
                                self.yaw_vel = 0
                            
                            # for up & down
                            if vDistance[1] > szY:
                                self.up_down_vel = speed
                            elif vDistance[1] < -szY:
                                self.up_down_vel = -speed
                            else:
                                self.up_down_vel = 0

                            F = 0
                            if abs(vDistance[2]) > 250:
                                F = speed

                            # for forward back
                            if vDistance[2] > 0:
                                self.forward_backward_vel = speed + F
                            elif vDistance[2] < 0:
                                self.forward_backward_vel = -speed - F
                            else:
                                self.forward_backward_vel = 0

                            # center circle
                            cv2.circle(frame, (targ_cord_x, targ_cord_y), 10, (0,255,0), 2)

                            # safety zone
                            cv2.rectangle(frame, (targ_cord_x - szX, targ_cord_y- szY), (targ_cord_x + szX, targ_cord_y + szY), (0, 255, 0), 2)

                            cv2.putText(frame, str(vDistance), (0, 64), self.font, 1, (255, 255, 255), 2)

                            self.send_rc_control(self.left_right_vel, self.forward_backward_vel, self.up_down_vel, self.yaw_vel)
                            return
