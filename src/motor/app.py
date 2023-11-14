from flask import Flask, render_template
import motor_controller as mc 

app = Flask(__name__)

hostname = 'robotpi-40'
ip_adress = '137.194.173.40'
port = 8080
motor = None

@app.route("/")
def index():
        return render_template('ui.html')

# enable mode choices for keyboard navigation or mouse navigation
@app.route("/kctrl")
def keyboard():
    return render_template('kctrl.html')

@app.route("/bctrl")
def button():
    return render_template('bctrl.html')

@app.route("/start")
def start():
    motor = mc.start_motor()
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

@app.route("/stop")
def stop():
    mc.stop_motor(motor)
    print("Stopping")
    return 'Stopping'

if __name__ == '__main__':
    app.run(ip_adress, port, debug=True) #add port = rpi port
      