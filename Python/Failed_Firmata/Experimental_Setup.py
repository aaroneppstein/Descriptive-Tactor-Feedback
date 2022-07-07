#### Experimental Setup ####
    # Programmed by Aaron Eppstein
    # For use with Tactor system
    # Originally Designed by Justin Tai
    # Redesigned by Aaron Eppstein

try: 
    from pyfirmata import Arduino, util, SERVO
except:
    import pip
    pip.main(['install','pyfirmata'])
    from pyfirmata import Arduino, util, SERVO
import time
from HX711 import HX711
from LoadCell_Calibration import LCC
import pandas as pd


#### Initialize Arduino Board ####
def exp_setup():

    servo.write(0)                  # write to position 0 (fully retracted)
    servo.write()                  # Set Servo to position equivalent to 5 N

    choice = input('Is it calibrated Y/n')   # Is it calibrated Y/n (Print)   (Weight in grams needs to be converted to N)
    if choice == 'n' or choice == 'N':         # if N - Calibrate scale to find offset of Syndaver as weight so its zeroed
        LCC.setup()
        LCC.calibrate()
        while True:
            LCC.loop()

    if choice == 'y' or choice == 'Y':                  # if Y - Set Scale with Syndaver weight as offset
        pass
    

def exp_loop():
    
    CS_vals = []                     # Start recording Current Sensor
    LC_vals = []                     # Start recording Load Cell

    ## ANSI/ISA-S51.1 ##
    test_num = []
    if test_num:
        test_num += 1
    else:
        test_num = 1
    
    choice = input('Start Test {} ? Y/n'.format(test_num))        # Start Test # ? Y/n
    if choice == 'y' or choice == 'Y':
        CS_vals.append('Test {}'.format(test_num))
        LC_vals.append('Test {}'.format(test_num))

        #Speed of Servo = Degree of Movement/Time Delay ~~in degree/s
        for pos_set1 in range(pos_5N,pos_10N,5):   # Move Servo to position equivalent to 10 N @5degrees inc
            servo.write(pos_set1)
            CS_vals.append(curr_sens.read())       # Recording Current Sensor
            LC_vals.append(hx.get_grams())         # Recording Load Cell
            time.sleep(0.05)                       # 50 ms Delay

        for pos_set2 in range(pos_10N,pos_0N,5):   # Move Servo to position equivalent to 0 N @5degrees inc
            servo.write(pos_set2)
            CS_vals.append(curr_sens.read())       # Recording Current Sensor
            LC_vals.append(hx.get_grams())         # Recording Load Cell
            time.sleep(0.05)                       # 50 ms Delay

        for pos_set3 in range(pos_0N,pos_5N,5):    # Move Servo to position equivalent to 5 N @5degrees inc
            servo.write(pos_set3)
            CS_vals.append(curr_sens.read())       # Recording Current Sensor
            LC_vals.append(hx.get_grams())         # Recording Load Cell
            time.sleep(0.05)                       # 50 ms Delay
        
    if choice == 'n' or choice == 'N':
        csv_out = {'Current Sensor': CS_vals, 'Load Cell': LC_vals}    # Write record data from Current Sensor and Load Cell to CSV or JSON
        df = pd.DataFrame(csv_out)
        df.to_csv('Tactor.csv')
        board.exit()
        break
    

#### Main Loop of Code) ####
if __name__ == '__main__':
    
    link = 'COM5'
    board = Arduino(link)
    iterator = util.Iterator(board)
    iterator.start()

    ## Servo ##
    servo = board.get_pin('d:3:o')      # Digital Pin 3
    servo.mode = SERVO

    ## Current Sensor ##
    curr_sens = board.get_pin('a:0:i')  # Analog Pin 0
    curr_sens.enable_reporting

    ## Load Cell ##
    pd_sck = board.get_pin('d:4:o')     # Digital Pin 4
    dout = board.get_pin('d:5:i')       # Digital Pin 5
    hx = HX711(link, pd_sck, dout, gain = 128)

    time.sleep(1.0)
    exp_setup()
    try:
        while True:
            exp_loop()
    except KeyboardInterrupt:
        board.exit()

