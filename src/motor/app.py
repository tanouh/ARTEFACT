from flask import Flask, render_template
import motor_controller as mc 

app = Flask(__name__)

motor = mc.start_motor()

@app.route("/")
def index():
        return render_template('ui.html')

@app.route("/move_forward")
def move_forward():
    mc.move_forward(motor)
    return 'Moving forward'

@app.route("/move_backward")
def move_backward():
      mc.move_backward(motor)
      return 'Moving backward'

@app.route("/turn_left")
def turn_left():
      mc.turn_left(motor)
      return 'Turning left'

@app.route("/turn_right")
def turn_right():
      mc.turn_right(motor)
      return 'Turning right'

if __name__ == '__main':
      app.run(debug=True)