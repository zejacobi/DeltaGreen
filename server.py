from sys import argv

from flask import Flask
from API.v1 import V1
from API.LetsEncrypt import Challenge
from templates.Views import Views

from LetsEncryptConfig import ROOT

app = Flask(__name__)

app.register_blueprint(V1, url_prefix='/api/v1')
app.register_blueprint(Challenge, url_prefix=ROOT)
app.register_blueprint(Views, url_prefix='')
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

host = 'localhost'
port = 8080

if argv and len(argv) > 1 and argv[1] == 'mobile':
    host = '0.0.0.0'

if argv and len(argv) > 1 and argv[1] == 'server':
    host = '0.0.0.0'
    port = 80

if __name__ == "__main__":
    app.run(host, port=port, debug=False)
