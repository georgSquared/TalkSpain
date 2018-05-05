from flask import Flask, request, send_file

import requests, shutil, os

app = Flask(__name__)

speech_url = 'http://speech_service/wav'
translation_url = 'http://translation_service/en_txt'

@app.route('/', methods=['POST', 'GET'])
def wav_to_es_txt():
	if request.method=='POST':
		
		wav_file = request.files['file']
		orig_filename = wav_file.filename
		wav_file.save(orig_filename)

		#Call the speech service
		files = {'file': open(orig_filename, 'rb')}
		r = requests.post(speech_url, files=files)

		if r.text=='Created' or r.text=='Already there':
			
			files = {'file': open(orig_filename, 'rb')}
			r = requests.get(speech_url, files=files)

			#Remove the wav file after we are done with recognition
			os.remove(orig_filename)

			with open(orig_filename + '.txt', 'wb') as f:
				f.write(r.text)

			#Call the translation service
			files = {'file': open(orig_filename + '.txt', 'rb')}
			r = requests.post(translation_url, files=files)

			if r.text == 'Created':
				
				file = {'file': open(orig_filename + '.txt', 'rb')}
				r = requests.get(translation_url, files=files)

				with open(orig_filename + '.txt', 'a') as f:
					f.write('\n')
					f.write('\n')
					f.write(r.text.encode('utf-8'))

				return send_file(orig_filename + '.txt')
				
			else:
				return "Translation Service Failed"

		else:
			return "Speech Service Failed"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)