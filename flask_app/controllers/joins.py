from flask_app import app
from flask import render_template, session, redirect, request, flash

from flask_app.models.post import Post
from flask_app.models import post, user, join
from flask_app.models.user import User
from flask_app.models.join import Joins
db = "meetyou"


@app.route('/join', methods=['POST'])
def join():
    post_id = request.form.get('post_id')
    user_id = session['user_id']

    join_data = {
        'id': id,
        'user_id': user_id,
        'post_id': post_id
    }

    join = Joins(join_data)
    join.save(join_data)

    return redirect('/dashboard')


@app.route('/unjoin', methods=["POST"])
def unjoin():
    post_id = request.form.get('post_id')
    user_id = session['user_id']

    join_data = {
        # 'id': id,
        'user_id': user_id,
        'post_id': post_id
    }

    Joins.leave(join_data)
    return redirect('/dashboard')
