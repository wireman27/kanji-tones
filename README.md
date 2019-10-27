# Kanji Tones
Kanji Tones converts [kanji](https://en.wikipedia.org/wiki/Kanji) strokes to sound. 

# Data Sources

Kanji Tones is possibly largely due to the following data sources.

1. Ulrich Apel's [KanjiVG](http://kanjivg.tagaini.net/) stroke diagrams.
2. Hiroshi Moriyama's [Seijiseikana Database](https://osdn.net/projects/seijiseikana/scm/git/seijiseikana-database/commits/462a10d77733ba8a41918e9a2f359c6c4938d1e7) for UTF-8 encodings.

# Code Attributions

Manipulating SVG and sound files can get very clunky mathematically. A lot of these manipulations were made easier by the following:

1. ScipPy's [signal processing module](https://docs.scipy.org/doc/scipy/reference/signal.html) in helping generate polynomial sweeps and the binary chunks that form a WAV file.
2. Andy Port's [svgpathtools](https://github.com/mathandy/svgpathtools) in helping parse SVG files and performing all sorts of calculations on paths.

# Deploying Locally

There are two components to the application: 

1. A [Falcon](https://falcon.readthedocs.io/en/stable/#)-based API that serves up requests for WAV bytes and SVGs
2. A simple front-end that uses plain Javascript

The following steps will focus on getting the API setup. 

### Part 0 out of 2: Setting up the environment

1. Clone this repo and `cd` into it.
2. Create a virtual environment: `virtualenv -p python3.6 .venv`
3. Activate the environment: `source ./.venv/bin/activate`
4. Install Python dependencies: `pip install -r requirements.txt`

### Part 1 out of 2: Setting up the data sources
#### Seijiseikana <> Redis
1. Follow the instructions relevant to your system to get the [latest stable release of Redis](https://redis.io/download). After you make from source, you can run `make install` to access the Redis binaries from anywhere.
2. Download the `tankanji-seikana-jisx0208` file [here](https://osdn.net/projects/seijiseikana/scm/git/seijiseikana-database/blobs/462a10d77733ba8a41918e9a2f359c6c4938d1e7/dict/tankanji-seikana-jisx0208).
3. In the `.env` file, add the following entry: `SEIJISEIKANA_LOCATION = /full/path/to/seijiseikanafile`
4. Start the redis server and assign it to a process: `redis-server &`
5. Move the raw data to Redis using `python3 utils/redis_populate.py`

#### KanjiVG <> BaseX

1. Download the [latest stable version of BaseX](http://files.basex.org/releases/9.2.4/BaseX924.zip) and extract the .zip into a folder called 'basex': `unzip BaseX924.zip basex`
2. Download the [latest KanjiVG package](https://github.com/KanjiVG/kanjivg/releases/download/r20160426/kanjivg-20160426.xml.gz) and extract the XML
3. In one terminal window, run the basex server: `/path/to/basex/bin/basexserver`. 
4. In another terminal window, run this command to import the downloaded XML into the database: `/path/to/basex/bin/basexclient -V -Uadmin -Padmin -c "CREATE DB kanji-strokes /home/path/to/extracted.xml"`

### Part 2 out of 2: Starting the WSGI Server

Ensure that the virtual environment is activated and then:

1. `cd` into the root directory, i.e. the cloned repo's directory.
2. Start the Gunicorn server: `gunicorn --reload -b 0.0.0.0:8000 "app:create_app()"`

You should be all set!

### Frontend

All the front-end code sits inside the `www` folder. Use a server of your choice to server up these static files. Tweak the following variables in `www/js/script.js` based on where the Falcon API is running.

1. `const API_KANJI_SVG`: Endpoint for the SVG calls. Change host and port accordingly. No changes required if the Gunicorn server is running on localhost:8000
2. `const API_KANJI_WAV`: Endpoint for the WAV calls. Change host and port accordingly. No changes required if the Gunicorn server is running on localhost:8000

You should be all set.