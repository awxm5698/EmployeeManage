from flask import (
    Blueprint, flash, g, session, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from employee.db import get_db
from employee.model.user_model import UserModel
from employee.model.blog_model import BlogModel

bp = Blueprint('user_center', __name__)

user_model = UserModel()
blog_model = BlogModel()


@bp.route('/')
@login_required
def index():
    if session.get('job_id') == 0:
        db = get_db()
        users = user_model.get_all_user(db)
        return render_template('user_center/index.html', users=users)
    else:
        db = get_db()
        posts = blog_model.get_all_posts(db)
        return render_template('blog/index.html', posts=posts)


@bp.route('/user/create', methods=('GET', 'POST'))
@login_required
def create_user():
    db = get_db()
    jobs = user_model.get_all_job(db)
    companys = user_model.get_all_company(db)
    status = user_model.get_all_status(db)

    if request.method == 'POST':
        login_name = request.form['login_name']
        password = request.form['password']
        really_name = request.form['really_name']
        phone = request.form['phone']
        job_id = request.form['job_id']
        company_id = request.form['company_id']
        status = request.form['status']
        print(login_name, password, really_name,
              phone, job_id, company_id, status)
        login_name_existed = user_model.login_name_existed(db, login_name)

        error = None
        if login_name_existed:
            error = 'Login name is existed'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_model.create_user(db, login_name, password, really_name,
                                   phone, job_id, company_id, status)
            return redirect(url_for('user_center.index'))
    return render_template('user_center/user_create.html',
                           jobs=jobs, companys=companys, status=status)


def get_user(user_id):
    db = get_db()
    user = user_model.get_user_by_id(db, user_id)
    if user is None:
        abort(404, "Job id {0} doesn't exist.".format(id))
    return user


@bp.route('/user/<int:user_id>/update', methods=('GET', 'POST'))
@login_required
def update_user(user_id):
    user = get_user(user_id)
    db = get_db()
    jobs = user_model.get_all_job(db)
    companys = user_model.get_all_company(db)
    status = user_model.get_all_status(db)

    if request.method == 'POST':
        login_name = request.form['login_name']
        # password = request.form['password']
        really_name = request.form['really_name']
        phone = request.form['phone']
        job_id = request.form['job_id']
        company_id = request.form['company_id']
        status = request.form['status']
        error = None
        if not login_name:
            error = 'Login name can\'t be null'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_model.update_user(db, user_id, really_name,
                                   phone, job_id, company_id, status)
            return redirect(url_for('user_center.index'))

    return render_template('user_center/user_update.html', user=user,
                           jobs=jobs, companys=companys, status=status)


@bp.route('/user/<int:user_id>/delete', methods=('POST',))
@login_required
def delete_user(user_id):
    if user_id == 1:
        abort(404, "User can't be deleted.".format(user_id))
    else:
        get_user(user_id)
        db = get_db()
        user_model.delete_user(db, user_id)
    return redirect(url_for('user_center.index'))


@bp.route('/user/<int:user_id>/password', methods=('GET', 'POST'))
@login_required
def update_user_password(user_id):
    user = get_user(user_id)
    if request.method == 'POST':
        new_password = request.form['new_password']
        if g.user['job_id'] == 0:
            db = get_db()
            user_model.update_password(db, user_id, new_password)
            return redirect(url_for('user_center.index'))

        old_password = request.form['old_password']
        error = None
        db = get_db()
        check_old_psd = user_model.check_old_password(db, user_id, old_password)
        if not check_old_psd:
            error = 'Old password is error'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_model.update_password(db, user_id, new_password)
            return redirect(url_for('user_center.index'))

    return render_template('user_center/user_update_password.html', user=user)


@bp.route('/job')
def job():
    db = get_db()
    jobs = user_model.get_all_job(db)
    return render_template('user_center/job.html', jobs=jobs)


@bp.route('/job/create', methods=('GET', 'POST'))
@login_required
def create_job():
    db = get_db()
    jobs = user_model.get_all_job(db)
    if request.method == 'POST':
        job_name = request.form['name']
        superior_id = request.form['superior_id']
        job_desc = request.form['desc']
        error = None

        if not job_name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_model.create_job(db, job_name, superior_id, job_desc)
            return redirect(url_for('user_center.job'))

    return render_template('user_center/job_create.html', jobs=jobs)


def get_job(job_id):
    db = get_db()
    job = user_model.get_job_by_id(db, job_id)
    if job is None:
        abort(404, "Job id {0} doesn't exist.".format(id))
    return job


@bp.route('/job/<int:job_id>/update', methods=('GET', 'POST'))
@login_required
def update_job(job_id):
    job = get_job(job_id)
    db = get_db()
    jobs = user_model.get_all_job(db)
    if request.method == 'POST':
        job_name = request.form['name']
        superior_id = request.form['superior_id']
        job_desc = request.form['desc']
        error = None

        if not job_name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_model.update_job(db, job_id, job_name, superior_id, job_desc)
            return redirect(url_for('user_center.job'))

    return render_template('user_center/job_update.html', post=job, jobs=jobs)


@bp.route('/job/<int:job_id>/delete', methods=('POST',))
@login_required
def delete_job(job_id):
    if job_id == 0:
        abort(404, "Job id {0} can't be deleted.".format(job_id))
    else:
        get_job(job_id)
        db = get_db()
        user_model.delete_job(db, job_id)
    return redirect(url_for('user_center.job'))


@bp.route('/company')
def company():
    db = get_db()
    companys = user_model.get_all_company(db)
    return render_template('user_center/company.html', companys=companys)


@bp.route('/company/create', methods=('GET', 'POST'))
@login_required
def create_company():

    if request.method == 'POST':
        company_name = request.form['name']
        company_desc = request.form['desc']
        error = None

        if not company_name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_model.create_company(db, company_name, company_desc)
            return redirect(url_for('user_center.company'))

    return render_template('user_center/company_create.html')


def get_company(company_id):
    db = get_db()
    company = user_model.get_company_by_id(db, company_id)
    if company is None:
        abort(404, "Company id {0} doesn't exist.".format(company_id))
    return company


@bp.route('/company/<int:company_id>/update', methods=('GET', 'POST'))
@login_required
def update_company(company_id):
    company = get_company(company_id)

    if request.method == 'POST':
        company_name = request.form['name']
        company_desc = request.form['desc']
        error = None

        if not company_name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_model.update_company(db, company_id, company_name, company_desc)
            return redirect(url_for('user_center.company'))

    return render_template('user_center/company_update.html', company=company)


@bp.route('/company/<int:company_id>/delete', methods=('POST',))
@login_required
def delete_company(company_id):
    if company_id == 0:
        abort(404, "Company id {0} can't be deleted.".format(company_id))
    else:
        get_company(company_id)
        db = get_db()
        user_model.delete_company(db, company_id)
    return redirect(url_for('user_center.company'))