from flask import Blueprint, render_template, flash, request, url_for, jsonify, redirect, session
from flask_login import login_required, current_user

safety = Blueprint('safety', __name__)

@safety.route('/safety')
@login_required
def show_safety():
    return render_template("safety.html")



