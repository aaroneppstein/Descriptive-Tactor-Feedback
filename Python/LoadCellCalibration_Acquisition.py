'''
To be used in conjunction with Experimental_Setup.ino
Syncs Arduino and DAQ by writing to serial to start arduino and starting DAQ for data acquisition
Written by Aaron Eppstein
'''

'''try: 
    import serial
except:
    import pip
    pip.main(['install','pyserial'])
    import serial'''

import serial
import nidaqmx
from nidaqmx import constants
from nidaqmx import stream_readers
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

## Arduino Initialization ##
port = 'COM5'
# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial(port, 9600, timeout=1)
time.sleep(2)
print('Connection Established with Arduino')
time.sleep(2)


## DAQ Initialization ##

#user input Acquisition
Ch02_name = 'LoadCell'
Ch01_name = 'CurrentSensor'
Ch03_name = 'Sync'
num_channels = 1
fs_acq = 40000 #sample frequency
bufsize = 40000
data = np.zeros((num_channels,1))


with nidaqmx.Task() as task:
    '''task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai1", name_to_assign_to_channel=Ch01_name,
                                        terminal_config= constants.TerminalConfiguration.BAL_DIFF, 
                                        min_val=-5, max_val=5)'''
    
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai2", name_to_assign_to_channel=Ch02_name,
                                        terminal_config= constants.TerminalConfiguration.BAL_DIFF, 
                                        min_val=-5, max_val=5)

    '''task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai3", name_to_assign_to_channel=Ch03_name,
                                        terminal_config= constants.TerminalConfiguration.BAL_DIFF, 
                                        min_val=-5, max_val=5)'''

    task.timing.cfg_samp_clk_timing(rate=fs_acq, sample_mode=constants.AcquisitionType.CONTINUOUS, samps_per_chan=bufsize) # you may not need samps_per_chan
                                    
    # I set an input_buf_size
    samples_per_buffer = int(fs_acq // 40)  # 400 hz update
    # task.in_stream.input_buf_size = samples_per_buffer * 10  # plus some extra space

    reader = stream_readers.AnalogMultiChannelReader(task.in_stream)

    def reading_task_callback(task_idx, event_type, num_samples, callback_data=None):
        """After data has been read into the NI buffer this callback is called to read in the data from the buffer.

        This callback is for working with the task callback register_every_n_samples_acquired_into_buffer_event.

        Args:
            task_idx (int): Task handle index value
            event_type (nidaqmx.constants.EveryNSamplesEventType): ACQUIRED_INTO_BUFFER
            num_samples (int): Number of samples that was read into the buffer.
            callback_data (object)[None]: No idea. Documentation says: The callback_data parameter contains the value
                you passed in the callback_data parameter of this function.
        """
        global data
        buffer = np.zeros((num_channels, num_samples), dtype=np.float64)
        reader.read_many_sample(buffer, num_samples, timeout=constants.WAIT_INFINITELY)

        # Convert the data from channel as a row order to channel as a column
        data = np.append(data,buffer.T.astype(np.float64))

        # Do something with the data
        
    task.register_every_n_samples_acquired_into_buffer_event(samples_per_buffer, reading_task_callback)


    
    #### Main.py ####
    try:    
        while True:
            line = ser.readline()   # read a byte
            if line:
                string = line.decode()  # convert the byte string to a unicode string
                print(string)
            choice = input('Ready ? (y/n) ')
            ser.write(bytes(choice, 'utf-8'))
            if choice == 'y' or choice == 'Y':
                task.start()                                    # Starting DAQ data acquisition
                while True:
                    line = ser.readline()   # read a byte
                    if line:
                        string = line.decode()  # convert the byte string to a unicode string
                        #num = int(string) # convert the unicode string to an int
                        if 'break' in string:
                            task.stop()
                            np.append(data,np.zeros((num_channels,1)))
                            break
            if choice == 'n' or choice == 'N':
                #csv_out = {'Servo Position (degrees)': Servo_Pos, 'Current Sensor (mA)': CS_vals, 'Load Cell (g)': LC_vals}    # Write record data from Current Sensor and Load Cell to CSV or JSON
                df = pd.DataFrame(data, columns=['LoadCell'])
                df.to_csv('LoadCell_Data.csv')
                for i in range(20):
                    print('Python go brrrr')
                ser.close()
                #task.close()
                time.sleep(3)               # Letting the threads close out, so we dont get a daemon error
                break
    except KeyboardInterrupt:   
        ser.close()
        #task.close()
        time.sleep(3)
