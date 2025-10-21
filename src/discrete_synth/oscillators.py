import numpy as np
from scipy.io.wavfile import write
from playsound import playsound
import soundfile as sf
import sounddevice as sd
import os
import time

# Helper functions.

#Function to count directories in specified path (1 layer)
def count_dir(path):
	count = 0
	for entry in os.scandir(path):
		if entry.is_dir():
			count+=1
	return count


class Oscillator:
    def __init__(self, dir_name="0"):
        self.SAMPLE_RATE= 44100
        self.MAX_AMPLITUDE = 32767
        self.MIN_AMPLITUDE = -32768
        self.PI = 3.1415926535
        self.dir_name = dir_name
        
        # Make new data directory.
        self.mk_data_dir()


# Directory management.

    # Function to make new data directory for each object instance.
    def mk_data_dir(self):
        data_dir = "./data"

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        self.save_path = f"{data_dir}/data_{self.dir_name}"

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)


# Waveforms.

    def sine(self, freq: float, amplitude: float = 1):
        period = 1 / freq
        omega = 2 * self.PI * freq

        time_arr = np.linspace(0., period, int(period * self.SAMPLE_RATE), endpoint=False)
        signal = (self.MAX_AMPLITUDE * amplitude * np.sin(omega * time_arr)).astype(np.int16)  # Define signal as 16bit integer

        return signal


# Saving.

    def save_wav(self, filename, signal):
          file_path = f"{self.save_path}/{filename}"
          write(file_path, self.SAMPLE_RATE, signal)

          return file_path
