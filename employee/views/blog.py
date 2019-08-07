from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from employee.db import get_db
from employee.model.blog_model import BlogModel

bp = Blueprint('blog', __name__)
blog_model = BlogModel()


@bp.route('/blog')
def index():
    db = get_db()
    posts = blog_model.get_all_posts(db)
    return render_template('blog/index.html', posts=posts)


@bp.route('/blog/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            blog_model.create_posts(db, g.user['id'], title, body)
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(post_id, check_author=True):
    post = blog_model.get_post_by_id(get_db(), post_id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(post_id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/blog/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            blog_model.update_post(db, post_id, title, body)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/blog/<int:id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    get_post(post_id)
    db = get_db()
    blog_model.delete_post(db, post_id)
    return redirect(url_for('blog.index'))
