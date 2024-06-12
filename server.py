from flask import Flask, render_template
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


# @app.route('/base')
# def test():
# 	"""Render the base template as a test."""

# 	return render_template('base.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)