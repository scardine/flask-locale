from flask import Flask
from flask.ext.locale import Locale, translate


app = Flask(__name__)
# app.config['DEFAULT_LOCALE'] = 'zh_CN'
locale = Locale(app)


@app.route('/')
def hello():
    return translate('Hello')


@locale.localeselector
def loader():
    return 'en_US'

if __name__ == "__main__":
    app.run(debug=True)
