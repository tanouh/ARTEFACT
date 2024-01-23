from flask import Flask, render_template , request
import webbrowser
from multiprocessing import Process, Value
import platform
import subprocess
import motor_controller as mc 
import time
import sys
sys.path.append("..")
from camera import stream_cam as s, realtime_detection as rd


app = Flask(__name__)

hostname = 'robotpi-40'
ip_adress = '137.194.173.40'
rpi_port = 5000
motor = None
ping_flag = True
auto_mode = False
move_flag = Value("b",False)

def launch_streaming():
    streamer = s.Streamer()
    time.sleep(0.5)
    global motor
    if auto_mode : 
            detector = rd.Detector()
            p = Process(target = streamer.streaming, args = ([motor, detector.run, move_flag.Value])) # open camera streaming and start auto mode
            p.start()
    return 
        
def auto():
    print("go auto")
    global move_flag
    move_flag.Value = True
    global motor
    if not motor :
        motor = mc.start_motor()
    global auto_mode
    auto_mode = True
    mc.move_forward(motor)
    time.sleep(2)
    launch_streaming()
    return 'go auto'
# Multi-threading à implémenter

@app.route("/")
def index():
    return render_template('ui.html')

@app.route("/ping", methods=['POST'])
def ping():
    request.post(url='http://137.194.127.137:5000/com?nature=ping&id=b',data={})
    return("Sent to", 'http://137.194.127.137:5000/com?nature=ping&id=b')
    
@app.route("/on")
def turn_on():
    global move_flag
    move_flag.Value = True
    global motor
    motor = mc.start_motor()
    print("Starting")
    return 'Starting...'

@app.route("/stop")
def stop():
    global move_flag
    move_flag.Value = False
    mc.stop_motor(motor)
    print("Stopping")
    return 'Stopping'

@app.route("/move_forward")
def move_forward():
    if not auto_mode : 
        mc.move_forward(motor)
        print('Moving forward')
    return 'Moving forward'

@app.route("/move_backward")
def move_backward():
    if not auto_mode : 
        mc.move_backward(motor)
        print('Moving backward')
    return 'Moving backward'

@app.route("/turn_left")
def turn_left():
    if not auto_mode :  
        mc.turn_left(motor)
        print('Turning left')
    return 'Turning left'

@app.route("/turn_right")
def turn_right():
    if not auto_mode : 
        mc.turn_right(motor)
        print("Turning right")
    return 'Turning right'

@app.route("/move_right_forward")
def move_right_forward():
    if not auto_mode:
        mc.move_right_forward(motor)
        print("Turning right forward")
    return 'Turning right forward'

@app.route("/move_left_forward")
def move_left_forward():
    if not auto_mode :
        mc.move_left_forward(motor)
        print("Turning left forward")
    return 'Turning left forward'

@app.route('/speed', methods=['POST'])
def speed():
    data = request.get_json() # Récupère les données envoyées
    speed = data.get('value') # Accède à la valeur entière
    mc.modify_speed(motor,speed) # Change la vitesse
    print(speed) # Affiche la valeur reçue dans la console
    return 'speed'

@app.route("/requesting",methods=["POST"])
def requesting():
    value='http://137.194.1:5000/com?nature=ping&id=b'
    request.post(url=value,data={})
    return("Sent to", value)

@app.route("/sendrequest",methods=["GET"])
def sendrequest():
    return render_template('request.html')

@app.route("/Auto")
def run():
    return auto()

@app.route("/Manu")
def manu():
    print("go manu")
    global move_flag
    move_flag.Value = True
    mc.stop_motor(motor)
    global auto_mode
    auto_mode = False
    return 'go manu'

@app.route("/kill", methods = ['POST', 'GET'])
def kill():
    if move_flag.value == False : 
        if not motor :
            print("Motor ")
            mc.stop_motor(motor)
            time.sleep(.5)
            mc.move_forward(motor) 
            time.sleep(.5)
    return 'KILLED ! '

    #prévenir que la voiture est partie
   
@app.route("/depart", methods = ['POST', 'GET'])
def depart():
    return auto()

@app.route("/video_stream")
def video_stream():
    return 'video_stream'
    # return Response(launch_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')
     

if __name__ == '__main__':
    try:
        app.run(host=ip_adress, port=rpi_port, debug=True) # add port = rpi port
        # Ouvrir le navigateur vers l'URL du serveur
        url = f"http://{ip_adress}:{rpi_port}"
        webbrowser.open_new(url)
    
    except KeyboardInterrupt:
        mc.stop_motor(motor)
    
    