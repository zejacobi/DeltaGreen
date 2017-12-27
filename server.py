from sys import argv

from flask import Flask
from API.v1 import V1
from templates.Views import Views

app = Flask(__name__)

app.register_blueprint(V1, url_prefix='/api/v1')
app.register_blueprint(Views, url_prefix='')
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

host = 'localhost'

if argv and len(argv) > 1 and argv[1] == 'mobile':
    host = '0.0.0.0'

if __name__ == "__main__":
    app.run(host, port=8080, debug=False)
