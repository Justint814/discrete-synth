import numpy as np
import time
import asyncio
from playsound import playsound
from scipy.io.wavfile import write
import soundfile as sf
import sounddevice as sd
from discrete_synth import Oscillator
from discrete_synth import Synth
import keyboard


my_osc = Oscillator(dir_name="0")
my_synth = Synth()

my_sinewave, my_frequency = my_osc.sine(432)
my_synth = Synth()
signals = my_synth.envelope(my_sinewave, my_frequency, 1, 0.5, 0.7, 0.4)
file_path = my_osc.save_wav("432_sine.wav", my_sinewave)

file_paths = []
for i, signal in enumerate(signals):
    file_path = f"432_sine_{i}.wav"
    file_paths.append(my_osc.save_wav(file_path, signal))

envelope_signals = []
for file in file_paths:
    data, samplerate = sf.read(file, dtype="float32")
    
    envelope_signals.append(data)

def play(signal, samplerate):
    key = 'space'

    while True:
        keyboard.wait(key)
        print('pressed')
        with sd.OutputStream(samplerate=samplerate, channels=1) as stream:
            while keyboard.is_pressed(key) == True:
                stream.write(signal.astype(np.float32))

def play_env(signals, samplerate):
    key = 'space'

    while True:
        keyboard.wait(key)
        print('pressed')
        with sd.OutputStream(samplerate=samplerate, channels=1) as stream:
            stream.write(signals[0].astype(np.float32))  # Attack.
            stream.write(signals[1].astype(np.float32))  # Decay.

            while keyboard.is_pressed(key) == True:
                stream.write(signals[2].astype(np.float32))  # Sustain.

            stream.write(signals[3].astype(np.float32))  # Release.     

#play(data, samplerate)
play_env(envelope_signals, samplerate)