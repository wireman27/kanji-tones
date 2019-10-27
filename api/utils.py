#!/usr/bin/env python3

from .svg_parser import KanjiVG
from .create_signal import *
import numpy as np
import requests
import base64
import redis
import os
from lxml import etree

BASEX_URL = os.getenv('BASEX_URL')
BASEX_PORT = os.getenv('BASEX_PORT')
BASEX_USERNAME = os.getenv('BASEX_USERNAME')
BASEX_PASSWORD = os.getenv('BASEX_PASSWORD')

REDIS_URL = os.getenv('REDIS_URL')
REDIS_PORT = os.getenv('REDIS_PORT')

FREQ_HIGHEST = int(os.getenv('FREQ_HIGHEST'))
FREQ_LOWEST = int(os.getenv('FREQ_LOWEST'))

r = redis.Redis()

def construct_basex_rest(kanji_id):

	"""
	Given a kanji id, construct the url to make the GET request to
	"""

	return f"http://{BASEX_URL}:{BASEX_PORT}/rest/kanji-strokes?query=//kanji[@id='{kanji_id}']"

def get_kvg_text(kanji_id):

	"""
	Given a kanji id, return all the svg corresponding to that kanji
	"""
	url = construct_basex_rest(kanji_id)
	password = base64.b64encode(f"{BASEX_USERNAME}:{BASEX_PASSWORD}".encode('utf-8'))
	page = requests.get(url, 
						headers=
							{"Authorization":f"Basic {password.decode('utf-8')}"
						})
	kvg_text = page.content.decode('utf-8')
	return kvg_text

def kvg_to_svg(kvg_text):

	"""
	Given the raw KanjiVG XML, create
	styled SVG for the animation
	"""

	kvg_tree = etree.fromstring(kvg_text)

	for elem in kvg_tree.xpath("//*"):
		keys = elem.attrib.keys()
		for key in keys:
			if not key in ('id','d'):
				elem.attrib.pop(key)
		if elem.tag == 'path':
			elem.attrib['style'] = 'fill:none;stroke:black;stroke-width:2'

	kvg_tree.tag = 'svg'
	svg_text = etree.tostring(kvg_tree).decode('utf-8')

	svg_text = svg_text.replace('xmlns:kvg="http://kanjivg.tagaini.net"',
								'xmlns="http://www.w3.org/2000/svg"')

	svg_tree = etree.fromstring(svg_text)
  
	svg_tree.attrib["width"] = "300"
	svg_tree.attrib["height"] = "300"
	svg_tree.attrib["viewBox"]= "0 0 100 100"

	return etree.tostring(svg_tree)


def get_kanji_id(kanji):

	"""
	Given a kanji, return the corresponding kanji id that will be queried
	in the main XML database
	"""

	uni_code = r.get(kanji).decode('utf-8')
	kanji_id = "kvg:kanji_"+uni_code[2:].lower()
	return kanji_id


def coord_to_freq(coordinate):

	"""
	Given a coordinate, return frequency
	"""

	return ((FREQ_HIGHEST-FREQ_LOWEST) / 100 * coordinate) + FREQ_LOWEST


def path_to_poly_points(path_segments):

	"""
	Given a path (list of segments), return (x_points, y_points)
	"""

	x_points = list()
	y_points = list()
	
	# At t = 0
	x_points.append(0)	
	y_points.append(coord_to_freq(path_segments[0]["start_y"]))

	current_length = 0

	for segment in path_segments:
		length = segment["length"] / 100
		x_points.append(current_length + length)
		current_length = current_length + length

		y_points.append(coord_to_freq(segment["end_y"]))

	return x_points, y_points, current_length
			

def coordinates_to_frequencies(stroke_start_coord, stroke_end_coord):

	"""
	Given stroke start and end coordinates, return start and
	end frequencies
	"""

	return {
			"freq_start": ((FREQ_HIGHEST-FREQUENCY_LOWEST) / 100 * stroke_start_coord) + FREQUENCY_LOWEST,
			"freq_end": ((FREQ_HIGHEST-FREQUENCY_LOWEST) / 100 * stroke_end_coord) + FREQUENCY_LOWEST
			}

def create_kanji_array(kanji):

	"""
	Given a kanji, return the final numpy array
	"""
	kanji_id = get_kanji_id(kanji)
	kvg_text = get_kvg_text(kanji_id)
	kanji = KanjiVG(kvg_text)

	paths_segments = kanji.get_paths_segments()
	final = np.empty([0])

	for path in paths_segments:
		x_points, y_points, duration = path_to_poly_points(path)
		w = poly_sweep(x_points, y_points, duration)
		final = np.concatenate([final, w, silence(0.1)],axis=0)

	return final

	

