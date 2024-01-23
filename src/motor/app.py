from flask import Flask, render_template , request
import webbrowser
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

def launch_streaming():
        streamer = s.Streamer()
        time.sleep(0.5)
        global motor
        if not auto_mode : 
                return streamer.streaming(motor, None)
        else :
                detector = rd.Detector()
                return streamer.streaming(motor, detector.run)
        
def auto():
    print("go auto")
    global motor
    if not motor :
        motor = mc.start_motor()
    global auto_mode
    auto_mode = True
    mc.move_forward(motor)
    time.sleep(2)
    launch_streaming() # open camera streaming and start auto mode
    return 'go auto'

@app.route("/")
def index():
    return render_template('ui.html')

@app.route("/ping")
def myping():
    parameter = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", parameter, "1", "http://137.194.13.82:5000/com?nature=ping&id=b"]
    response = subprocess.call(command)

    if response == 0:
        return 'Ping successful'
    else:
        return 'Ping failed'
    
@app.route("/on")
def turn_on():
    global motor
    motor = mc.start_motor()
    print("Starting")
    return 'Starting...'

@app.route("/stop")
def stop():
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
    value=request.args.get('url')
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
    mc.stop_motor(motor)
    global auto_mode
    auto_mode = False
    return 'go manu'

@app.route("/kill")
def kill():
    mc.stop_motor(motor)
    return 'KILLED ! '

    #prévenir que la voiture est partie
   
@app.route("/start")
def start():
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
    
    