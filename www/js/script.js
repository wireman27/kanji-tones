

const PROTOCOL = 'http://'
const API_KANJI_SVG = 'localhost:8000/kanjisvg/'
const API_KANJI_WAV = 'localhost:8000/kanji/'

const URL_LOADING_GIF = 'gif/loading.gif';

const ERR_TOO_FEW_CHARS = '字を一つ入力してください'
const ERR_TOO_MANY_CHARS = '字を一つだけ入力してください'
const ERR_KANJI_NOT_IN_DB = 'すみませんでした。その字は見つかりませんでした。'

const KVG_HEIGHT = '30vh';
const KVG_WIDTH = '30vh';
const KVG_STROKE_WIDTH = '2';

var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
var currentState = audioCtx.state;
var source;

var play = document.querySelector('.play');
var stop = document.querySelector('.stop');
var input = document.querySelector('.input');
var svgContainer = document.querySelector('.theater');
var awakeSvg = document.querySelector('img.audiostatus.on')
var asleepSvg = document.querySelector('img.audiostatus.off')

var paths;
var nextPath;

function asyncWav(kanji) {
	return new Promise(function(resolve, reject) {
		source = audioCtx.createBufferSource();
		source.addEventListener('ended', () => {
				play.style.opacity = 1;
				play.removeAttribute("disabled")
				audioCtx.suspend()
		});
		request_wav = new XMLHttpRequest();
		request_wav.open('GET', PROTOCOL+API_KANJI_WAV+kanji, true);
		request_wav.responseType = 'arraybuffer';

		request_wav.onload = function() {
			if (request_wav.statusText === "Bad Request") {
					reject()
			} else if (request_wav.statusText === "OK") {
				var audioData = request_wav.response;
				audioCtx.decodeAudioData(audioData, function(buffer) {
						myBuffer = buffer;
						songLength = buffer.duration;
						source.buffer = myBuffer;
						source.connect(audioCtx.destination);
						resolve(true)
				},
					function(e){
						"Error with decoding audio data" + e.error
					}
				);
			}
		}

		request_wav.onerror = function() {
			reject()
		}

		request_wav.send();
	})
}

function asyncKvgSvg(kanji) {
	return new Promise(function(resolve, reject) {
		request_svg = new XMLHttpRequest();
		request_svg.open('GET', PROTOCOL+API_KANJI_SVG+kanji, true);

		request_svg.onload = function() {
			if (request_wav.statusText == "Bad Request") {
					Swal.fire(ERR_KANJI_NOT_IN_DB)
					reject()
			}
			resolve(request_svg.responseText)
		}

		request_svg.onerror = function() {
			Swal.fire(ERR_KANJI_NOT_IN_DB)
			reject()
		}
		request_svg.send()      
	})
}

function validateKanji(kanji) {
	if (kanji.length < 1) {
		Swal.fire(ERR_TOO_FEW_CHARS)
		return false
	} else if (kanji.length > 1) {
		Swal.fire(ERR_TOO_MANY_CHARS)
		return false
	}
	return true
}

function drawPath(p) {

	var length = p.getTotalLength();
	var duration = length / 100
	p.style.transition = p.style.webkitTransition = 'none';
	p.style.strokeDasharray = length + ' ' + length;
	p.style.strokeDashoffset = length;
	p.getBoundingClientRect();
	p.style.transition = p.style.webkitTransition = 'stroke-dashoffset '+duration+'s ease-in-out';
	p.style.strokeDashoffset = '0';
}

function animateKanji(paths) {
	for (var x=0; x < paths.length - 1; x++) {
		paths[x].nextPath = paths[x+1]
		paths[x].addEventListener("transitionend", function() {
			that = this
			setTimeout(function() {
				drawPath(that.nextPath)
			},100)
		})
	}
	drawPath(paths[0])
}

audioCtx.suspend();

document.onkeyup = function(event) {
	if (event.keyCode === 13) {
		event.preventDefault();
		play.click();
	}
};

play.onclick = function() {

	var kanji = input.value
	if (validateKanji(kanji) === false) {
		return
	} 

	play.style.opacity = 0.5
	play.setAttribute("disabled","disabled")
	svgContainer.innerHTML = '<img width="100" height="160" src='+URL_LOADING_GIF+'></img>'

	Promise.all([asyncWav(kanji),asyncKvgSvg(kanji)]).then(function(values) {
		svgContainer.innerHTML = values[1];
		svg = document.querySelector("svg");
		svg.style.width = KVG_WIDTH;
		svg.style.height = KVG_HEIGHT;
		svg.style.strokeWidth = KVG_STROKE_WIDTH;
		paths = document.querySelectorAll("svg path");
		animateKanji(paths)
		source.start(0);
		audioCtx.resume()
	}, function(values) {
		svgContainer.innerHTML = '';
		play.removeAttribute("disabled");
		play.style.opacity = 1;
	});
}

audioCtx.onstatechange = function() {
	if (currentState != this.state) {
		if (this.state ==  'suspended') {
				awakeSvg.style.visibility = 'hidden';
				asleepSvg.style.visibility = 'visible';
		} else {
				awakeSvg.style.visibility = 'visible';
				asleepSvg.style.visibility = 'hidden';
		}
	}
	currentState = this.state;
}






