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
 
class Detector():
    def __init__(self, dico = dict):
        self.dict = arU.getPredefinedDictionary(dico)
        self.params = arU.DetectorParameters()
        self.detector = arU.ArucoDetector(self.dict, self.params)
    
    def detect_aruco_tags(self,frame):
        (corners, ids, rejected) = self.detector.detectMarkers(frame)
        if ids == None:
            return
        if len(corners) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                
                # get marker' s height

                height = abs(topRight[1] - bottomRight[1])

                # get distance from cam to marker
                dist_marker = get_distance(height)

                # execute appropriate move
                if (dist_marker > 20) : 
                    print("Avancer")
                else : 
                    print("Stop") 



# if __name__ == "__main__":
#     # construct the argument parser and parse the arguments
#     ap = argparse.ArgumentParser()
#     ap.add_argument("-t", "--type", type=str, default="DICT_6X6_50", help="type of ArUCo tag to detect")
#     args = vars(ap.parse_args())

    # Call the function with the supplied arguments
    detect_aruco_tags(0)
