
import falcon
import json
from .utils import *

def validate_kanji(req, resp, resource, params):

	error_length = "A kanji should be 1 character long"
	if len(params['kanji']) != 1:
		raise falcon.HTTPBadRequest('Bad request', error_length)

	error_kanji_not_in_db = "Character not found in database"
	utf_code = r.get(params['kanji'])
	if not utf_code:
		raise falcon.HTTPBadRequest('Bad request', error_kanji_not_in_db)


class Kanji(object):

	@falcon.before(validate_kanji)
	def on_get(self, req, resp, kanji):
		resp.set_header('Access-Control-Allow-Origin', '*')
		final = create_kanji_array(kanji)
		wav_byte_array = return_wav_byte_array(final)
		resp.data = wav_byte_array
		resp.content_type = 'audio/x-wav'
		resp.status = falcon.HTTP_200