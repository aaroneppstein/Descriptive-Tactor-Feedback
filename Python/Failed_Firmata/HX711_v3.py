
import time
import sys


def createBoolList(size=8):
    ret = []
    for i in range(8):
        ret.append(False)
    return ret


class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        #GPIO.output(self.PD_SCK, True)
        #GPIO.output(self.PD_SCK, False)

        self.set_gain(gain);

    def is_ready(self):
        return self.DOUT.read() == 0

    def set_gain(self, gain):
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2

        self.PD_SCK.write(0)
        self.read()

    def read(self):
        while not self.is_ready():
            #print("WAITING")
            pass

        dataBits = [createBoolList(), createBoolList(), createBoolList()]

        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                self.PD_SCK.write(1)
                dataBits[j][i] = self.DOUT.read()
                self.PD_SCK.write(0)

        #set channel and gain factor for next reading
        #for i in range(self.GAIN):
        self.PD_SCK.write(1)
        self.PD_SCK.write(0)

        #check for all 1
        if all(item == True for item in dataBits[0]):
            return self.lastVal

        bits = []
        for i in range(2, -1, -1):
            bits += dataBits[i]

        self.lastVal = int(''.join(map(str, bits)), 2)
        return self.lastVal

        '''
        data = [0,0,0]
        for i in range(0,3):
            #print(''.join(map(str, dataBits[i])))
            data[i] = int(''.join(map(str, dataBits[i])), 2)
            #print(data[i])
        #data[2] ^= 0x80
        return data[2] << 16 | data[1] << 8 | data[0]
        '''

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()

        return sum / times

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        self.PD_SCK.write(0)
        self.PD_SCK.write(1)

    def power_up(self):
        self.PD_SCK.write(0)
        
'''############# EXAMPLE
hx = HX711(9, 11)
hx.set_scale(7050)
hx.tare()

while True:
    try:
        val = hx.get_units(3)
        if val > 100:
            print("OH NO")
        #hx.power_down()
        #time.sleep(.001)
        #hx.power_up()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()'''