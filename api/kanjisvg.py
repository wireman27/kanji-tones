
import falcon
import json
from .utils import *


def validate_kanji_svg(req, resp, resource, params):

	error_length = "A kanji should be 1 character long"
	if len(params['kanji']) != 1:
		raise falcon.HTTPBadRequest('Bad request', error_length)

	error_kanji_not_in_db = "Character not found in database"
	utf_code = r.get(params['kanji'])
	if not utf_code:
		raise falcon.HTTPBadRequest('Bad request', error_kanji_not_in_db)

class KanjiSVG(object):

	@falcon.before(validate_kanji_svg)
	def on_get(self, req, resp, kanji):
		resp.set_header('Access-Control-Allow-Origin', '*')
		uni_code = get_kanji_id(kanji)
		kvg_text = get_kvg_text(uni_code)
		resp.body = kvg_to_svg(kvg_text)
		resp.status = falcon.HTTP_200