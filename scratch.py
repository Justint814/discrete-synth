from playsound import playsound
import numpy as np
from scipy.io.wavfile import write

sample_rate = 44100  # 44100Hz for CD quality.
duration = 5  # 5s.
bounds = [-32768, 32767]

# Specify time length
t = np.linspace(0., duration, int(duration*sample_rate), endpoint=False)

# Sine wave.
norm_A = 0.5  # Normalized amplitude (between 0 and 1).
freq = 432  # 432Hz frequency.
data = norm_A * np.sin(432 * 2 * np.pi * t)
data_scaled = (data * bounds[1]).astype(np.int16)

# line?.
period = 1 / freq
def sawtooth(freq, A, L, sample_rate=44100, scale_lim=32767):
    period = 1 / freq
    #t = np.linspace(0., L, int(L*sample_rate), endpoint=False)
    period_ind_len = int(period * sample_rate)
    cycle = []
    num_cycles = int(L * freq)

    for j in range(period_ind_len):
        y = (2 * A / L) * j - A
        cycle.append(y)

    cycle = np.array(cycle)
    data = np.tile(cycle, num_cycles)
    
    data_scaled = np.array(scale_lim * data).astype(np.int16)

    return data_scaled

sawtooth_wave = sawtooth(200, 1, 2)

# Save data as .wav file.
out_file = "./data/sawtooth.wav"
write(out_file, sample_rate, sawtooth_wave)

playsound(out_file)