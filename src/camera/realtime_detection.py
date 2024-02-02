import numpy as np
import math 
import cv2
from cv2 import aruco as arU
from math import dist
import time
import sys
sys.path.append("..")
from motor import motor_controller as mc, mylib 

dict = cv2.aruco.DICT_6X6_50
tolerance = 57 # should be replaced depending on experimental settings
FWD_SPEED = .4

def get_distance(height):
    '''Calculates the distance estimations based on the height of the markers'''
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
        self.rotationFix = 10
        self.rotationFlag = True # flag if rotation is needed

        self.direction = 0 
        self.moveDuration = 0
        self.speed = 0
        self.stop_flag = False

        self.visited_Id = []

    # search mode on 
    def hunting (self, direction):
        """Find a marker by rotating himself according to the direction given"""
        if not self.arucoToFind: 

            # no markers found yet, specially the one we need
            if not self.rotationDuration : 
                self.rotationDuration = time.time() #init du timer
                # self.speed = .3
        
            if time.time() - self.rotationDuration < self.rotationFix and self.rotationFlag:
                # if a rotation is needed
                print("Turning , direction = ", direction )
                self.direction = direction
                self.speed = .25

            elif self.rotationFlag: # no more rotation
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
               

    # return the marker id to be found next 
    # it makes sure that the previous marker is found                  
    def get_marker_to_find(self):
        '''It corresponds to the specification : may be changed in future versions'''
        if not self.arucoFlag[0]:
            return 2
        elif self.arucoFlag[0] and not self.arucoFlag[1]:
            return 4
        elif self.arucoFlag[0] and self.arucoFlag[1] and not self.arucoFlag[2]:
            return 6
        else:
            return 9


    def detect_aruco_tag_bis(self, frame):
        '''Identify the aruco tag and create a structure encapsulating its information'''
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
        '''Test if the aruco detected is currently the one the robot should be looking for.'''
        list = self.arucoList
        self.rotationDuration = None
        self.arucoToFind =  None
        
        for aruco in list : 
            print(aruco["id"])
            if aruco["id"] == self.get_marker_to_find():
                self.arucoToFind = aruco
        
   
    def run(self, frame, motor):
        '''The main function'''

        self.detect_aruco_tag_bis(frame)
        #print("detect okk")
        self.catch_aruco()
        if self.arucoToFind :
            print( "A CHERCHER ", self.arucoToFind["id"] )

        if (not self.arucoToFind and not self.stop_flag):
            print("########## HUNTING ############")
            self.hunting(-1) 
        elif (not self.stop_flag):
            print("########## GO TO MARKER ########", self.arucoToFind["id"])
            self.go_to_aruco(frame)
        else :
            self.direction = 3
            self.speed = 0
        
        mc.updateMotor(motor, self.direction, self.speed, self.moveDuration)
    
    def go_to_aruco(self, frame):
        '''Calculates all the movement parameters according to the distance between the aruco and the robot'''
        height, width = frame.shape[:2]
        frame_center = width//2
        
        if self.arucoToFind and self.arucoToFind["dist"] > tolerance:
            print(self.arucoToFind["dist"])

            # ping the server when the targetted aruco is found
            mylib.pg()
            
            # here the robot speed and movement duration are determined by the distance between

            if self.arucoToFind["dist"] > 5 * tolerance: 
                self.speed = FWD_SPEED*2
                self.moveDuration = 1.5
            elif self.arucoToFind["dist"] > 3 * tolerance:
                self.speed = FWD_SPEED*2
                self.moveDuration = .5
            else :
                self.speed = FWD_SPEED
                self.moveDuration = .5

            if self.arucoToFind["center"][0] < frame_center: 
                self.direction = -.2
            else: 
                self.direction = .2
        else:

            # here the aruco we are looking for is not detected yet so we engage the hunting mode
            if self.arucoToFind : 
                self.speed = FWD_SPEED
                self.direction = 0
            else : 
            
            # we do not have any aruco to find anymore so we stop the robot
                self.speed = 0
                self.direction = 0
        
        # we upadate the future aruco to find
        if self.arucoToFind and self.arucoToFind["dist"] < tolerance: 
            
            # in order to count arucos found until then 
            # we manage not to add the same aruco more than once
            if self.arucoToFind["id"] not in self.visited_Id :
                print(" add  ", self.arucoToFind["id"])
                self.visited_Id.append(self.arucoToFind["id"])
                mylib.pg()
            
            # renouveller les flags
            self.arucoFlag[len(self.visited_Id)-1] = True
            if self.arucoFlag[-1] == True:
                print("Finish finding all markers")
                self.speed = 0 
                self.direction = 0
                self.stop_flag = True
                mylib.arr()
            self.arucoToFind = None
