from flask import Flask, request, send_file

import subprocess

app = Flask(__name__)


@app.route('/en_txt', methods=['POST', 'GET'])
def en_to_es():
	if request.method=='POST':
		
		txt_file = request.files['file']

		txt_file.save(txt_file.filename)

		subprocess.call(['apertium', 'en-es', txt_file.filename, 'spanish_' + txt_file.filename])

		return 'Created'

	elif request.method=='GET':
		
		txt_file = request.files['file']

		return send_file('spanish_' + txt_file.filename)
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)