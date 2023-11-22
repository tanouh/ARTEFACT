import argparse
import time
import cv2
from cv2 import aruco as arU
import sys

dict = cv2.aruco.DICT_6X6_50

def get_distance(height):
    if height <= 0 : 
        return 0 
    elif height <= 300 :
        return 13793/height
    else :
        return -0.0814*height + 53.412
 
def detect_aruco_tags(video_source=0):
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
                print(dist_marker)
                if (dist_marker > 20) : 
                    print("Avancer")
                else : 
                    print("Stop") 
 

        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break

    cv2.destroyAllWindows()
    vc.release()

# if __name__ == "__main__":
#     # construct the argument parser and parse the arguments
#     ap = argparse.ArgumentParser()
#     ap.add_argument("-t", "--type", type=str, default="DICT_6X6_50", help="type of ArUCo tag to detect")
#     args = vars(ap.parse_args())

#     # Call the function with the supplied arguments
#     detect_aruco_tags(0)
