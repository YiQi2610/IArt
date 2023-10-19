#!/usr/bin/env python

import time
import datetime
from max30105 import MAX30105, HeartRate
import numpy as np
import os

max30105 = MAX30105()
max30105.setup(leds_enable=2)

max30105.set_led_pulse_amplitude(1, 0.2)
max30105.set_led_pulse_amplitude(2, 12.5)
max30105.set_led_pulse_amplitude(3, 0)

max30105.set_slot_mode(1, 'red')
max30105.set_slot_mode(2, 'ir')
max30105.set_slot_mode(3, 'off')
max30105.set_slot_mode(4, 'off')

hr = HeartRate(max30105)

tab=[]

try :
    for j in range(1000):
        samples = max30105.get_samples()
        if samples is not None:
            for i in range(0, len(samples), 2):
                ir = samples[i+1] & 0xff
                d = hr.low_pass_fir(ir)
            
            tab.append(int(d/2))
            time.sleep(1.0/100)

except KeyboardInterrupt:
    pass

bpm = str(np.mean(tab))
print(bpm + " BPM\n")

os.chdir(os.path.dirname(os.path.realpath(__file__)))

temp = max30105.get_temperature()
print("{:.2f}".format(temp) + " °C\n")
with open('../data_to_send/send_heartrate.txt', 'w') as f:
	f.write(bpm)
	f.close()
