from camera.realtime_detection import detect_aruco_tags
from motor.app import app

hostname = 'robotpi-40'
ip_adress = '137.194.173.40'
rpi_port = 8080

mode = 0

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=rpi_port, debug=True)


