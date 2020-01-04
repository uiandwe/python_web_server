# -*- coding: utf-8 -*-
import os
import sys
import requests
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def get_text_md5_hash(text):
	enc = hashlib.md5()
	enc.update(text.encode('utf-8'))
	enc_text = enc.hexdigest()
	return enc_text


def test_req_index():

	with requests.Session() as s:
		req = s.get('http://localhost:65432/')

		assert req.status_code == 200
		assert req.headers == {'Accept-Charset': 'utf-8'}

		req = s.head('http://localhost:65432/')

		assert req.status_code == 200
		assert req.headers == {'Accept-Charset': 'utf-8'}


def test_req_static():
	with requests.Session() as s:
		req = s.get('http://localhost:65432/static/css/main.css')

		assert req.status_code == 200
