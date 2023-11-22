import os
import time
import cv2
from . import stream_cam as s, realtime_detection as rd

device_path = '/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0'

class Streamer():
        def __init__(self):
                self.camera = cv2.VideoCapture(0)
                # self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

               
        def streaming (self,motor, func):
                print("[STREAM] starting video stream...")
                while True :
                        ret, frame = self.camera.read()
                        if not ret:
                                break
                        if func is not None :
                                func(frame, motor)
                        else : 
                                print("[STREAM] No function to read")

                print("[STREAM] ending video stream...")
                cv2.destroyAllWindows()
                self.camera.release()


