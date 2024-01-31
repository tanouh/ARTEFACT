import os
import time
import cv2
from . import stream_cam as s, realtime_detection as rd
import sys
sys.path.append("..")
from motor import motor_controller as mc


device_path = '/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0'


def streaming (motor, auto):
                detector = rd.Detector()
                streamer = s.Streamer()
                print("[STREAM] starting video stream...")

                time.sleep(0.5)
                try :   
                        while auto :
                                print(" [TEST] while ")
                                ret, frame = streamer.camera.read()
                                print(streamer.camera.read())
                                if not ret:
                                        break
                                detector.run(frame, motor)
                                # if func is not None :
                                #         print("go to detection ... ")
                                #         func(frame, motor)
                                # else : 
                                #         continue  # print("[STREAM] No function to read")
                                        
                except : 
                        streamer.release()
                        mc.stop_motor(motor)
                        time.sleep(10)
                        print("SHUTDOWN")



class Streamer():
        def __init__(self):
                self.camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.camera.set(cv2.CAP_PROP_FPS, 30)
                self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)




        def release(self):
                print("[STREAM] Ending video stream...")
                cv2.destroyAllWindows()
                self.camera.release()


