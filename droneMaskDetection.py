"""
1. 드론이 카메라만 켜진 상태에서 마스크를 착용한 사람이 detecting 되면 떠오른다.(고 추정하는 코드)

"""
import cv2
import numpy as np
import time
from djitellopy import Tello


me = Tello()
me.connect()
print(me.get_battery())


try :
    me.streamon()
except :
    print("Could not start video stream")
# if not me.streamon():
#     print("Could not start video stream")

frame_read = me.get_frame_read().frame

net = cv2.dnn.readNet('weights/yolov3_train_last.weights', 'cfgs/yolov3_masks.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

classes = []
with open('datas/masks.names','r') as f:
    classes = f.read().splitlines()
print(classes)

font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(len(classes), 3))
height = 360
width = 240

# drone status
IS_FLYING = False

# mask status
ALL_WITH_MASK = True
hover_time = 0

while True:
    start_time = time.time()
    img = cv2.resize(frame_read, (360, 240))
    # height, width, _ = img.shape

    boxes = []
    confidences = []
    class_ids = []

    # 4. 이미지를 blob(Binary Large Object) 으로 변환하고 사이즈도 줄여서 네트워크에 넣기
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (320, 320), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)


    # 5. output layer에서 결과 받기
    # ln = net.getLayerNames()
    # output_layers_names = [ln[i[0] - 1]for i in net.getUnconnectedOutLayers()]
    output_layers_names = net.getUnconnectedOutLayersNames()
    # output_layers_names = net.getLayerNames()
    layerOutputs = net.forward(output_layers_names)

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    if len(boxes) > 0:
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255, 255, 255), 2)

    loop_time = time.time() - start_time
    # find mask man
    if 1 in class_ids:
        print("==============find without mask person==========")
        ALL_WITH_MASK == False
        mask_safe_time = 0
        if not IS_FLYING :
            print('============drone takes off============')
            # me.takeoff()
            IS_FLYING = True

    # 10초 지나면 다시 착륙
    if (ALL_WITH_MASK == True) & (IS_FLYING == True):
        mask_safe_time += loop_time
        print(mask_safe_time)
        if mask_safe_time > 10:
            print('============drone land =============')
            mask_safe_time = 0
            IS_FLYING = False
            time.sleep(2)


    # 화면 출력 스케일 조절
    # scale_percent = 50
    # width = int(width * scale_percent / 100)
    # height = int(height * scale_percent / 100)
    # dim = (width, height)
    # resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # FPS
    iter_time = time.time() - start_time
    fps = 1./iter_time
    cv2.putText(img, "FPS: {:.2f}".format(fps), (0,30), 0, 1, (0,0,255))
    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key == 27:
        break

img.release()
cv2.destroyAllWindows()