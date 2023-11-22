import os
import time
import cv2

device_path = '/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0'

class Streamer():
        def __init__(self):
                self.camera = cv2.VideoCapture(0)

        def connect_camera (self):
                os.sync()
                devices = []
                files = os.listdir('/dev/v4l/by-id')
                for file in files:
                        if file.startswith('video'):
                                devices.append(os.path.join('/dev', file))
                if device_path in devices :
                        print("[STREAM] Connecting to :", device_path)
                        self.camera = cv2.VideoCapture(device_path)
                        time.sleep(1.0)
                else : 
                        print(f"[STREAM] Failed to open {device_path}")

                
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