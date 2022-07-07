## Testing code for using the DAQ to sample the Current Sensor and LoadCell ##
import numpy as np

import nidaqmx
from nidaqmx import constants
from nidaqmx import stream_readers
import matplotlib.pyplot as plt
import time

import numpy as np
from threading import Thread

#user input Acquisition
Ch02_name = 'LoadCell'
Ch01_name = 'CurrentSensor'
Ch03_name = 'Sync'
num_channels = 1
fs_acq = 40000 #sample frequency
bufsize = 40000
data = np.zeros((num_channels,1))

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai1", name_to_assign_to_channel=Ch01_name,
                                        terminal_config= constants.TerminalConfiguration.BAL_DIFF, 
                                        min_val=-1, max_val=1)
    '''
    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai2", name_to_assign_to_channel=Ch02_name,
                                        terminal_config= constants.TerminalConfiguration.BAL_DIFF, 
                                        min_val=-1, max_val=1)

    task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/ai3", name_to_assign_to_channel=Ch03_name,
                                        terminal_config= constants.TerminalConfiguration.BAL_DIFF, 
                                        min_val=-1, max_val=1)'''

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

    
    task.start()
    time.sleep(3)
    task.stop()
    print(data)
    time.sleep(5)

'''choice = input('Are you ready kids?   ')
if choice == 'y':
    task.start()
    time.sleep(10)
    task.close()
else:
    print('Get fucked kid')'''