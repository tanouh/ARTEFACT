from camera  import stream_cam as s
from camera import realtime_detection as rd
from motor.app import app

hostname = 'robotpi-40'
ip_adress = '137.194.173.40'
rpi_port = 8080

mode_auto = 1

if __name__ == '__main__':
        streamer = s.Streamer()
        app.start()
        if mode_auto == 0 : 
                streamer.streaming(app.motor, None)
        else :
                detector = rd.Detector()
                streamer.streaming(app.motor, detector.detect_aruco_tags)

        #app.run(host='0.0.0.0', port=rpi_port, debug=True)


