import MySQLdb as mysql


class AmmDB(object):
    def __init__(self):
        self.conn = mysql.connect(host='ammdb.cwwnkw8gimhn.us-west-2.rds.amazonaws.com', port=3306, user='admin',
                                  passwd='*********', db='mydb')
        self.cursor = self.conn.cursor(mysql.cursors.DictCursor)

    def conn_check(self):
        if self.conn.closed:
            self.__init__()

    @staticmethod
    def get_where_stmnt(where_query, col_name, value, operator, compare=''):

        if where_query == "":
            if compare == 'like':
                return "WHERE " + col_name + " LIKE '%" + value + "%' "
            else:
                return "WHERE " + col_name + " = '" + value + "'"
        else:
            if compare == 'like':
                return " " + operator + " " + col_name + " LIKE '%" + value + "%' "
            else:
                return " " + operator + " " + col_name + " = '" + value + "'"

    def check_email_exist(self, email):
        self.conn_check()

        self.cursor.execute("SELECT email FROM user WHERE email = '" + email + "'")
        data = self.cursor.fetchall()

        if len(data) > 0:
            return True
        else:
            return False

    def check_uname_exist(self, uname):
        self.conn_check()

        self.cursor.execute("SELECT uname FROM user WHERE uname = '" + uname + "'")
        data = self.cursor.fetchall()

        if len(data) > 0:
            return True
        else:
            return False

    def add_user(self, uname, email, passwd, fn, ln, admin=0, phone=''):
        self.conn_check()

        if self.check_uname_exist(uname):
            return 'Username exists'
        elif self.check_email_exist(email):
            return 'Email exists'

        self.cursor.execute("INSERT INTO user (uname, email, passwd, phone, fn, ln, admin) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (uname, email, passwd, phone, fn, ln, admin))
        self.conn.commit()

    def add_activity(self, name, skill, datetime, duration, numplayers, private, available, category, leader, latitude,
                     longitude):
        self.conn_check()

        self.cursor.execute("INSERT INTO activity " +
                            "(name, skill, datetime, duration, numplayers, private, available, category, leader, "
                            "latitude, longitude) " +
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (name, skill, datetime, duration, numplayers, private, available, category, leader,
                             latitude, longitude))
        self.conn.commit()

    def get_activity_type(self, activity_type_id='', name='', operator='AND'):
        self.conn_check()

        where_query = ''

        params = {
            'id': activity_type_id,
            'name': name,
        }

        for param, value in params.items():
            if value != '':
                if param == 'name':
                    where_query += self.get_where_stmnt(where_query, param, value, operator, 'like')
                else:
                    where_query += self.get_where_stmnt(where_query, param, str(value), operator)

        self.cursor.execute("SELECT * FROM activitytype " + where_query)
        data = self.cursor.fetchall()

        return data

    def get_activity(self, activity_id='', name='', skill='', duration='', numplayers='', available='', category='',
                     leader='', operator='AND'):
        self.conn_check()

        where_query = ""

        params = {
            'id': activity_id,
            'name': name,
            'skill': skill,
            'duration': duration,
            'numplayers': numplayers,
            'available': available,
            'category': category,
            'leader': leader,
        }

        for param, value in params.items():
            if value != '':
                if param == 'name':
                    where_query += self.get_where_stmnt(where_query, param, value, operator, 'like')
                else:
                    where_query += self.get_where_stmnt(where_query, param, str(value), operator)

        self.cursor.execute("SELECT * FROM activity " + where_query)
        data = self.cursor.fetchall()

        return data

    def get_user(self, user_id='', uname='', email='', phone='', fn='', ln='', operator='AND', similar=False,
                 exact=False):
        self.conn_check()

        where_query = ""

        params = {
            'id': user_id,
            'uname': uname,
            'email': email,
            'phone': phone,
            'fn': fn,
            'ln': ln,
        }

        for param, value in params.items():
            if value != '':
                if param == 'uname' and similar:
                    where_query += self.get_where_stmnt(where_query, param, value, operator, 'like')
                else:
                    where_query += self.get_where_stmnt(where_query, param, str(value), operator)

        if exact and where_query == '':
            return ''

        self.cursor.execute("SELECT * FROM user " + where_query)
        data = self.cursor.fetchall()

        return data

    def get_user_activity(self, user_id='', activity_id='', private_app='', operator='AND'):
        self.conn_check()

        where_query = ''

        params = {
            'userid': user_id,
            'activityid': activity_id,
            'private_application': private_app,
        }

        for param, value in params.items():
            if value != '':
                where_query += self.get_where_stmnt(where_query, param, str(value), operator)

        self.cursor.execute("SELECT * FROM useractivity " + where_query)
        data = self.cursor.fetchall()

        return data
