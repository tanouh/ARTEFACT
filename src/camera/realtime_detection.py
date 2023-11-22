import cv2
from cv2 import aruco as arU
import time
import sys
sys.path.append("..")
from motor import motor_controller as mc

dict = cv2.aruco.DICT_6X6_50
flag = False

step = 0.2
hstep = 0.1

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
            mc.modify_speed(motor,35)
            mc.turn_right(motor)
            mc.stop_motor(motor)
            time.sleep(10*hstep)
            return
        
        mc.stop_motor(motor)
        if len(corners) > 0:
            ids = ids.flatten()

            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft=(int(bottomLeft[0]), int(bottomLeft[1]))
                
                # get marker' s height
                height = abs(topRight[1] - bottomRight[1])
                middle= abs(topRight[0]-bottomLeft[0])

                # get distance from cam to marker
                dist_marker = get_distance(height)
                global flag

                if markerID % 2 == 1 and not flag: # Impair marqueur et flag = false


                    # execute appropriate move
                    if dist_marker > 30 : 
                        print("Avancer")
                        mc.modify_speed(motor, 40)
                        mc.move_forward(motor)
                        time.sleep(step)
                        mc.stop_motor(motor)

                        mc.modify_speed(motor, 30)
                        mc.turn_left(motor)
                        time.sleep(hstep)

                        mc.stop_motor(motor)
                        
                    else : 
                        flag = True
                        print("Marqueur Impair: Demi-tour & tourner à gauche * 2")
                        mc.stop_motor(motor)

                        mc.modify_speed(motor, 60) # modifier la vitesse 
                        mc.turn_left(motor)
                        time.sleep(step)
                        
                        mc.stop_motor(motor)

                elif markerID % 2 == 0 and flag: # Pair marqueur et flag = true
                    # execute appropriate move
                    if dist_marker > 20 : 
                        print("Avancer")
                        mc.modify_speed(motor, 40)
                        mc.move_forward(motor)
                        time.sleep(hstep)

                        mc.stop_motor(motor)
                    else : 
                        print("Marqueur Pair: Arrêter")
                        mc.stop_motor(motor)
                else:
                    mc.modify_speed(motor,35)
                    mc.turn_right(motor)
                    time.sleep(hstep)
                    mc.stop_motor(motor)
                    return
                        
                
                        
            





