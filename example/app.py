from flask import Flask
from flask.ext.locale import Locale, translate

app = Flask(__name__)
app.config['DEFAULT_LOCALE'] = 'zh_CN'
Locale(app)

@app.route('/')
def hello():
	return translate('Hello')
	
if __name__ == "__main__":
	app.run(debug=True)