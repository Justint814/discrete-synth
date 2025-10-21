import numpy as np
import time
import asyncio
from playsound import playsound
from scipy.io.wavfile import write
import soundfile as sf
import sounddevice as sd
from discrete_synth import Oscillator
import keyboard


my_osc = Oscillator(dir_name="0")

my_sinewave = my_osc.sine(432)
file_path = my_osc.save_wav("432_sine.wav", my_sinewave)

data, samplerate = sf.read(file_path, dtype="float32")
data_2 = data * .75



def play(signal, samplerate):
    press = False
    loops = 0
     
    def on_release(event):
        nonlocal press
        press = False

    keyboard.wait("space")

    with sd.OutputStream(samplerate=samplerate, channels=1) as stream:
        while press == True:
            keyboard.on_release_key("space", on_release)
            stream.write(signal.astype(np.float32))


play(data, samplerate)