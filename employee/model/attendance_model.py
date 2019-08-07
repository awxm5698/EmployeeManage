import datetime


class AttendanceModel:

    def __init__(self):
        pass

    @staticmethod
    def get_all_application(db, user_id=None):
        sql = 'SELECT a.id, a.application_nbr, a.type, t.type_desc, a.applicant_id, ' \
              'u1.really_name as applicant_name, a.begin_date, a.end_date, a.duration_time, ' \
              'a.application_reason, a.auditor_status, s.status_desc, a.auditor_id, ' \
              'u2.really_name as application_name, ' \
              'a.create_time, a.auditor_reason, a.auditor_time ' \
              'FROM attendance_application a JOIN user u1 ON a.applicant_id = u1.id ' \
              'JOIN user u2 ON a.auditor_id = u2.id ' \
              'JOIN auditor_status s on a.auditor_status = s.status ' \
              'JOIN application_type t on a.type = t.type_id '
        if user_id is not None:
            sql = sql + 'WHERE a.applicant_id = ? or a.auditor_id = ?;'
            attendances = db.execute(sql, (user_id, user_id))
        else:
            attendances = db.execute(sql)

        return attendances

    @staticmethod
    def get_application_by_id(db, user_id, application_type):
        sql = 'SELECT a.id, a.application_nbr, a.type, t.type_desc, a.applicant_id, ' \
              'u1.really_name as applicant_name, a.begin_date, a.end_date, a.duration_time, ' \
              'a.application_reason, a.auditor_status, s.status_desc, a.auditor_id, ' \
              'u2.really_name as application_name, ' \
              'a.create_time, a.auditor_reason, a.auditor_time ' \
              'FROM attendance_application a JOIN user u1 ON a.applicant_id = u1.id ' \
              'JOIN user u2 ON a.auditor_id = u2.id ' \
              'JOIN auditor_status s on a.auditor_status = s.status ' \
              'JOIN application_type t on a.type = t.type_id ' \
              'WHERE a.applicant_id = ? and a.type = ?;'
        attendances = db.execute(sql, (user_id, application_type)).fetchall()
        return attendances

    @staticmethod
    def get_auditor_by_id(db, user_id):
        sql = 'SELECT u2.id, u2.really_name ' \
              'FROM user u1 JOIN job j ON u1.job_id = j.id ' \
              'JOIN user u2 ON j.superior_id = u2.job_id ' \
              'WHERE u1.id = ?;'
        auditor = db.execute(sql, (user_id, )).fetchall()
        return auditor

    @staticmethod
    def create_application(db, application_nbr, application_type, applicant_id, begin_date,
                           end_date, duration_time, application_reason, auditor_id):
        sql = 'INSERT INTO attendance_application ' \
              '(application_nbr, type, applicant_id, begin_date, ' \
              'end_date, duration_time, application_reason, auditor_id) values ' \
              '( ?, ?, ?, ?, ?, ?, ?, ?)'
        db.execute(sql, (application_nbr, application_type, applicant_id, begin_date,
                         end_date, duration_time, application_reason, auditor_id))
        db.commit()

    @staticmethod
    def recall_application(db, application_id):
        sql = 'Update attendance_application set auditor_status=4'\
              ' Where auditor_status = 1 and id=?'
        db.execute(sql, (application_id, ))
        db.commit()

    @staticmethod
    def auditor_application(db, application_id, status):
        auditor_reason = 'Pass' if status == 2 else 'Reject'
        auditor_time = str(datetime.datetime.now())[0:18]
        sql = 'Update attendance_application set auditor_status=?,auditor_reason=?,' \
              'auditor_time=? Where id = ? and auditor_status=1'
        db.execute(sql,(status, auditor_reason, auditor_time, application_id))
        db.commit()

    @staticmethod
    def delete_application(db, application_id):
        sql = 'Delete from attendance_application Where id=?'
        db.execute(sql, (application_id, ))
        db.commit()

    @staticmethod
    def get_application_type(db):
        sql = 'Select type_id, type_desc From application_type'
        application_types = db.execute(sql).fetchall()
        return application_types

    @staticmethod
    def default_date():
        now_hour = int(datetime.datetime.now().strftime('%H'))
        if now_hour < 9:
            begin_date = datetime.datetime.now().strftime('%Y-%m-%d 09:00:00')
            end_date = datetime.datetime.now().strftime('%Y-%m-%d 18:00:00')
            duration_time = 8
        elif now_hour < 11:
            begin_date = (datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00')
            end_date = datetime.datetime.now().strftime('%Y-%m-%d 18:00:00')
            duration_time = 18 - now_hour - 2
        elif 11 <= now_hour < 14:
            begin_date = datetime.datetime.now().strftime('%Y-%m-%d 14:00:00')
            end_date = datetime.datetime.now().strftime('%Y-%m-%d 18:00:00')
            duration_time = 4
        elif 14 <= now_hour < 17:
            begin_date = (datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00')
            end_date = datetime.datetime.now().strftime('%Y-%m-%d 18:00:00')
            duration_time = 18 - now_hour - 1
        elif 17 <= now_hour < 21:
            begin_date = (datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00')
            end_date = datetime.datetime.now().strftime('%Y-%m-%d 20:00:00')
            duration_time = 20 - now_hour - 1
        else:
            begin_date = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d 09:00:00')
            end_date = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d 18:00:00')
            duration_time = 8

        default_date = {
            "begin_date": begin_date,
            "end_date": end_date,
            "duration_time": duration_time
        }
        return default_date
