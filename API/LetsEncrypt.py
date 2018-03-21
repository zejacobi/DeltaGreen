from flask import Blueprint

from LetsEncryptConfig import ENDPOINT, RESPONSE

Challenge = Blueprint('challenge', __name__)


@Challenge.route(ENDPOINT, methods=['GET'])
def answer_acme_challenge():
    return RESPONSE, 200
