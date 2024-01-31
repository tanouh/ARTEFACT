import os
import time
import cv2
from . import stream_cam as s, realtime_detection as read
import sys
sys.path.append("..")
from motor import motor_controller as mc

device_path = '/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0'

class Streamer():
        def __init__(self):
                self.camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.camera.set(cv2.CAP_PROP_FPS, 30)
                self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)


               
        def streaming (self,motor, func):
                print("[STREAM] starting video stream...")
                time.sleep(0.5)
                try :   
                        # while True :
                        ret, frame = self.camera.read()
                        if not ret:
                                return
                        if func is not None :
                                func(frame, motor)
                        else : 
                               return  # print("[STREAM] No function to read")
                                
                except : 
                        self.release()
                        mc.stop_motor(motor)
                        time.sleep(10)
                        print("SHUTDOWN")


        def release(self):
                print("[STREAM] Ending video stream...")
                cv2.destroyAllWindows()
                self.camera.release()


