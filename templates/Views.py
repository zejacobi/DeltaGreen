from flask import Blueprint, render_template

Views = Blueprint('views', __name__)


@Views.route('/')
def landing():
    return render_template('landing.pug')
