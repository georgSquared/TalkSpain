from flask import Flask, request, send_from_directory

import os
import hashlib

import recognition as rec

app = Flask(__name__)


def md5(file_object):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file_object.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()



@app.route('/wav', methods=['POST', 'GET'])
def wav_to_text():
	if request.method=='POST':
		
		wav_file = request.files['file']

		wav_file.save('temp')

		#Check if we have already translated, based on file hash
		#Use a temp file and then destroy it
		temp_file_obj = open('temp', 'rb')
		file_hash = md5(temp_file_obj)

		#If we dont find it, created
		if not os.path.exists('./en_text_dir/' + file_hash):

			#Turn the file to text
			output_file = open(file_hash, 'w')
			rec.recognize(open('temp', 'rb'), output_file)

			#Move a saved copy to appropriate folder
			os.rename(('./' + file_hash), ('./en_text_dir/' + file_hash))
			
			#Delete the temp file
			os.remove('temp')

			return "Created"
		else:

			#Delete the temp file
			os.remove('temp')
			
			return "Already there"

	elif request.method=='GET':
		wav_file = request.files['file']

		#Check if we have already translated, based on file hash
		file_hash = md5(wav_file)

		if os.path.exists('./en_text_dir/' + file_hash):
			
			return send_from_directory('./en_text_dir/', file_hash, as_attachment=True)
		else:

			return 'Not found', 404

	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

