from flask import Blueprint, render_template
from flask_login import login_required, current_user

view = Blueprint('view', __name__)


@view.route('/')
@login_required
def home():
    return render_template("home.html", current_user=current_user)


@view.route('/analytics', methods=['GET'])
@login_required
def analytics():
    pass


@view.route('/settings', methods=['GET'])
@login_required
def settings():
    pass


@view.route('/clips', methods=['GET'])
@login_required
def clips():
    pass


@view.route('/live', methods=['GET'])
@login_required
def video():
    pass
