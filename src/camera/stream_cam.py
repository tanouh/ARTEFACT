import os
import time
import cv2
from . import stream_cam as s, realtime_detection as rd
import sys
sys.path.append("..")
from motor import motor_controller as mc


device_path = '/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0'


def streaming (motor, auto):
        '''Engage the streaming'''
        detector = rd.Detector()
        streamer = s.Streamer()
        
        print("[STREAM] starting video stream...")

        time.sleep(0.5)
        try :   
                while auto.value :
                        ret, frame = streamer.camera.read()
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

               
        # def streaming (self,motor, func):
        #         print("[STREAM] starting video stream...")
        #         while True :
        #                 ret, frame = self.camera.read()
        #                 if not ret:
        #                         break
        #                 if func is not None :
        #                         func(frame, motor)
        #                 else : 
        #                         print("[STREAM] No function to read")

        #         print("[STREAM] ending video stream...")
        #         cv2.destroyAllWindows()
        #         self.camera.release()

        def generate_frames(self, motor, func):
                print("[STREAM] Starting video stream...")
                while True:
                        ret, frame = self.camera.read()
                        if not ret:
                                break
                        if func is not None:
                                func(frame, motor)  # 处理图像的函数，如果需要的话

                        ret, buffer = cv2.imencode('.jpg', frame)
                        if not ret:
                                break

                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        def streaming(self, motor, func):
                if func is None:
                        return self.generate_frames_without_processing(motor)
                else:
                        return self.generate_frames(motor, func)

        def generate_frames_without_processing(self, motor):
                print("[STREAM] Starting video stream without processing...")
                while True:
                        ret, frame = self.camera.read()
                        if not ret:
                                break
                        ret, buffer = cv2.imencode('.jpg', frame)
                        if not ret:
                                break
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        def release(self):
                print("[STREAM] Ending video stream...")
                cv2.destroyAllWindows()
                self.camera.release()


