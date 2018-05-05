import time

from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *



def recognize(wav_file, result_file):

	#This should point to wherever pocketsphinx folders are
	MODELDIR = "./pocketsphinx-5prealpha/model"
	DATADIR = "./pocketsphinx-5prealpha/test/data/"


	# Create a decoder with certain model
	config = Decoder.default_config()
	config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
	config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
	config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
	#Skip the debug info output
	config.set_string('-logfn', '/dev/null')

	# Decode streaming data.
	decoder = Decoder(config)


	decoder.start_utt()
	while True:
	    buf = wav_file.read(1024)
	    if buf:
	        decoder.process_raw(buf, False, False)
	    else:
	        break

	decoder.end_utt()

	words = []
	[words.append(seg.word) for seg in decoder.seg()]

	counter = 0

	#Send result into file
	for word in words:
		if (not word.startswith('<')) and (word != '[NOISE]'):
			result_file.write("%s " % word)
			
			#Add newlines every 10 words for readability
			counter = counter + 1
			if (counter%10 == 0):
				result_file.write('\n')



if __name__=='__main__':
	#Result file
	result_file = open('english.txt', 'w')
	wav_file = open('test.wav', 'rb')

	start = time.time()

	recognize(wav_file, result_file)


	end = time.time()

	res_time = end - start
	print "Time elapsed is: " + str(res_time)

