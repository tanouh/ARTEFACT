from flask import Flask, render_template , request
import webbrowser
from multiprocessing import Process, Value
import motor_controller as mc 
import time
import sys
import pygame
from pygame.locals import *
sys.path.append("..")
from camera import stream_cam as s, realtime_detection as rd


app = Flask(__name__)

hostname = 'robotpi-40'
ip_adress = '137.194.173.40'
rpi_port = 8000
motor = None
ping_flag = Value("b", True)
auto_flag = Value("b",False)
processes = []

servers = ["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]


def launch_streaming():
    global auto_flag
    global motor
    time.sleep(0.3)
    # streamer.streaming(motor, detector.run, auto_flag.value)
    p = Process(target = s.streaming, args = (motor, auto_flag.value)) # open camera streaming and start auto mode
    p.start()
    if not auto_flag.value :
        p.terminate()
        p.join()
    return 

def init_motor (flag):
    global motor 
    global auto_flag
    if not motor:
        motor = mc.start_motor()
    auto_flag.value = flag
             
def auto():
    print("go auto")
    mc.move_forward(motor)
    time.sleep(2)
    mc.stop_motor(motor)
    launch_streaming()
    return 'go auto'

def send_request(nature, ip):
    try: request.post("http://"+ip+"/com?nature="+nature+"&id=b",data={})
    except:
        return(False)
    return(True)

def communicate (list, nature):
    global processes
    for i in list:
        p = Process(target=send_request, args=(nature, i))
        processes.append(p)
        p.start()

def pinging ():
    global ping_flag
    while ping_flag.value : 
        communicate(servers, "ping")

@app.route("/")
def index():
    return render_template('ui.html')

@app.route("/ping", methods=['POST'])
def ping():
    communicate(servers, "ping")
    return 'Sending ping ...'
    
@app.route("/on")
def turn_on():
    global ping_flag
    ping_flag.value = True 
    init_motor(False)
    print("Starting")
    return 'Starting...'

@app.route("/stop")
def stop():
    global auto_flag
    if auto_flag.value :
        auto_flag.value = False
    mc.stop_motor(motor)
    print("Stopping")
    return 'Stopping'

@app.route("/move_forward")
def move_forward():
    if not auto_flag.value : 
        mc.move_forward(motor)
        print('Moving forward')
    return 'Moving forward'

@app.route("/move_backward")
def move_backward():
    if not auto_flag.value : 
        mc.move_backward(motor)
        print('Moving backward')
    return 'Moving backward'

@app.route("/turn_left")
def turn_left():
    if not auto_flag.value :  
        mc.turn_left(motor)
        print('Turning left')
    return 'Turning left'

@app.route("/turn_right")
def turn_right():
    if not auto_flag.value : 
        mc.turn_right(motor)
        print("Turning right")
    return 'Turning right'

@app.route("/move_right_forward")
def move_right_forward():
    if not auto_flag.value:
        mc.move_right_forward(motor)
        print("Turning right forward")
    return 'Turning right forward'

@app.route("/move_left_forward")
def move_left_forward():
    if not auto_flag.value :
        mc.move_left_forward(motor)
        print("Turning left forward")
    return 'Turning left forward'

@app.route('/speed', methods=['POST'])
def speed():
    data = request.get_json() # Récupère les données envoyées
    speed = data.get('value') # Accède à la valeur entière   
    # modifier le speed ici ...
    return 'speed'

@app.route("/Auto")
def run():
    init_motor(True)
    return auto()

@app.route("/Manu")
def manu():
    init_motor(False)
    # init_joystick()
    return 'Go manu : en attente de commande'

@app.route("/kill", methods = ['POST', 'GET'])
def kill():
    global auto_flag
    auto_flag.value = False
    if motor :
        mc.move_forward(motor) 
        time.sleep(1)
    communicate(servers, "kill")
    return 'KILLED !'
    #prévenir que la voiture est partie

@app.route("/depart", methods = ['POST', 'GET'])
def depart():
    communicate(servers, "depart")
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

        pping = Process(target = pinging, args = {})
        pping.start()
        processes.append(pping)

    except KeyboardInterrupt:
        if motor:
            mc.stop_motor(motor)
        for p in processes : 
            p.join()


    # pygame.init()
    

    
    
    