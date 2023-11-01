import motor_driver
import motor_controller as mc
import keyboard as kb
import time

inputdir = {
        'z' : 'FORWARD',
        's': 'BACKWARD',
        'q': 'LEFT',
        'd': 'RIGHT',
        'x': 'STOP'
}

defaultspeed = 100

def run(speed=defaultspeed):
        motor = mc.start(speed)
        while True:
                input = listen_kb()
                if input:
                        execute(motor, input, speed)
                else:
                        time.sleep(0.1)


def listen_kb():
        key = kb.read_key()
        if key in inputdir.keys():
                return inputdir[key]
        else:
                return None

def execute(motor, input):
        if input == 'FORWARD':
                mc.move_forward(motor)
        elif input == 'BACKWARD':
                mc.move_backward(motor)
        elif input == 'LEFT':
                mc.turn_left(motor)
        elif input == 'RIGHT':
                mc.turn_right(motor)
        elif input == 'STOP':
                mc.stop(motor)
        
        

