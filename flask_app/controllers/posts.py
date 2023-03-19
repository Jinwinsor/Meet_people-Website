from flask import Flask, render_template, redirect, request, session
from flask_app import app
import requests
from flask_app.models import user, post, join
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.join import Joins


# DASHBOARD == basic screen =========


@app.route('/dashboard')
def dashboard():

    if not 'user_id' in session:
        return redirect('/user')
    # Bring all posts. and for loop.
    posts = Post.get_all_posts()

    user_data = {
        'id': session['user_id']
    }
    this_user = User.getOne(user_data)
    if not this_user:
        return redirect('/user')

    like_counts = {}

    for post in posts:
        like_count = Joins.count_likes(post.id)
        like_counts[post.id] = like_count
        post.joined_users = Joins.get_users_by_post_id(post.id)
        joined_users = Joins.get_users_by_post_id(post.id)
        post.joined_user_ids = [user.id for user in joined_users]

    weather_data = session.get('weather_data', None)
    # Clear the weather data from the session
    session.pop('weather_data', None)
    return render_template('dashboard.html', like_counts=like_counts, post=post, posts=posts, user=this_user, weather_data=weather_data)


# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect('/')

#     logged_in_user = User.get_one_by_id({'id': session['user_id']})
#     posts = Post.get_all()
#     for post in posts:
#         post.joined_users = Joins.get_users_by_post_id(post.id)

#     return render_template('dashboard.html', user=logged_in_user, posts=posts)


# NEW posts ====
@app.route('/posts/create')
def posts_create():

    user_data = {
        'id': session['user_id']
    }
    this_user = User.getOne(user_data)

    return render_template('posts_create.html', user=this_user)


@app.route('/posts/create/new', methods=['POST'])
def new_posts():
    if 'title' not in request.form:
        return "Title is missing", 400

    post_data = {
        'title': request.form['title'],
        'comment': request.form['comment'],
        'location': request.form['location'],
        'date': request.form['date'],
        'user_id': session['user_id']
    }
    print(post_data)
    Post.save(post_data)

    if not Post.valiate_comment(request.form):
        return redirect('/posts/create')

    return redirect('/dashboard')


# VIEW posts ====

@app.route('/posts/view/<int:id>')
def view(id):

    if not 'user_id' in session:
        return redirect('/user')

    data = {
        'id': id
    }
    post = Post.getOne_post(data)

# ========

    user_data = {
        'id': session['user_id']
    }
    this_user = User.getOne(user_data)
    current_user = User.getOne(session['user_id'])

# =======
    # joins_data = {
    #     'id': id
    # }
    # dont_join = Joins.user_dont_like(joins_data)
    joined_users = Joins.get_users_by_post_id(id)

    return render_template('posts_view.html', joined_users=joined_users, current_user=current_user, post=post, user=this_user)


# EDIT posts ====
@app.route('/posts/update/<int:id>')
def update(id):

    data = {
        'id': id
    }

    comment = post.Post.getOne_post(data)

    # Show current user's name on NAV BAR.
    user_data = {
        "id": session['user_id']
    }
    this_user = User.getOne(user_data)

    return render_template('posts_edit.html', comment=comment, user=this_user)


@app.route('/posts/update/<int:id>/edit', methods=['POST'])
def edit(id):

    data = {
        'id': id,
        'title': request.form['title'],
        'comment': request.form['comment'],
        'location': request.form['location'],
        'date': request.form['date'],
        'user_id': session['user_id']
    }
    Post.update(data)

    if not Post.valiate_comment(request.form):
        return redirect(f'/posts/update/{id}')
    return redirect(f'/posts/update/{id}')


# DELETE posts ====
@app.route('/posts/delete/<int:id>')
def delete(id):

    data = {
        'id': id,
        'user_id': session['user_id']
    }
    Post.delete(data)
    return redirect('/dashboard')


# go to MYMEET =====
@app.route('/posts/<int:id>/mymeet')
def mymeet(id):

    user_data = {
        'id': id
    }
    user = User.getOne(user_data)

    posts = Post.get_all_posts()

    return render_template('mymeet.html', user=user, posts=posts)
