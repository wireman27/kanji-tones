#!/usr/bin/env python3

from svgpathtools import *

class KanjiVG:
	"""
	A full KanjiVG object that one can query
	to get different attributes.

	"""
	def __init__(self, svg_text):
		self.svg_text = svg_text
		self.paths = svg2paths(svg_text, is_file = False, return_svg_attributes=True)

	def get_path_list(self):
		return self.paths[0]

	def get_path_data(self):
		return self.paths[1]

	def get_path_endpoints(self):
		path_endpoints = list()
		path_list = self.get_path_list()
		for path in path_list:
			path_endpoints.append({
				"start_x":path.start.real,
				"start_y":100 - path.start.imag,
				"end_x":path.end.real,
				"end_y":100 - path.end.imag
				}
			)
		return path_endpoints

	def get_path_waypoints(self):
		waypoint_list = list()
		path_list = self.get_path_list()
		for path in path_list:
			path_waypoints = list()
			path_waypoints.append({
				"x":path.start.real,
				"y":100 - path.start.imag
				})
			for segment in path:
				path_waypoints.append({
					"x":segment.end.real,
					"y":100 - segment.end.imag
					})

			waypoint_list.append(path_waypoints)

		return waypoint_list

	def get_paths_segments(self):

		path_list = self.get_path_list()
		paths_segments = list()

		for path in path_list:
			segments = list()

			for segment in path:
				segments.append({
					"start_x":segment.start.real,
					"start_y":100 - segment.start.imag,
					"end_x": segment.end.real,
					"end_y":100 - segment.end.imag,
					"length":segment.length()
					})

			paths_segments.append(segments)

		return paths_segments






