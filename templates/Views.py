from flask import Blueprint, render_template

Views = Blueprint('views', __name__)


@Views.route('/')
def landing():
    return render_template('landing.pug')


@Views.route('/character')
def character():
    return render_template('character.pug')


@Views.route('/character/')
def character_alt():
    return render_template('character.pug')


@Views.route('/character/<char>')
def character_load(char=None):
    return render_template('character.pug')
