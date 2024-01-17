import numpy as np
import math 
import cv2
from cv2 import aruco as arU
from math import dist
import time
import sys
sys.path.append("..")
from motor import motor_controller as mc

dict = cv2.aruco.DICT_6X6_50
marker_index = 0 
flag = [False, False, False,False]
tolerance = 100 # should be replaced depending on experimental settings
flagtest=0

hstep = 0.1
sec = 10*hstep

FWD_SPEED = .3


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


        self.arucoList = []
        self.arucoToFind = None
        

        #cahier des charges
        self.arucoFlag = [False, False, False,False]

        self.rotationDuration = None 
        self.rotationFix = .5
        self.rotationFlag = True # flag if rotation is needed

        self.direction = 0 
        self.speed = 0

        self.visited_Id = []

    # search mode on 
    def hunting (self, direction, motor):
        """Find a marker by rotating himself according to the direction given"""
        # global flagtest
        # mc.modify_speed(motor,25)
        # mc.turn_right(motor)
        # mc.stop_motor(motor)
        # time.sleep(sleep)
        # flagtest=0
        if not self.arucoToFind: 

            # no markers found yet, specially the one we need
            if not self.rotationDuration : 
                self.rotationDuration = time.time() #init du timer
                # self.speed = .3
        
            if time.time() - self.rotationDuration < self.rotationFix and self.rotationFlag:
                # if a rotation is needed
                print("Turning , direction = ", direction )
                self.direction = direction
                self.speed = .3

            elif self.rotationFlag: #no more rotation
                print("Stop turning " )
                self.rotationDuration = time.time()
                self.rotationFlag = False # stop
            
            if time.time() - self.rotationDuration < self.rotationFix and not self.rotationFlag:
                    print("Not Turning anymore")
                    self.direction= 0
                    self.speed = 0

            elif not self.rotationFlag:
                print("More turning , direction = ", direction )
                self.rotationDuration = time.time()
                self.rotationFlag = True # we keep turning around
        else:
            print("Marquer ID: ", self.arucoToFind["id"])
            self.direction = 0
            self.speed = 0
        
        # mc.updateMotor(motor, self.direction, self.speed)
        
          

    # return the marker id to be found next 
    # it makes sure that the previous marker is found                  
    def get_marker_to_find(self):
        if not self.arucoFlag[0]:
            return 1
        elif self.arucoFlag[0] and not self.arucoFlag[1]:
            return 3
        elif self.arucoFlag[0] and self.arucoFlag[1] and not self.arucoFlag[2]:
            return 5
        else:
            return 9


    def detect_aruco_tag_bis(self, frame, motor):
        (corners, ids, rejected) = self.detector.detectMarkers(frame)
        self.arucoList = [] # initialiser
        
        if len(corners) > 0:
            ids = ids.flatten()

            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                center = (int((topLeft[0] + bottomRight[0]) / 2.0), int((topLeft[1] + bottomRight[1]) / 2.0))
                
                aruco = {
                    "id": markerID,
                    "center": center,
                    "tr": topRight,
                    "tl": topLeft,
                    "br": bottomRight,
                    "bl": bottomLeft,
                    "dist": get_distance(0.5*(math.dist(topLeft, bottomLeft) + math.dist(bottomRight, topRight))) 
                }
                self.arucoList.append(aruco)
            
    def catch_aruco(self):
        list = self.arucoList
        self.rotationDuration = None
        self.arucoToFind =  None
        for aruco in list : 
            if aruco["id"] == self.get_marker_to_find():
                self.arucoToFind = aruco
        
   
    def run(self, frame, motor):
        self.detect_aruco_tag_bis(frame, motor)
        self.catch_aruco()
        if self.arucoToFind :
            print( "A CHERCHER ", self.arucoToFind["id"] )

        if (not self.arucoToFind):
            print("########## HUNTING ############")
            self.hunting(-1, motor) 
        else:
            print("########## GO TO MARKER ########", self.arucoToFind["id"])
            self.go_to_aruco(frame)
        
        mc.updateMotor(motor, self.direction, self.speed)
    
    def go_to_aruco(self, frame):
        height, width = frame.shape[:2]
        frame_center = width//2
        if self.arucoToFind and self.arucoToFind["dist"] > tolerance:
            self.speed = FWD_SPEED

            if self.arucoToFind["center"][0] < frame_center: 
                self.direction = -.2
            else: 
                self.direction = .2

        else:
            self.speed = 0 
            self.direction = 0

        if self.arucoToFind and self.arucoToFind["dist"] < tolerance:
            if self.arucoToFind["id"] not in self.visited_Id :
                print(" add  ")
                self.visited_Id.append(self.arucoToFind["id"])
            # renouveller les flags
            self.arucoFlag[len(self.visited_Id)-1] = True
            if self.arucoFlag[-1] == True:
                print("Finish finding all markers")
            self.arucoToFind = None
        

    # TODO : voiture  ne s'arrête pas, cherchez le pbm: n'entre pas dans le hunting mode après première detection
    

    def detect_aruco_tags(self,frame,motor):
            global flagtest

            # Get frame coordinates
            frame_height, frame_width, _ = frame.shape
            # we only need the center of x coordinate
            frame_center = frame_width / 2 
            if self.flag_is_move == False: 
                (corners, ids, rejected) = self.detector.detectMarkers(frame)
                if ids == None:
                    self.hunting(motor, hstep)
                    return
                
                mc.stop_motor(motor)
                # Si ids != None, un balise est trouve:
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
                        
                        # test if the marker detected is the current marker we are looking for
                        global flag
                        global marker_index
                        print("Marker to find: ", self.get_marker_to_find())
                        print ("Marker detected: ", markerID)
                        if markerID == self.get_marker_to_find() :
                            print("Successfully seen Marquer ID: ", markerID)
                            if flagtest==0:
                                mc.modify_speed(motor,25)
                                mc.turn_left(motor)
                                mc.stop_motor(motor)
                                time.sleep(sec)
                                flagtest=1
                            # After seeing the right marquer, 
                            # continue to get close to this marker

                            # get marker 's center position
                            marker_center = int(topRight[0] + topLeft[0])/2

                            deviation = frame_center - marker_center
                            print("Deviation : ", deviation)
                            
                            # get marker' s height
                            height = abs(topRight[1] - bottomRight[1])

                            # get distance from cam to marker
                            dist_marker = get_distance(height)
                            print("Distance : ", dist_marker)


                            if (dist_marker > 65):
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
                                    time.sleep(sec)
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
                                    time.sleep(sec)
                                self.flag_is_move = False

                            else:
                                # now dist_marker <= 30:
                                # we set the current marker_to_be_found_flag to True
                                # then we increment the marker_index corresponding to the next one to be found

                                flag[marker_index] = True
                                print("Status of finding: ", flag) # show which marquers have been detected
                                marker_index += 1
                                self.flag_is_move = False
                                
                                # at the arrival point
                                if flag[3] : 
                                    print("ARRIVED TO DESTINATION \n")
                                    mc.stop_motor(motor)
                                    time.sleep(20)
                                    mc.set_speed(motor,0)
                                    return
                                                
                                
                        else :
                            print("\t\tDETECTION D'UN AUTRE MARKER\n")

                            # if we do not get the marker we need 
                            self.flag_is_move = False
                            self.hunting(motor, hstep)
                            return
                    
                    

# Pour les détections des balises numérotées, 
# peut-être faire un tableau à trois dimension avec éléments True ou False 
# et ne pas passer au deuxième tant que i-1 n'est pas True 

# faire une fonction qui renvoie le marqueur à chercher 




                

                    








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
                            
                    
                            
                





