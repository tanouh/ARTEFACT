from flask import Flask, render_template , request
import webbrowser
from multiprocessing import Process, Value
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

servers =["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]


def launch_streaming():
    global move_flag
    global motor
    streamer = s.Streamer()
    detector = rd.Detector()
    p = Process(target = streamer.streaming, args = (motor, detector.run)) # open camera streaming and start auto mode
    while move_flag.value : 
        p.start()
    p.terminate()
    p.join()
    return 

def init_motor (auto_flag):
    global motor 
    global move_flag
    if not motor:
        motor = mc.start_motor()
    if not move_flag.value : 
        move_flag.value = True
    global auto_mode 
    auto_mode = auto_flag
             
def auto():
    print("go auto")
    init_motor(auto_flag=True)
    mc.move_forward(motor)
    time.sleep(2)
    launch_streaming()
    return 'go auto'

def send_request(nature, ip):
    try: request.post("http://"+ip+"/com?nature="+nature+"&id=b",data={})
    except:
        return(False)
    return(True)

def communicate (list, nature):
    processes = []
    for i in list:
        p = Process(target=send_request, args=(nature, i))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

@app.route("/")
def index():
    return render_template('ui.html')

@app.route("/ping", methods=['POST'])
def ping():
    send_request("ping","Ping")
    return 'Sending ping ...'
    
@app.route("/on")
def turn_on():
    init_motor()
    print("Starting")
    return 'Starting...'

@app.route("/stop")
def stop():
    if auto_mode :
        global move_flag
        move_flag.value = False
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
    # modifier le speed ici ...

    return 'speed'

@app.route("/Auto")
def run():
    return auto()

@app.route("/Manu")
def manu():
    init_motor(auto_flag=False)
    return 'Go manu : en attente de commande'

@app.route("/kill", methods = ['POST', 'GET'])
def kill():
    global move_flag
    move_flag.value = False
    if motor :
        mc.move_forward(motor) 
        time.sleep(1)
    communicate(servers, "Im gone ! 8b")

    return 'KILLED !'
    #prévenir que la voiture est partie

@app.route("/depart", methods = ['POST', 'GET'])
def depart():
    send_request("depart", "Departure")

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
    
    