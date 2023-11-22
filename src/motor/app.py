from flask import Flask, render_template , request
import motor_controller as mc 

app = Flask(__name__)

hostname = 'robotpi-40'
ip_adress = '137.194.173.40'
rpi_port = 8080
motor = None

@app.route("/")
def index():
        return render_template('ui.html')

# enable mode choices for keyboard navigation or mouse navigation
"""@app.route("/kctrl")
def keyboard():
    return render_template('kctrl.html')

@app.route("/bctrl")
def button():
    return render_template('bctrl.html')"""

@app.route("/start")
def start():
    global motor 
    motor = mc.start_motor() #ce n'est oas modifé autre part ! A voir
    print("Starting")
    return 'Starting...'

@app.route("/move_forward")
def move_forward():
    mc.move_forward(motor)
    print('Moving forward')
    return 'Moving forward'

@app.route("/move_backward")
def move_backward():
    mc.move_backward(motor)
    print('Moving backward')
    return 'Moving backward'

@app.route("/turn_left")
def turn_left():
    mc.turn_left(motor)
    print('Turning left')
    return 'Turning left'

@app.route("/turn_right")
def turn_right():
    mc.turn_right(motor)
    print("Turning right")
    return 'Turning right'

@app.route("/move_right_forward")
def move_right_forward():
    mc.move_right_forward(motor)
    print("Turning right forward")
    return 'Turning right forward'

@app.route("/move_left_forward")
def move_left_forward():
    mc.move_left_forward(motor)
    print("Turning left forward")
    return 'Turning left forward'

@app.route("/stop")
def stop():
    mc.stop_motor(motor)
    print("Stopping")
    return 'Stopping'

@app.route('/speed', methods=['POST'])
def speed():
    data = request.get_json() # Récupère les données envoyées
    speed = data.get('value') # Accède à la valeur entière
    mc.modify_speed(motor,speed) #Change la vitesse
    print(speed) # Affiche la valeur reçue dans la console
    return 'speed'

if __name__ == '__main__':
    app.run(host=ip_adress, port=rpi_port, debug=True) #add port = rpi port
      