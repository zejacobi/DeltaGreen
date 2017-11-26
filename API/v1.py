from flask import Blueprint, jsonify, request

from Lib.Character import BaseCharacter
from Lib.Generator import Generator
from Lib.Utilities.Exceptions import NotFoundError, MalformedError

V1 = Blueprint('v1', __name__)


@V1.route('/characters', methods=["GET"])
def get_character():
    return jsonify({"Character": Generator().generate()})


@V1.route('/characters', methods=["POST"])
def save_character():
    character = BaseCharacter()
    try:
        character.parse_character(request.form)
        character.save()
        return jsonify({"Success": True, "Error": None})
    except NotFoundError as e:
        return jsonify({"Error": str(e), "Success": False}), 400


@V1.route('/characters/<character_id>', methods=["GET"])
def load_character(character_id):
    character = BaseCharacter()
    try:
        character.load_character_from_db(character_id)
        return jsonify({"Character": character.get_character()})
    except (NotFoundError, MalformedError) as e:
        return jsonify({"Error": str(e), "Success": False}), int(e)
