from flask import Flask, render_template , request
import webbrowser
from mylib import *
from multiprocessing import Process, Value
import motor_controller as mc 
import time
import sys
sys.path.append("..")
from camera import stream_cam as s


app = Flask(__name__)

hostname = 'robotpi-40'
ip_adress = '137.194.173.40'
rpi_port = 5000
motor = None
ping_flag = Value("b", True)
auto_flag = Value("b",False)
processes = []
delta = 0 

def launch_streaming():
    ''' Launch the camera streamin in a child process'''
    global auto_flag
    global motor
    global delta
    time.sleep(0.3)
    return(s.streaming(motor,auto_flag))
    # streamer.streaming(motor, detector.run, auto_flag.value)
    """
    p = Process(target = s.streaming, args = (motor, auto_flag,)) # open camera streaming and start auto mode
    p.start()
    if not auto_flag.value :
        p.terminate()
        p.join()
    return 
    """
def init_motor (flag):
    '''Initialize the motor driver'''
    global motor 
    global auto_flag
    if not motor:
        motor = mc.start_motor()
    auto_flag.value = flag
             
def auto():
    '''Engage the automatic mode'''
    print("go auto")
    init_motor(True)
    mc.move_forward(motor)
    time.sleep(7)
    mc.stop_motor(motor)
    launch_streaming()
    return 'go auto'

@app.route("/")
def index():
    global delta
    delta = time.time()
    return render_template('ui.html')

@app.route("/ping", methods=['POST', 'GET'])
def ping():
    pg()
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
    if motor:
        mc.stop_motor(motor)
        time.sleep(1)
    arr()
    return 'KILLED !'
    #prévenir que la voiture est partie

@app.route("/depart", methods = ['POST', 'GET'])
def depart():
    global ping_flag 
    ping_flag.value = False
    dep()
    p=Process(target=auto,args=())
    p.start()
    return ("Depart reçu")

@app.route("/video_stream")
def video_stream():
    return 'video_stream'
    # return Response(launch_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')
     
try:
    
    # ping_flag.value = True
    # pping = Process(target = pinging, args = (ping_flag,))
    # pping.start()
    # processes.append(pping)

    app.run(host=ip_adress, port=rpi_port, debug=True) # add port = rpi port 

except KeyboardInterrupt:
    if motor:
        mc.stop_motor(motor)
    for p in processes : 
        p.join()


    # pygame.init()
    

    
    
    