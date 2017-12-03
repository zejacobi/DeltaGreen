from flask import Flask
from API.v1 import V1

app = Flask(__name__)

app.register_blueprint(V1, url_prefix='/api/v1')


if __name__ == "__main__":
    app.run('localhost', port=8080, debug=False)
