from math import *

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
	def __init__(self, attack, decay, sustain, release):
		self.attack = attack
		self.decay = decay
		self.sustain = sustain
		self.release = release
		self.input = 0
		self.output = 0
		self.t = 0 # In seconds.

	def step(self, sampleRate, keyPressed):
		totalLength = self.attack + self.decay + self.release
		increment = 1/sampleRate
		if keyPressed:
			if self.t <= self.attack:
				return self.input*sustain/()
			if self.attack < self.t <= self.attack + self.decay:

		else:
			pass

class Synth(object):
	def __init__(self, oscillators, envelopes, sampleRate):
		self.oscillators = oscillators
		self.envelopes = envelopes
		self.sampleRate = sampleRate
		self.keyPressed = False

	def step(self):
		for oscillator in self.oscillators:
			oscillator.step(self.sampleRate)

		# route the oscillators to the right envelopes

		for envelope in self.envelopes:
			envelope.step(self.sampleRate, self.keyPressed)

		

