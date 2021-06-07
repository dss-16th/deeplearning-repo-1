import cv2


def draw_info(image, fps, tello_mode):
    cv2.putText(image, "FPS: " + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2, cv2.LINE_AA)
    """
    k : keyboard control, 
    m : mask detecting & tracking, 
    g : gesture handling
    """
    mode_string = ['KEYBOARD CONTROL', 'MASK DETECTING & TRACKING', 'GESTURE HANDLING']
    dic = {'k':0, 'm':1, 'g':2}

    selected_mode_string = mode_string[dic[tello_mode]]

    cv2.putText(image, "MODE: " + selected_mode_string, (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1,
                cv2.LINE_AA)

    return image