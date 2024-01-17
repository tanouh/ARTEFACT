import os
import time
import cv2
from . import stream_cam as s, realtime_detection as rd

device_path = '/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0'

class Streamer():
        def __init__(self):
                self.camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
                print(self.camera)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.camera.set(cv2.CAP_PROP_FPS, 30)
                self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)


               
        def streaming (self,motor, func):
                print("[STREAM] starting video stream...")
                ret, frame = self.camera.read()
                print(frame)
                time.sleep(0.2)
                try :
                        while True :
                                ret, frame = self.camera.read()
                                print(ret)
                                if not ret:
                                        break
                                if func is not None :
                                        func(frame, motor)
                                else : 
                                        # print("[STREAM] No function to read")
                                        continue

                        print("[STREAM] ending video stream...")
                        cv2.destroyAllWindows()
                        self.camera.release()

                except : 
                        print("SHUTDOWN TO DO")

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

        # def streaming(self, motor, func):
        #         if func is None:
        #                 return self.generate_frames_without_processing(motor)
        #         else:
        #                 return self.generate_frames(motor, func)

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


