#!/usr/bin/env python3

import numpy as np
import struct
from scipy import signal as sg
from scipy.io.wavfile import write
from scipy.interpolate import lagrange

SAMPLE_RATE = 44100
WAVE_FORMAT_PCM = 0x0001

def simple_sweep(duration, freq_start, freq_end):

	"""
	Given a duration, start frequency and end frequency,
	create a nice pitch bending 
	"""

	x = np.linspace(0, duration, (SAMPLE_RATE * duration) + 1)
	y = 80 * sg.chirp(x, f0=freq_start,f1=freq_end,t1=duration,method='linear')
	return y

def silence(duration):

	"""
	Create a numpy array of silence for a given duration
	"""

	sample_count = int(SAMPLE_RATE * duration)
	zero_array = np.zeros([sample_count],dtype=int)
	return zero_array

def poly_sweep(x_values, y_values, duration):

	"""
	Given x_values (time), y_values (frequency) and total duration of the stroke,
	generate a polynomial sweep
	"""

	poly = lagrange(x_values,y_values)
	t = np.linspace(0, duration, (SAMPLE_RATE * duration) + 1)
	w = 25000 * sg.sweep_poly(t, poly)
	return w

def save_to_wave(value_array):

	"""
	Given a numpy sound array, save to a wav file with RIFF header
	"""

	write('wav_header.wav',SAMPLE_RATE,value_array.astype(np.int16))


def return_wav_byte_array(value_array):

	"""
	Given a numpy array, return the bytes 
	that'd make it a WAV file with RIFF header
	"""

	int_array = value_array.astype(np.int16)

	header_data = b''
	header_data += b'RIFF'
	header_data += b'\x00\x00\x00\x00'
	header_data += b'WAVE'
	header_data += b'fmt '

	format_tag = WAVE_FORMAT_PCM
	channels = 1
	bit_depth = int_array.dtype.itemsize * 8
	bytes_per_second = SAMPLE_RATE*(bit_depth // 8)*channels
	block_align = channels * (bit_depth // 8)

	fmt_chunk_data = struct.pack('<HHIIHH', format_tag, channels, SAMPLE_RATE,
								 bytes_per_second, block_align, bit_depth)

	header_data += struct.pack('<I', len(fmt_chunk_data))
	header_data += fmt_chunk_data

	data_chunk = b'data'
	data_chunk += struct.pack('<I', int_array.nbytes)

	actual_data = int_array.ravel().view('b').data
	data_chunk += actual_data

	wav_bytes = header_data + data_chunk

	return wav_bytes

if __name__ == "__main__":
	x = np.array([0.2,0.5,0.8])
	y = np.array([900,400,1800])
	save_to_wave(poly_sweep(x, y))




