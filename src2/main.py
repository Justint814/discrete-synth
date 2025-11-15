from synth import Oscillator, Filter, Envelope, Synth
import numpy as np
import keyboard
import sounddevice as sd
import time

print("initializing...")

key = 'space'
sample_rate = float(48000)  # Hz
period = float(1 / sample_rate) # s

my_oscillators = [Oscillator(200, 1)]
sample_osc = Oscillator(350, 1)

my_envelope = Envelope(50E-3, 10E-3, 0.7, 10E-3)
my_filter = Filter(100, 300, sample_rate)

my_synth = Synth(my_oscillators, my_envelope, my_filter, sample_rate)

print("starting loop")

with sd.OutputStream(samplerate=sample_rate, channels=1) as stream:
    while True:

        if keyboard.is_pressed(key):
            my_synth.keyPressed = True
        else:
            my_synth.keyPressed = False

        stream.write(my_synth.step())



        