"""
API endpoints. I'm going to use versioning, so once these hit the master branch, all breaking
changes should require a new version number to be used.
"""

import Lib.Character as Character
import Lib.Generator as Generator

from flask import Blueprint, jsonify, request

from json import loads
from json.decoder import JSONDecodeError

from Lib.Utilities.Exceptions import NotFoundError, MalformedError

V1 = Blueprint('v1', __name__)


@V1.route('/characters', methods=["GET"])
def get_character():
    return jsonify({"Character": Generator.Generator().generate()})


@V1.route('/characters', methods=["POST"])
def save_character():
    character = Character.BaseCharacter()
    try:
        charset = request.charset
        character_data = loads(request.data.decode(charset))
    except (JSONDecodeError, TypeError):
        return jsonify({"Error": "Could not load JSON data", "ID": None}), 400

    try:
        character.parse_character(character_data)
        id = character.save()
        return jsonify({"ID": str(id), "Error": None})
    except NotFoundError as e:
        return jsonify({"Error": str(e), "ID": None}), 400


@V1.route('/characters/<character_id>', methods=["GET"])
def load_character(character_id):
    character = Character.BaseCharacter()
    try:
        character.load_character_from_db(character_id)
        return jsonify({"Character": character.get_character(), "Error": None})
    except (NotFoundError, MalformedError) as e:
        return jsonify({"Error": str(e), "Character": None}), int(e)
