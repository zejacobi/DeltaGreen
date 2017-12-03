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
    """
    Generates a new character and returns the character as a JSON dictionary.

    :status 200:
        :json: Key: `"Character"`; Value: A character object, as created by the
            :meth:`Lib.Character.BaseCharacter.get_character` method.
    """
    return jsonify({"Character": Generator.Generator().generate()})


@V1.route('/characters', methods=["POST"])
def save_character():
    """
    Saves a character to the database. The returned ID can be later used to load the character.

    :jsonparameter string Class: The name of the primary class of the character.
    :jsonparameter string Package: The name of the package of skills applied to the Character
    :jsonparameter int Number_Bonds: The number of bonds the character has
    :jsonparameter dict Bonds: A dictionary mapping the character's bonds (strings giving the
        type of relationship) to their strength (and int based on the character's charisma)
    :jsonparameter list Bonds: A list of the types of bond the character has lost
    :jsonparameter string Veteran: If the character is a Damaged Veteran, a string explaining
        which type of veteran they are
    :jsonparameter list Disorders: A list of any disorders the character has
    :jsonparameter list Adapted_To: A list of any types of sanity damage the character is adapted
        to.
    :jsonparameter dict Attributes: A dictionary mapping the character's four attributes,
        `"Sanity"`, `"Hit Points"`, `"Willpower Points"`, and `"Breaking Point"` to their integer
        values.
    :jsonparameter dict Stats: A dictionary mapping the character's six primary stats to their
        integer values. Stats are: `"Strength"`, `"Dexterity"`, `"Constitution"`, `"Power"`,
        `"Intelligence"`, and `"Charisma"`
    :jsonparameter dict Skills: A dictionary mapping all of the skills the character has to their
        integer values.

    :status 200:
        :json: Key: `"ID"`; Value: the unique ID of the character, a string suitable for later
            retrieving the character object from the database.
    :status 400:
        :json: Key: `"Error"`; Value: A string describing the specific way that the request could
            not be processed
    """
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
    """
    Finds an existing character and returns them in their entirety.

    :param str character_id: The unique ID of the character. If it is not a valid ObjectID (e.g.
        not 24 characters long, or cannot otherwise be parsed by the admittedly finicky ObjectID
        class) or if it cannot be found in the database, an error will be returned.

    :status 200:
        :json: Key: `"Character"`; Value: A character object, as created by the
            :meth:`Lib.Character.BaseCharacter.get_character` method.
    :status 400:
        :json: Key: `"Error"`; Value: A string describing the specific way that the request could
            not be processed (which is most likely a problem trying to read the character_id).
    :status 404:
        :json: Key: `"Error"`; Value: A string explaining that the character could not be found.
    """
    character = Character.BaseCharacter()
    try:
        character.load_character_from_db(character_id)
        return jsonify({"Character": character.get_character(), "Error": None})
    except (NotFoundError, MalformedError) as e:
        return jsonify({"Error": str(e), "Character": None}), int(e)
