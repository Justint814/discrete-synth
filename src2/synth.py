from math import *
import numpy as np

class Oscillator(object):
	def __init__(self, frequency, amplitude):
		self.frequency = frequency
		self.amptilude = amplitude
		self.t = 0
		self.output = 0

	def step(self, sampleRate):
		period = sampleRate/self.frequency
		increment = 2*pi/period
		t = self.t
		self.t += increment
		if self.t > pi*0.5:
			self.t = 0
		return self.amplitude*sin(2*pi*self.frequency*self.t)

class Envelope(object):
	def __init__(self, attack_t, decay_t, sustain_amp, release_t):
		self.attack_t = attack_t
		self.decay_t = decay_t
		self.attack_decay_t = self.attack_t + self.decay_t
		self.sustain_amp = sustain_amp
		self.release_t = release_t
		self.input = 0
		self.output = 0
		self.t = 0 # In seconds.

	@classmethod
	def linear_attack(cls, t, attack_t, MAX_AMP=1):
		return (t * MAX_AMP)/ attack_t
	
	@classmethod
	def linear_decay(cls, dt, decay_t, MAX_AMP=1):
		return MAX_AMP - (dt * MAX_AMP)/ decay_t
	
	@classmethod
	def exponential_attack(cls, t, attack_t, MAX_AMP=1):
		return np.exp(t - attack_t)
	
	@classmethod
	def exponential_decay(cls, t, attack_t, MAX_AMP=1):
		return np.exp(-(t - 5 + attack_t))

	def step(self, sampleRate, keyPressed):
		increment = 1/sampleRate
		t = self.t

		if keyPressed:
			self.t += increment
			if t <= self.attack_t:
				return self.input * Envelope.linear_attack(t, self.attack_t)
			elif t <= self.attack_decay_t:
				return self.input * Envelope.linear_decay(t - self.attack_t, self.decay_t )
			elif t > self.decay_t + self.attack_t:
				return self.input * self.sustain_amp
			
		elif self.t != 0:
			if self.t < self.attack_decay_t:
				self.t = self.attack_decay_t
				return self.input * Envelope.linear_decay(self.t - self.attack_decay_t, self.release_t, MAX_AMP=self.sustain_amp)
			else:
				self.t += increment
				return self.input * Envelope.linear_decay(t - self.attack_decay_t, self.release_t, MAX_AMP=self.sustain_amp)
			
class Filter(object):
	def __init__(self, min_frequency, max_frequency):
		self.min_frequency = min_frequency
		self.max_frequency = max_frequency
		self.input = 0
	
	def step(self, buffer, buffer_length, sampleRate):
		T = 1 / sampleRate
		max_t = buffer_length * T
		t = np.arange(0,max_t,T)

		fft_values = np.fft.fft(np.array(buffer))
		freq_arr = np.fft.fftfreq(buffer_length, T)
		
		mask = self.min_frequency > freq_arr > self.max_frequency
		fft_values[np.where(mask)] = 0 + 0j

		filtered_signal = np.fft.ifft(fft_values)

		return[filtered_signal[-1]]


class Synth(object):
	def __init__(self, oscillators, envelopes, filters, sampleRate):
		self.oscillators = oscillators
		self.envelopes = envelopes
		self.filters = filters
		self.buffer = []
		self.N_fourier = 4096
		self.sampleRate = sampleRate
		self.keyPressed = False

	def step(self):
		input = 0
		for oscillator in self.oscillators:
			filter_input += oscillator.step(self.sampleRate)
		
		# Assume one filter for now.
		buffer_length = len(self.buffer)
		if buffer_length < self.N_fourier:
			envelope_input = self.filters.step(self.buffer, self.sampleRate, buffer_length)

			self.buffer = self.buffer[1,:].append(filter_input)
		else:
			self.buffer.append(filter_input)
			envelope_input  = filter_input

		self.envelopes.input = envelope_input
		output = self.envelopes.step(self.sampleRate, self.keyPressed)

		return output

		# route the oscillators to the right envelopes

		#for envelope in self.envelopes:
			#envelope.step(self.sampleRate, self.keyPressed)

		

