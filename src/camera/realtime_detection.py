import cv2
from cv2 import aruco as arU
import time
import sys
sys.path.append("..")
from motor import motor_controller as mc

dict = cv2.aruco.DICT_6X6_50
flag = False
tolerance = 100 # should be replaced depending on experimental settings


step = 0.2
hstep = 0.1
vhstep = 0.05
sec = 10*hstep



def get_distance(height):
    if height <= 0 : 
        return 0 
    elif 0 < height and height <= 400 :
        return 16587*height**(-1.11)
    else :
        return -0.047*height + 39.099

 
class Detector():
    def __init__(self, dico = dict):
        self.dict = arU.getPredefinedDictionary(dico)
        self.params = arU.DetectorParameters()
        self.detector = arU.ArucoDetector(self.dict, self.params)
        self.flag_is_move = False
    
    # search mode on 
    def hunting (self, motor, sleep):
        mc.modify_speed(motor,35)
        mc.turn_right(motor)
        mc.stop_motor(motor)
        time.sleep(sleep)

    def detect_aruco_tags(self,frame,motor):
        # Get frame coordinates
        frame_height, frame_width, _ = frame.shape
        #we only need the center of x coordinate
        frame_center = frame_width / 2 

        if self.flag_is_move == False:
            (corners, ids, rejected) = self.detector.detectMarkers(frame)
            if ids == None:
                self.hunting(motor, sec)
                return
            mc.stop_motor(motor)
            self.flag_is_move = True
            if len(corners) > 0:
                ids = ids.flatten()


                print("###### BALISE DETECTE #########")
                for (markerCorner, markerID) in zip(corners, ids):
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft=(int(bottomLeft[0]), int(bottomLeft[1]))
                    
                    # get marker 's center position
                    marker_center = int(topRight[0] + topLeft[0])/2

                    deviation = frame_center - marker_center
                    print("Deviation : ", deviation)
                    
                    # get marker' s height
                    height = abs(topRight[1] - bottomRight[1])

                    # get distance from cam to marker
                    dist_marker = get_distance(height)
                    print("DDDDDDDDistance : ", dist_marker)
                    if (dist_marker > 30):
                        if (deviation < 0):
                            if(dist_marker > 100 ):
                                mc.right(deviation, motor)
                                print("\tAVANCER DROITE VITE \n")
                            else:
                                mc.right_slow(deviation, motor)    
                                print("\tAVANCER DROITE LENTEMENT \n")                      
                            # move to the right
                            # speed_right ++
                            # speed_left --
                            mc.move_forward(motor)
                        else:
                            if(dist_marker > 100 ):
                                mc.left(deviation, motor)
                                print("\tAVANCER GAUCHE VITE \n")
                            else:
                                mc.left_slow(deviation, motor)  
                                print("\tAVANCER GAUCHE LENTEMENT \n")                          
                                # move to the right
                                # inverse 
                                mc.move_forward(motor)
                    else:
                        self.flag_is_move = False
                        self.hunting(motor, hstep)
                        return
                    
                    # global flag
                    
                    # if markerID % 2 == 1 and not flag: # Si trouver Impair marqueur et flag = false
                    #     print(dist_marker)
                    #     # execute appropriate move
                    #     if dist_marker > 50: 
                    #         print("Avancer")

                    #         mc.modify_speed(motor, 30) # ??
                    #         mc.turn_left(motor)  # tourner a gauche avant d'avancer pour modifier la direction
                    #         # time.sleep(hstep)
                    #         mc.stop_motor(motor)


                    #         if dist_marker > 150 :
                    #             mc.modify_speed(motor, 60) # Si tres loin marcher plus vite
                    #             mc.move_forward(motor) # Avancer
                    #             time.sleep(sec)
                    #         else :
                    #             mc.modify_speed(motor, 30) # ??
                    #             mc.move_forward(motor) # Avancer
                    #             time.sleep(2*step)
                            
                    #         mc.stop_motor(motor)

                    #         mc.modify_speed(motor, 20)
                    #         mc.turn_left(motor) # Tourner a gauche trop
                    #         # time.sleep(hstep)

                    #         mc.stop_motor(motor)
                    #         time.sleep(hstep)
                    #         # mc.reach_target(motor, dist_marker)
                            
                    #     else : 
                    #         flag = True
                    #         print("Marqueur Impair: Demi-tour & tourner à gauche * 2")
                    #         mc.stop_motor(motor)

                    #         mc.modify_speed(motor, 70) # modifier la vitesse 
                    #         mc.turn_left(motor)
                    #         time.sleep(sec)

                    #         mc.stop_motor(motor)
                    #         mc.move_forward(motor)
                    #         time.sleep(step)
                    #         mc.stop_motor(motor)
                            
                    #         # mc.turn_around(motor, mc.turn_left)
                    #         self.flag_is_move = False

                    # elif markerID % 2 == 0 and flag: # Si trouver Pair marqueur et flag = true
                    #     # execute appropriate move
                    #     if dist_marker > 50 : 
                    #         print("Avancer")

                    #         mc.modify_speed(motor, 30) # ??
                    #         mc.turn_left(motor)  # tourner a gauche avant d'avancer pour modifier la direction
                    #         # time.sleep(hstep)
                    #         mc.stop_motor(motor)


                    #         if dist_marker > 150 :
                    #             mc.modify_speed(motor, 60) # Si tres loin marcher plus vite
                    #             mc.move_forward(motor) # Avancer
                    #             time.sleep(sec)
                    #         else :
                    #             mc.modify_speed(motor, 30) # ??
                    #             mc.move_forward(motor) # Avancer
                    #             time.sleep(2*step)
                            
                    #         mc.stop_motor(motor)

                    #         mc.modify_speed(motor, 20)
                    #         mc.turn_left(motor) # Tourner a gauche trop
                    #         # time.sleep(hstep)

                    #         mc.stop_motor(motor)
                    #         time.sleep(hstep)
                    #         # mc.reach_target(motor, dist_marker)
                    #         self.flag_is_move = False
                    #     else : 
                    #         print("Marqueur Pair: Arrêter")
                    #         mc.stop_motor(motor)
                    #         time.sleep(20)
                    #         self.flag_is_move = False
                    # else:
                    #     self.flag_is_move = False
                    #     self.hunting(motor, hstep)
                    #     return
                            
                    
                            
                





