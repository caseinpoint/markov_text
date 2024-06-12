from flask import Flask, jsonify, render_template, request
from markov import MarkovChain as MC, MarkovWord
# from os import environ


app = Flask(__name__)
# app.secret_key = environ['APP_SECRET']

# Markov chains
AUTHORS = {
	'shakespeare': MC.load('./training_data/pickle/shakespeare2.pickle'),
}


@app.route('/')
def index():
	"""Render the home page."""

	return render_template('index.html')


@app.route('/api/suggest/<author>.json', methods=['POST'])
def suggest(author):
	"""Return a list of words based on author's Markov chain."""

	author_mc = AUTHORS[author.lower()]
	key = tuple(request.json.get('key'))

	try:
		words = author_mc.get_words(key=key)
	except KeyError:
		return jsonify({'success': False, 'error': 'Key not found'})
	
	return jsonify({'success': True, 'words': words})


# @app.route('/base')
# def test():
# 	"""Render the base template as a test."""

# 	return render_template('base.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)