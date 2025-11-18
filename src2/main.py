from synth import Oscillator, Filter, Envelope, Synth
import numpy as np
import keyboard
import sounddevice as sd
import time

print("initializing...")

key = 'space'
sample_rate = 4096  # Hz

my_oscillators = [Oscillator(100, 1)]
sample_osc = Oscillator(100, 1)

my_envelope = Envelope(50E-2, 10E-2, 0.7, 10E-1, sample_rate)
my_filter = Filter(900, 1100, sample_rate)

my_synth = Synth(my_oscillators, my_envelope, my_filter, sample_rate)

print("starting loop")

ADSR_arr = []
with sd.OutputStream(samplerate=sample_rate, channels=1) as stream:
    while True:

        if keyboard.is_pressed(key):
            my_synth.keyPressed = True
        else:
            my_synth.keyPressed = False

        stream.write(my_synth.step())


        my_synth.keyPressedLast = my_synth.keyPressed
        


#ADSR_arr = np.array(ADSR_arr)
#np.save('/Users/justintraywick/Coding/discrete-synth/discrete-synth/data/ADSR_arr.npy', ADSR_arr, allow_pickle=True)
