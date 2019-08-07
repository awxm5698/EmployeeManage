class BlogModel:

    def __init__(self):
        pass

    @staticmethod
    def get_all_posts(db):
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, login_name'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()
        return posts

    @staticmethod
    def create_posts(db, user_id, title, body):
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            (title, body, user_id)
        )
        db.commit()

    @staticmethod
    def get_post_by_id(db, post_id):
        post = db.execute(
            'SELECT p.id, title, body, created, author_id, login_name'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?',
            (post_id,)
        ).fetchone()
        return post

    @staticmethod
    def update_post(db, post_id, title, body):
        db.execute(
            'UPDATE post SET title = ?, body = ?'
            ' WHERE id = ?',
            (title, body, post_id)
        )
        db.commit()

    @staticmethod
    def delete_post(db, post_id):
        db.execute('DELETE FROM post WHERE id = ?', (post_id,))
        db.commit()
