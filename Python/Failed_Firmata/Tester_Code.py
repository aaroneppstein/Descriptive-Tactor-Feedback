try: 
    from pyfirmata import Arduino, util, SERVO
except:
    import pip
    pip.main(['install','pyfirmata'])
    from pyfirmata import Arduino, util
import time
import pandas as pd
from HX711 import HX711
import sys


def map(x, in_min, in_max, out_min, out_max):           #Mapping analog to digital
    return int((x - in_min) * (out_max-out_min) / (in_max - in_min) + out_min)

#### Setup ####
port = 'COM5'

board = Arduino(port)             # USB Port COM5
iterator = util.Iterator(board)
iterator.start()

Servo = board.get_pin('d:3:p')      # Digitial Pin 3
Servo.mode = SERVO

Pot = board.get_pin('a:5:i')        # Analog Pin 5
Pot.enable_reporting()

curr_sens = board.get_pin('a:0:i')  # Analog Pin 0
curr_sens.enable_reporting

time.sleep(1.0)

'''
# Servo w/ Current Sensor
CS_vals = []

size_list1 = range(0,180,10)        
try:
    for s in size_list1:
        Servo.write(s)
        print(curr_sens.read())
        CS_vals.append(curr_sens.read())
        time.sleep(0.075)
    csv_out = {'Current Sensor': CS_vals}
    df = pd.DataFrame(csv_out)
    df.to_csv('tester.csv')
    board.exit()
except:
    board.exit()'''
    

#### Loop ####

'''
#Servo w/ Potentiometer
try:
    while True:
        Pot_val = Pot.read()
        val = map(Pot_val, 0, 1, 0, 180)        # For PyFirmata, analog is read in 0-1 rather than 0-1023 in arduino
        print(val)
        Servo.write(val)
        time.sleep(0.05)                        # 50 ms delay   
except KeyboardInterrupt:
    board.exit()'''


# Load Cell Example

dout = board.get_pin('d:4:i')
dout.enable_reporting()
pd_sck = board.get_pin('d:5:o')
hx = HX711(dout, pd_sck, gain=128)
#hx.set_offset(5592916.333333333)
hx.set_scale(1)
hx.tare(15)

while True:
    try:
        val = hx.get_units()
        print(val)

        hx.power_down()
        time.sleep(.001)
        hx.power_up()

        time.sleep(.01)
    except KeyboardInterrupt:
        board.exit()
        sys.exit()