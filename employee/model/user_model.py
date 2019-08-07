from werkzeug.security import check_password_hash, generate_password_hash


class UserModel:

    @staticmethod
    def get_all_user(db):
        user = db.execute(
            'select w.id, w.login_name, w.really_name, w.phone, w.company_id, c.company_name,'
            ' w.job_id, j.job_name, w.status, s.status_name, w.initiation_time, w.departure_time'
            ' from user w'
            ' left join job j on w.job_id = j.id'
            ' left join user_status s on w.status = s.id'
            ' left join company c on w.company_id = c.id'
            ).fetchall()
        return user

    @staticmethod
    def login_name_existed(db, login_name):
        user = db.execute(
            'SELECT id FROM user WHERE login_name = ?', (login_name,)
            ).fetchone()
        if user is None:
            return False
        else:
            return True

    @staticmethod
    def get_user_by_id(db, user_id):
        user = db.execute(
            'select w.id, w.login_name, w.really_name, w.phone, w.company_id, c.company_name,'
            ' w.job_id, j.job_name, w.status, s.status_name, w.initiation_time, w.departure_time'
            ' from user w'
            ' left join job j on w.job_id = j.id'
            ' left join user_status s on w.status = s.id'
            ' left join company c on w.company_id = c.id'
            ' where w.id = ?', (user_id,)
        ).fetchone()
        return user

    @staticmethod
    def create_user(db, login_name, password, really_name,
                    phone, job_id, company_id, status):
        db.execute(
            'INSERT INTO user (login_name, password, really_name,'
            'phone, job_id, company_id, status)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?)',
            (login_name, generate_password_hash(password), really_name,
             phone, job_id, company_id, status)
        )
        db.commit()

    @staticmethod
    def update_user(db, user_id, really_name,
                    phone, job_id, company_id, status):
        db.execute(
            'UPDATE User SET really_name = ?,'
            ' phone = ?, job_id = ?, company_id = ?, status = ?'
            ' WHERE id = ?', (really_name,
                              phone, job_id, company_id, status,
                              user_id)
        )
        db.commit()

    @staticmethod
    def delete_user(db, user_id):
        db.execute(
            'delete from user where id=?',
            (user_id,)
        )
        db.commit()

    @staticmethod
    def check_old_password(db, user_id, old_password):
        user = db.execute('select * from user where id = ?', (user_id, )).fetchone()
        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], old_password):
            error = 'Incorrect password.'
        if error is None:
            return True
        else:
            return False

    @staticmethod
    def update_password(db, user_id, new_password):
        db.execute('Update user set password=?'
                   ' where id = ?', (generate_password_hash(new_password), user_id))
        db.commit()

    @staticmethod
    def get_all_job(db):
        job = db.execute(
            'select id, job_name, superior_id, job_desc, '
            '(select job_name from job jo where j.superior_id=jo.id) as superior_name'
            ' from job j where id >= 0'
            ' order by id'
        ).fetchall()
        return job

    @staticmethod
    def create_job(db, job_name, superior_id, job_desc):
        db.execute(
            'INSERT INTO job (job_name, superior_id, job_desc)'
            ' VALUES (?, ?, ?)',
            (job_name, superior_id, job_desc)
        )
        db.commit()

    @staticmethod
    def get_job_by_id(db, job_id):
        job = db.execute(
            'SELECT j.id, j.job_name, j.superior_id, j.job_desc,'
            ' (select jo.job_name from job jo where j.superior_id=jo.id) as superior_name'
            ' FROM job j'
            ' WHERE j.id = ?',
            (job_id,)
        ).fetchone()
        return job

    @staticmethod
    def update_job(db, job_id, job_name, superior_id, job_desc):
        db.execute(
            'UPDATE Job SET job_name = ?, superior_id = ?, job_desc = ?'
            ' WHERE id = ?',
            (job_name, superior_id, job_desc, job_id)
        )
        db.commit()

    @staticmethod
    def delete_job(db, job_id):
        db.execute('DELETE FROM job WHERE id = ?', (job_id,))
        db.commit()

    @staticmethod
    def get_all_company(db):
        company = db.execute('SELECT id,company_name,company_desc FROM company')
        return company

    @staticmethod
    def get_all_status(db):
        status = db.execute('SELECT id,status_name,status_desc FROM user_status')
        return status

    @staticmethod
    def create_company(db, company_name, company_desc):
        db.execute('insert into company (company_name,company_desc) '
                   'values(?, ?)', (company_name, company_desc)
                   )
        db.commit()

    @staticmethod
    def get_company_by_id(db, company_id):
        company = db.execute('SELECT id,company_name,company_desc FROM company'
                             ' where id = ?', (company_id,)
                             ).fetchone()
        return company

    @staticmethod
    def update_company(db, company_id, company_name, company_desc):
        db.execute(
            'UPDATE company SET company_name = ?, company_desc = ?'
            ' WHERE id = ?',
            (company_name, company_desc, company_id)
        )
        db.commit()

    @staticmethod
    def delete_company(db, company_id):
        db.execute('DELETE FROM company WHERE id = ?', (company_id,))
        db.commit()
