import argparse
import time
import cv2
from cv2 import aruco as arU
import sys
from motor_controller import start_motor, stop_motor, set_step_duration, move_forward, move_backward, turn_left, turn_right, modify_speed

dict = cv2.aruco.DICT_6X6_50

def get_distance(height):
    if height <= 0 : 
        return 0 
    elif height <= 300 :
        return 13793/height
    else :
        return -0.0814*height + 53.412

def detect_aruco_tags(aruco_dict_type="DICT_6X6_50", video_source=0):
    # 和之前的 ArUco 检测逻辑一样
    # ...
    print("[INFO] starting video stream...")
    vc = cv2.VideoCapture(video_source)
    time.sleep(2.0)

    arucoDict = arU.getPredefinedDictionary(dict)
    arucoParams = arU.DetectorParameters()
    detector = arU.ArucoDetector(arucoDict, arucoParams)


    while True:
        ret, frame = vc.read()
        if not ret:
            break

        (corners, ids, rejected) = detector.detectMarkers(frame)
        if ids == None:
            continue
        if len(corners) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                    

                height = abs(topRight[1] - bottomRight[1])

                dist_marker = get_distance(height)
                if (dist_marker > 20) : 
                    print("Avancer")
                    move_forward(motor)
                else : # quand la distance <= 20, faire la demi-tour
                    print("Stop and turn left") 
                    if markerID % 2 == 1:  # marqueur impair
                        print("Turn left * 2")
                        modify_speed(motor, 40) # modifier la vitesse 
                        turn_left(motor)
                        turn_left(motor)
                    else:  # marqueur pair
                        print("Stop")
 

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vc.release()



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    motor = start_motor()  # 初始化电机控制

    try:
        detect_aruco_tags(0)

        # 在这里添加根据 ArUco 检测结果的逻辑
        # 例如，如果检测到 ArUco 编号为 33，则调用 turn_right 函数
        # aruco_detected = True  # 你需要替换这个值为实际的 ArUco 检测逻辑
        # if aruco_detected:
        #     turn_right(motor)

        # 以下是一个简单的例子，每隔一秒钟小车向前移动一次
        while True:
            move_forward(motor)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        stop_motor(motor)  
