import datetime
import random
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .auth import login_required
from employee.db import get_db
from employee.model.attendance_model import AttendanceModel
from employee import config

bp = Blueprint('attendance', __name__)
attendance_model = AttendanceModel()
cfg = config


@bp.route('/attendance')
@login_required
def index():
    db = get_db()
    if g.user['job_id'] == 0:
        attendance = attendance_model.get_all_application(db)
    else:
        attendance = attendance_model.get_all_application(db, g.user['id'])
    return render_template('attendance/index.html', attendance=attendance)


@bp.route('/attendance/create', methods=('GET', 'POST'))
@login_required
def create_application():
    db = get_db()
    auditor = attendance_model.get_auditor_by_id(db, g.user['id'])
    types = attendance_model.get_application_type(db)
    default_date = attendance_model.default_date()
    if request.method == 'POST':
        application_nbr = 'L{}{}'.format(datetime.datetime.now().strftime('%Y%m%d'),
                                   random.randint(1000, 9999))
        application_type = request.form['application_type']
        begin_date = request.form['begin_date']
        end_date = request.form['end_date']
        duration_time = request.form['duration_time']
        application_reason = request.form['application_reason']
        auditor_id = request.form['auditor_id']
        if application_type == str(cfg.leave_type):
            last_application = attendance_model.get_application_by_id(db, g.user['id'], cfg.leave_type)
        else:
            last_application = attendance_model.get_application_by_id(db, g.user['id'], cfg.overtime_type)
        error = None

        r = re.compile('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
        r2 = re.compile('^\d+$')
        if not r.findall(begin_date):
            error = 'Begin Date must like: 2019-08-07 11:00:00'
        if not r.findall(end_date):
            error = 'End Date must like: 2019-08-07 11:00:00'
        if not r2.findall(str(duration_time)):
            error = 'Duration time Must be a number'
        if (datetime.datetime.strptime(begin_date, '%Y-%m-%d %H:%M:%S')
                >= datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')):
            error = 'Begin date must less than the end date'
        for application in last_application:
            if application is not None:
                last_end_date = application['end_date']
                if last_end_date >= datetime.datetime.strptime(begin_date, '%Y-%m-%d %H:%M:%S'):
                    error = 'You have an application which with a deadline on {}'.format(last_end_date)
        if error is not None:
            flash(error)
        else:
            db = get_db()
            attendance_model.create_application(db, application_nbr, application_type, g.user['id'], begin_date,
                                                end_date, duration_time, application_reason, auditor_id)
            return redirect(url_for('attendance.index'))

    return render_template('attendance/create.html',
                           auditor=auditor,
                           default_date=default_date,
                           types=types)


@bp.route('/attendance/<int:application_id>/recall', methods=('POST',))
@login_required
def recall_application(application_id):
    db = get_db()
    attendance_model.recall_application(db, application_id)
    return redirect(url_for('attendance.index'))


@bp.route('/attendance/<int:application_id>/auditor/<int:status>/', methods=('POST',))
@login_required
def auditor_application(application_id, status):
    db = get_db()
    attendance_model.auditor_application(db, application_id, status)
    return redirect(url_for('attendance.index'))


@bp.route('/attendance/<int:application_id>/delete', methods=('POST',))
@login_required
def delete_application(application_id):
    db = get_db()
    attendance_model.delete_application(db, application_id)
    return redirect(url_for('attendance.index'))
