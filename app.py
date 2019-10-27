

from dotenv import load_dotenv
load_dotenv()

import falcon
from api.kanji import Kanji
from api.kanjisvg import KanjiSVG

def create_app():
	kanji = Kanji()
	kanjisvg = KanjiSVG()
	api = falcon.API()
	api.add_route('/kanji/{kanji}', kanji)
	api.add_route('/kanjisvg/{kanji}',kanjisvg)
	return api

