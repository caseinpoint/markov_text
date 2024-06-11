from flask import Flask, render_template, session
from os import environ

app = Flask(__name__)
app.secret_key = environ.get('APP_SECRET', 'super_secret_key')

@app.route('/base')
def test():
	"""Render the base template as a test."""

	return render_template('base.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)