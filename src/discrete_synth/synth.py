import numpy as np
from discrete_synth import Oscillator

class Synth:
    def _init__(self):
        self.MAX_AMPLITUDE = 32767

    @classmethod
    def time_to_cycles(cls, time, frequency):
        return int(time * frequency)
    
    @classmethod
    def linear_attack(cls, signal, num_cycles):
        signal_length = len(signal)
        delta_amplitude = 1 / num_cycles
        amplitudes = delta_amplitude * np.repeat(np.arange(1, num_cycles + 1), signal_length)

        attack_signal = (np.tile(signal, num_cycles) * amplitudes).astype(np.int16)

        return attack_signal
    
    @classmethod
    def linear_decay(cls, signal, sustain_amplitude, num_cycles):
        signal_length = len(signal)
        amplitude_diff = (1 - sustain_amplitude)
        delta_amplitude = amplitude_diff / num_cycles
        amplitudes = sustain_amplitude + delta_amplitude * np.repeat(np.arange(num_cycles, 0, -1), signal_length)

        decay_signal = (np.tile(signal, num_cycles) * amplitudes).astype(np.int16)

        return decay_signal

    def envelope(self, signal, frequency, attack_time, decay_time, release_time, sustain_amplitude, attack_curve="linear", decay_curve="linear", samplerate=44100):  # time in seconds.
        attack_cycles = Synth.time_to_cycles(attack_time, frequency)
        decay_cycles = Synth.time_to_cycles(decay_time, frequency)
        release_cycles = Synth.time_to_cycles(release_time, frequency)

        # Attack.
        if attack_curve == "linear":
            attack_signal = Synth.linear_attack(signal, attack_cycles)
        
        # Decay.
        if decay_curve == "linear":
            decay_signal = Synth.linear_decay(signal, sustain_amplitude, decay_cycles)
        
        # Sustain.
        sustain_signal = np.int16(sustain_amplitude * signal)

        # Release.
        release_signal = Synth.linear_decay(sustain_signal, 0, release_cycles)  # Use linear decay function as release.

        return [attack_signal, decay_signal, sustain_signal, release_signal]



        