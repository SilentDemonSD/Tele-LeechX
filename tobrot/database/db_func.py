from os import path as ospath, makedirs
from psycopg2 import connect, DatabaseError

from tobrot import DOWNLOAD_LOCATION, DB_URI, LOGGER, user_specific_config, PRE_DICT, CAP_DICT, IMDB_TEMPLATE

class DatabaseManager:
    def __init__(self):
        self.err = False
        self.connect()

    def connect(self):
        if DB_URI:
            try:
                self.conn = connect(DB_URI)
                self.cur = self.conn.cursor()
            except DatabaseError as error:
                LOGGER.error(f"Error in PostgreSQL DB : {error}")
                self.err = True
        else: 
            LOGGER.info(f'[DB] DATABASE_URL not Provided')
            self.err = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_init(self):
        if self.err:
            return
        sql = """CREATE TABLE IF NOT EXISTS users (
                 uid bigint,
                 vid boolean DEFAULT FALSE,
                 doc boolean DEFAULT FALSE,
                 thumb bytea DEFAULT NULL,
                 pre text ARRAY,
                 cap text DEFAULT '',
                 imdb text DEFAULT ''
              )
              """
        self.cur.execute(sql)
        self.conn.commit()
        LOGGER.info("[DB] Database Initiated")
        self.db_load()

    def db_load(self):
        # User Data
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()  # return a list ==> [(uid-0, vid-1, doc-2, thumb-3, pre-4, cap-5, imdb-6), ..]
        if rows:
            for row in rows:
                if row[2]:
                    user_specific_config[row[0]] = row[2]
                path = f"{DOWNLOAD_LOCATION}/thumbnails/{row[0]}.jpg"
                if row[3] is not None and not ospath.exists(path):
                    if not ospath.exists(f'{DOWNLOAD_LOCATION}/thumbnails'):
                        makedirs(f'{DOWNLOAD_LOCATION}/thumbnails')
                    with open(path, 'wb+') as f:
                        f.write(row[3])
                if row[4]:
                    PRE_DICT[row[0]] = row[4]
                if row[5]:
                    CAP_DICT[row[0]] = row[5]
                if row[6]:
                    IMDB_TEMPLATE[row[0]] = row[6]
            LOGGER.info("[DB] User Data has been Imported from Database")
        self.disconnect()

    def user_save_thumb(self, user_id: int, path):
        if self.err:
            return
        image = open(path, 'rb+')
        image_bin = image.read()
        if not self.user_check(user_id):
            sql = 'INSERT INTO users (thumb, uid) VALUES (%s, %s)'
        else:
            sql = 'UPDATE users SET thumb = %s WHERE uid = %s'
        self.cur.execute(sql, (image_bin, user_id))
        self.conn.commit()
        self.disconnect()

    def user_rm_thumb(self, user_id: int, path):
        if self.err:
            return
        elif self.user_check(user_id):
            sql = 'UPDATE users SET thumb = NULL WHERE uid = {}'.format(user_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()

    def user_vid(self, user_id: int):
        if self.err:
            return
        elif not self.user_check(user_id):
            sql = 'INSERT INTO users (uid, vid) VALUES ({}, TRUE)'.format(user_id)
        else:
            sql = 'UPDATE users SET vid = TRUE, doc = FALSE WHERE uid = {}'.format(user_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()

    def user_doc(self, user_id: int):
        if self.err:
            return
        elif not self.user_check(user_id):
            sql = 'INSERT INTO users (uid, doc) VALUES ({}, TRUE)'.format(user_id)
        else:
            sql = 'UPDATE users SET vid = FALSE, doc = TRUE WHERE uid = {}'.format(user_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()

    def user_pre(self, user_id: int, user_pre):
        if self.err:
            return
        elif not self.user_check(user_id):
            sql = 'INSERT INTO users (pre, uid) VALUES (%s, %s)'
        else:
            sql = 'UPDATE users SET pre = %s WHERE uid = %s'
        self.cur.execute(sql, (user_pre, user_id))
        self.conn.commit()
        self.disconnect()

    def user_cap(self, user_id: int, user_cap):
        if self.err:
            return
        elif not self.user_check(user_id):
            sql = 'INSERT INTO users (cap, uid) VALUES (%s, %s)'
        else:
            sql = 'UPDATE users SET cap = %s WHERE uid = %s'
        self.cur.execute(sql, (user_cap, user_id))
        self.conn.commit()
        self.disconnect()

    def user_imdb(self, user_id: int, user_imdb):
        if self.err:
            return
        elif not self.user_check(user_id):
            sql = 'INSERT INTO users (imdb, uid) VALUES (%s, %s)'
        else:
            sql = 'UPDATE users SET imdb = %s WHERE uid = %s'
        self.cur.execute(sql, (user_imdb, user_id))
        self.conn.commit()
        self.disconnect()

    def user_check(self, uid: int):
        self.cur.execute("SELECT * FROM users WHERE uid = {}".format(uid))
        res = self.cur.fetchone()
        return res

if DB_URI is not None:
    DatabaseManager().db_init()
