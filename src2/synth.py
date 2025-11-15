from math import *
import numpy as np

class Oscillator(object):
	def __init__(self, frequency, amplitude):
		self.frequency = frequency
		self.amplitude = amplitude
		self.t = 0
		self.output = 0

	def step(self, sampleRate):
		increment = float(1 / sampleRate)
		t = self.t
		self.t += increment
		#if self.t > pi:
		#	self.t = 0
		return np.float32(self.amplitude*np.sin(2*np.pi*self.frequency*self.t))

class Envelope(object):
	def __init__(self, attack_t, decay_t, sustain_amp, release_t):
		self.attack_t = attack_t
		self.decay_t = decay_t
		self.attack_decay_t = self.attack_t + self.decay_t
		self.sustain_amp = sustain_amp
		self.release_t = release_t
		self.input = 0
		self.output = 0
		self.t = 0
		self.t_prime = 0

	@classmethod
	def linear_attack(cls, t, attack_t, MAX_AMP=1):
		return (t * MAX_AMP)/ attack_t
	
	@classmethod
	def linear_decay(cls, dt, decay_t, MAX_AMP=1):
		return MAX_AMP - (dt * MAX_AMP)/ decay_t
	
	@classmethod
	def exponential_attack(cls, t, attack_t, MAX_AMP=1):
		return np.float32(np.exp(t - attack_t))
	
	@classmethod
	def exponential_decay(cls, t, attack_t, MAX_AMP=1):
		return np.exp(-(t * (1/ attack_t)))

	def step(self, sampleRate, keyPressed):
		increment = 1 / sampleRate
		t = self.t

		if keyPressed:
			self.t += increment
			if t <= self.attack_t:
				print('attack')
				return self.input * Envelope.linear_attack(t, self.attack_t)
			elif t <= self.attack_decay_t:
				print('decay')
				return self.input * Envelope.linear_decay(t - self.attack_t, self.decay_t)
			else: 
				print('sustain')
				return self.input * self.sustain_amp
			
		elif self.t != 0:
			if self.t <= self.attack_t:
				self.t += increment
				return self.input * Envelope.linear_attack(t, self.attack_t)
			elif self.t <= self.attack_decay_t:
				self.t += increment
				return self.input * Envelope.linear_attack(t - self.attack_t, self.decay_t)
			
			t_prime = self.t_prime
			if t_prime <= self.release_t:
				self.t_prime += increment
				print('release')
				return self.input * Envelope.linear_decay(t_prime, self.release_t, MAX_AMP=self.sustain_amp)
			else:
				print('end release')
				self.t_prime = 0
				self.t = 0
				return 0
		else:
			return 0
			
class Filter(object):
	def __init__(self, min_frequency, max_frequency, sampleRate, cutoff_range=10):
		self.min_frequency = min_frequency
		self.max_frequency = max_frequency
		self.cutoff = cutoff_range
		self.input = 0
		self.sampleRate = sampleRate
		self.buffer_length = sampleRate // 2
		self.period = 1 / sampleRate
		self.sampleRate = sampleRate
		self.index_frequency = 2  # [Hz / Index]
		self.max_t = self.buffer_length * self.period
		self.half_length = self.buffer_length // 2
		self.filter = Filter.bandpass_filter(self.sampleRate, self.cutoff, self.min_frequency, self.max_frequency)
	
	@classmethod
	def bandpass_filter(cls, samplerate, cutoff_range, low_frequency, high_frequency):
		n = int(samplerate // 2)
		period = 1 / samplerate
		max_freq = samplerate // 2

		neg_slices = slice(int((high_frequency - cutoff_range) / period),  int(n // 2), 1)#, slice(int(n - (low_frequency + cutoff_range) / period), n, 1)]
		pos_slices = [slice(0, int((high_frequency + cutoff_range) / period), 1), slice(int(n // 2), int(n - (low_frequency + cutoff_range) / period), 1)]

		neg_arr = np.arange(0, (max_freq - high_frequency - cutoff_range) / period, 1)
		pos_arr = np.arange(0, (low_frequency + cutoff_range) / period, 1)

		filter = np.full(int(n), 1)

		neg_out = np.exp(-(period/cutoff_range) * neg_arr) 
		pos_out = np.exp(pos_arr - (cutoff_range / period)) 

		filter[neg_slices] = neg_out
		filter[pos_slices[0]], filter[pos_slices[1]] = pos_out, pos_out

		return filter


	
	def step(self, buffer, buffer_length, sampleRate):
		fft_values = np.fft.fft(buffer, buffer_length)

		filtered_fft = fft_values * self.filter
		filtered_signal = np.fft.ifft(filtered_fft)

		return np.abs(filtered_signal[-1])


class Synth(object):
	def __init__(self, oscillators, envelopes, filters, sampleRate):
		self.oscillators = oscillators
		self.envelopes = envelopes
		self.filters = filters
		self.buffer = []
		self.N_fourier = sampleRate // 2
		self.sampleRate = sampleRate
		self.keyPressed = False
		self.num_oscillators = len(oscillators)

	def step(self):
		print(self.keyPressed)
		filter_input = 0
		for oscillator in self.oscillators:
			filter_input += np.float32(oscillator.step(self.sampleRate))
				
		# Normalize superposition of oscillators.
		filter_input = filter_input / self.num_oscillators
		
		# Assume one filter for now.
		buffer_length = len(self.buffer)
		
		if buffer_length > self.N_fourier:
			envelope_input = np.float32(self.filters.step(self.buffer, buffer_length, self.sampleRate))

			self.buffer = self.buffer[1:]
			self.buffer.append(filter_input)
		else:
			self.buffer.append(filter_input)
			envelope_input = np.float32(filter_input)
		

		self.envelopes.input = envelope_input
		output = np.float32(self.envelopes.step(self.sampleRate, self.keyPressed))

		return output

		# route the oscillators to the right envelopes

		#for envelope in self.envelopes:
			#envelope.step(self.sampleRate, self.keyPressed)

		

