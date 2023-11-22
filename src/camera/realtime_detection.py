import argparse
import time
import cv2
from cv2 import aruco as arU
import sys

from .. import motor_controller as mc

dict = cv2.aruco.DICT_6X6_50


def get_distance(height):
    if height <= 0 : 
        return 0 
    elif 0 < height and height <= 300 :
        return 13793/(height**1.07)
    else :
        return -0.0814*height + 53.412
 
class Detector():
    def __init__(self, dico = dict):
        self.dict = arU.getPredefinedDictionary(dico)
        self.params = arU.DetectorParameters()
        self.detector = arU.ArucoDetector(self.dict, self.params)
    

    def detect_aruco_tags(self,frame,motor):

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
                if dist_marker > 20 : 
                    print("Avancer")
                    mc.move_forward(motor)
                    # mc.modify_speed(motor, 25)
                elif 0 < dist_marker and dist_marker <= 20 : 
                    if markerID % 2 == 1:  # marqueur impair
                        print("Marqueur Impair: Demi-tour & tourner à gauche * 2")
                        mc.modify_speed(motor, 40) # modifier la vitesse 
                        mc.turn_left(motor)
                        mc.turn_left(motor)
                    else:
                        print("Marqueur Pair: Arrêter") 
                        mc.stop_motor(motor)
                else:
                    print("Trop proche")

                




