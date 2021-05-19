from logging import log
import cv2
import numpy as np
import time
from djitellopy import Tello
import argparse


# Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument('-c','--confidence', type=float, default=0.6, 
    help='use -c to change minimum probability to filter weak detections. default = 0.6' )
args = vars(ap.parse_args())

# Tello init
# me = Tello()
# me.connect()
# print('====>', me.get_battery())

# get frame
# try:
#   me.streamon()
# except:
#   print("====> Could not start video stream")
# frame_read = me.get_frame_read()

cap = cv2.VideoCapture(0)
_, frame = cap.read()
height, width, _ = frame.shape

target_size = 456
frame_center_x = int(width / 2)
frame_center_y = int(height / 2)


# yolo net
net = cv2.dnn.readNet('weights/yolov3_train_last.weights', 'cfgs/yolov3_masks.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
print("🛰🛰🛰 net is working")

classes = []
with open('datas/masks.names','r') as f:
    classes = f.read().splitlines()
print("====> classes :",classes)

# settings
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# drone status
IS_FLYING = False

# mask status
all_with_mask_time = 0

# following status
szX = 100
szY = 55
speed = 20

while True:
    start_time = time.time()
    _, frame = cap.read()
    # frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)

    boxes = []
    confidences = []
    class_ids = []

    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]

            if scores.max() > args['confidence']:
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                x = int((detection[0] - detection[2]/2) * width)
                y = int((detection[1] - detection[3]/2) * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)


    if len(class_ids) == 0:
        print("====> DETECTED NOTHING !!")

    else:
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label + " " + confidence, (x, y+20), font, 2, (255, 255, 255), 2)

        # 대기 상태
        if not IS_FLYING:
            if (1 in class_ids):
                print('🚀🚀🚀 DRONE TAKES OFF !!')
                # me.takeoff()
                IS_FLYING = True

        else:
            # all with_mask일 경우
            if (1 not in class_ids):
                iter_time = time.time() - start_time
                all_with_mask_time += iter_time
                print('all with_mask duration :',round(all_with_mask_time, 3))

                if all_with_mask_time > 10:
                    print('🪂🪂🪂 DRONE LANDS !!')
                    # me.land()
                    all_with_mask_time = 0
                    IS_FLYING = False
                    time.sleep(2)

            # without_mask가 감지되었을 경우
            else:
                all_with_mask_time = 0

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
                            yaw_velocity = speed
                        elif vDistance[0] > szX:
                            yaw_velocity = -speed
                        else:
                            yaw_velocity = 0
                        
                        # for up & down
                        if vDistance[1] > szY:
                            up_down_velocity = speed
                        elif vDistance[1] < -szY:
                            up_down_velocity = -speed
                        else:
                            up_down_velocity = 0

                        F = 0
                        if abs(vDistance[2]) > 250:
                            F = speed

                        # for forward back
                        if vDistance[2] > 0:
                            for_back_velocity = speed + F
                        elif vDistance[2] < 0:
                            for_back_velocity = -speed - F
                        else:
                            for_back_velocity = 0

                        # center circle
                        cv2.circle(frame, (targ_cord_x, targ_cord_y), 10, (0,255,0), 2)


                        print(' DRONE FOLLOW TARGET !!')
                        # me.send_rc_control(0, for_back_velocity, up_down_velocity, yaw_velocity)


    # 화면 출력 스케일 조절
    # scale_percent = 50
    # width = int(width * scale_percent / 100)
    # height = int(height * scale_percent / 100)
    # dim = (width, height)
    # resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # FPS
    iter_time = time.time() - start_time
    fps = 1./iter_time
    cv2.putText(frame, "FPS: {:.2f}".format(fps), (0,30), 0, 1, (0,0,255))
    cv2.imshow('Image', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

frame.release()
cv2.destroyAllWindows()