
import nidaqmx

# Let's load up the NI-DAQmx system that is visible in the
# Measurement & Automation Explorer (MAX) software of NI-DAQmx for
# the local machine.
system = nidaqmx.system.System.local()
# We know on our current system that our DAQ is USB-6210
DAQ_device = system.devices['DAQ1']
# create a list of all the counters available on 'DAQ1'
counter_names = [ci.name for ci in DAQ_device.ci_physical_chans]
print(counter_names)
# note that using the counter output channels instead of the inputs
# includes the '[device]/freqout' output, which is not a counter
print([co.name for co in DAQ_device.co_physical_chans])