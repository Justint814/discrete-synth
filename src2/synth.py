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
	def __init__(self, attack_t, decay_t, sustain_amp, release_t, sample_rate):
		self.attack_t = attack_t
		self.decay_t = decay_t
		self.attack_decay_t = self.attack_t + self.decay_t
		self.sustain_amp = sustain_amp
		self.release_t = release_t
		self.input = 0
		self.output = 0
		self.t = 0
		self.t_prime = 0
		self.sample_rate = sample_rate
		self.increment = 1 / sample_rate
		self.release = True

	@classmethod
	def linear_attack(cls, t, attack_t, MAX_AMP=1):
		return (t * MAX_AMP)/ attack_t
	
	@classmethod
	def linear_decay(cls, dt, decay_t, MIN_AMP, MAX_AMP=1):
		return ((MIN_AMP - MAX_AMP) * dt / decay_t) + MAX_AMP
	
	@classmethod
	def exponential_attack(cls, t, attack_t, MAX_AMP=1):
		return np.float32(np.exp(t - attack_t))
	
	@classmethod
	def exponential_decay(cls, t, attack_t, MAX_AMP=1):
		return np.exp(-(t * (1/ attack_t)))

	def step(self, keyPressed, KeyPressedLast):
		t = self.t

		if keyPressed:
			self.t += self.increment
			if KeyPressedLast == False: # Override recent enveloping when a key is pressed.
				self.t = 0
			if t <= self.attack_t:
				return self.input * Envelope.linear_attack(t, self.attack_t)
			elif t <= self.attack_decay_t:
				return self.input * Envelope.linear_decay(t - self.attack_t, self.decay_t, self.sustain_amp)
			else: 
				return self.input * self.sustain_amp
			
		elif self.t != 0:
			if self.t <= self.attack_t:
				self.t += self.increment
				return self.input * Envelope.linear_attack(t, self.attack_t)
			elif self.t <= self.attack_decay_t:
				self.t += self.increment
				self.release = False
				return self.input * Envelope.linear_attack(t - self.attack_t, self.decay_t)
			elif (self.t > self.attack_decay_t) & (self.release == True):
				t_prime = self.t_prime
				if t_prime <= self.release_t:
					self.t_prime += self.increment
					return self.input * Envelope.linear_decay(t_prime, self.release_t, 0, MAX_AMP=self.sustain_amp)
				else:
					self.t_prime = 0
					self.t = 0
					self.release = True
					return 0
		else:
			self.t_prime = 0
			self.t = 0
			self.release = True
			return 0
			
class Filter(object):
	def __init__(self, min_frequency, max_frequency, sampleRate, type="bandpass", cutoff_range=10):
		if sampleRate % 2 !=0:
			raise ValueError("Sample rate must be an even integer.")
		self.min_frequency = min_frequency
		self.max_frequency = max_frequency
		self.cutoff = cutoff_range
		self.sampleRate = sampleRate
		self.buffer_length = sampleRate // 2
		self.type = type
		if self.type == "bandpass":
			self.filter = Filter.bandpass_filter(self.sampleRate, self.cutoff, self.min_frequency, self.max_frequency, self.buffer_length)
	
	@classmethod
	def bandpass_filter(cls, samplerate, c, f1, f2, bufferlength):
		period = 1 / samplerate
		half_buffer = bufferlength // 2

		freqs = np.fft.fftfreq(bufferlength, period)
		freqs_abs = freqs[0:half_buffer]

		filter = np.full_like(freqs_abs, 1)

		lower_inds = np.where(freqs_abs < (f1 + c))[0]
		upper_inds = np.where(freqs_abs > (f2 - c))[0]

		len_lower = len(lower_inds)
		len_upper = len(upper_inds)

		lower_input = np.arange(0, len_lower, 1)
		upper_input = np.arange(0, len_upper, 1)

		
		a_1 = 1.38628 / lower_input[-1]
		b_1 = -1.38628
		a_2 = -1.38628/ upper_input[-1]

		filter[lower_inds] = np.exp(a_1 * lower_input + b_1)
		filter[upper_inds] = np.exp(a_2 * upper_input)

		# Flip and append to filter to make full filter over +&- frequencies.
		filter = np.concatenate((np.array([0]), filter, np.flip(filter)))

		return filter
	
	def step(self, buffer, buffer_length):
		fft_values = np.fft.fft(buffer, buffer_length)

		if self.type == "bandpass":
			filtered_fft = fft_values * self.filter
		
		filtered_signal = np.fft.ifft(filtered_fft)[-1]
		return np.abs(filtered_signal)

class Synth(object):
	def __init__(self, oscillators, envelopes, filters, sampleRate):
		if sampleRate % 2 !=0:
			raise ValueError("Sample rate must be an even integer.")
		self.oscillators = oscillators
		self.envelopes = envelopes
		self.filters = filters
		self.buffer = []
		self.N_fourier = sampleRate // 2
		self.sampleRate = sampleRate
		self.keyPressed = False
		self.keyPressedLast = False
		self.num_oscillators = len(oscillators)

	def step(self):
		filter_input = 0
		for oscillator in self.oscillators:
			filter_input += np.float32(oscillator.step(self.sampleRate))
				
		# Normalize superposition of oscillators.
		filter_input = filter_input / self.num_oscillators
		
		# Assume one filter for now.
		buffer_length = len(self.buffer)
		
		if buffer_length > self.N_fourier:
			envelope_input = np.float32(self.filters.step(self.buffer, buffer_length))

			self.buffer = self.buffer[1:]
			self.buffer.append(filter_input)
		else:
			self.buffer.append(filter_input)
			envelope_input = np.float32(filter_input)
		

		self.envelopes.input = envelope_input
		output = np.float32(self.envelopes.step(self.keyPressed, self.keyPressedLast))

		return output

		# route the oscillators to the right envelopes

		#for envelope in self.envelopes:
			#envelope.step(self.sampleRate, self.keyPressed)

