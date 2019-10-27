#!/usr/bin/env/python3

import redis
import csv
import os
from dotenv import load_dotenv
load_dotenv()


SEIJISEIKANA_LOCATION = os.getenv('SEIJISEIKANA_LOCATION')

def main():
	r = redis.Redis()

	with open(SEIJISEIKANA_LOCATION) as f:
		kanji_reader = csv.reader(f, delimiter='\t')
		for kanji in kanji_reader:
			if len(kanji) == 10 and "U+" in kanji[7]:
				uni_code = kanji[7]
				kanji = kanji[0]
				r.set(kanji, uni_code)

if __name__ == "__main__":
	main()


