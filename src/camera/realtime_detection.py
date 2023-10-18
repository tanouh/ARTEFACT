import argparse
import time
import cv2
from cv2 import aruco as arU
import sys
from dictlib import ARUCO_DICT

def detect_aruco_tags(aruco_dict_type="DICT_ARUCO_ORIGINAL", video_source=0):
    if ARUCO_DICT.get(aruco_dict_type, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(aruco_dict_type))
        sys.exit(0)

    print("[INFO] detecting '{}' tags...".format(aruco_dict_type))

    arucoDict = arU.getPredefinedDictionary(ARUCO_DICT[aruco_dict_type])
    arucoParams = arU.DetectorParameters()
    detector = arU.ArucoDetector(arucoDict, arucoParams)

    print("[INFO] starting video stream...")
    vc = cv2.VideoCapture(video_source)
    time.sleep(2.0)

    while True:
        ret, frame = vc.read()
        if not ret:
            break

        (corners, ids, rejected) = detector.detectMarkers(frame)
        if len(corners) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                # TO DO : (FILL ME) Get distance approximation 
                # Etape 1 : Calibrer la caméra cf doc


                # Etape 2: 
                # pixel_width = abs(topRight - topLeft)
                # distance  = (markerSize * longueurfocale)/pixel_width
                

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vc.release()

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    # Call the function with the supplied arguments
    detect_aruco_tags(args["type"])
