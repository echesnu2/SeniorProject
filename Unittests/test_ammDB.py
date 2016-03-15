import unittest
from amm_db import AmmDB
import MySQLdb as mysql


class TestAmmDB(unittest.TestCase):
    def test_conn_check(self):
        host = 'ammdb.cwwnkw8gimhn.us-west-2.rds.amazonaws.com'
        user = 'admin'
        passwd = 'adminadmin'
        self.conn = mysql.connect(host=host, port=3306, user=user, passwd=passwd, db='mydb')
        self.cursor = self.conn.cursor(mysql.cursors.DictCursor)
        self.failIf(self.conn.closed, self)

    def test_get_where_stmnt(self):
        db = AmmDB()
        observed = db.get_where_stmnt("", "testCol", "testVal", "", 'like')
        expected = "WHERE testCol LIKE '%testVal%' "
        self.assertEqual(observed, expected)

        observed = db.get_where_stmnt("", "testCol", "testVal", "", '')
        expected = "WHERE testCol = 'testVal'"
        self.assertEqual(observed, expected)

        observed = db.get_where_stmnt("testWhere", "testCol", "testVal", ">", 'like')
        expected = " > testCol LIKE '%testVal%' "
        self.assertEqual(observed, expected)

        observed = db.get_where_stmnt("testWhere", "testCol", "testVal", ">", '')
        expected = " > testCol = 'testVal'"
        self.assertEqual(observed, expected)

    def test_check_email_exist(self):
        db = AmmDB()
        self.assertTrue(db.check_email_exist("test@test.com"), True)

    def test_check_uname_exist(self):
        db = AmmDB()
        self.assertTrue(db.check_uname_exist("test"), True)

    def test_get_user(self):
        # Positive
        db = AmmDB()
        passwd = b'$2b$12$Z2OaKVc39OH6duIxaKFnkefKztlq7oPiYpzdNHfSwQDvBRfFjVCJ6'
        observed = db.get_user(9, 'test', 'test@test.com', '1234567890', 'test', 'test', 'AND', False)
        expected = ({'suspension': None, 'admin': 0, 'email': 'test@test.com', 'uname': 'test', 'passwd': passwd, 'id': 9, 'phone': '1234567890', 'ln': 'test', 'fn': 'test'},)
        self.assertEqual(observed, expected)

        # Negative
        observed = db.get_user('-1', 'bad', 'bad@bad.com', '-11111111', 'bad', 'bad', 'AND', False)
        expected = ()
        self.assertEqual(observed, expected)


    def test_add_user(self):
        # Positive
        db = AmmDB()
        db.add_user('test', 'test@test.com', 'test', 'test', 'test', 0, '1234567890')
        passwd = b'$2b$12$Z2OaKVc39OH6duIxaKFnkefKztlq7oPiYpzdNHfSwQDvBRfFjVCJ6'
        observed = db.get_user(9, 'test', 'test@test.com', '1234567890', 'test', 'test', 'AND', False)
        expected = ({'suspension': None, 'admin': 0, 'email': 'test@test.com', 'uname': 'test', 'passwd': passwd, 'id': 9, 'phone': '1234567890', 'ln': 'test', 'fn': 'test'},)
        self.assertEqual(observed, expected)

        # Negative
        # Add user with bad info
        # get user
        # store observed get_user out
        # store expected get_user out
        # assertnotequal observed is expected

    def test_get_activity(self):
        # Positive
        db = AmmDB()
        # observed = db.get_activity(1, 'testName', 4, 1, 3, 1, 25, 9, 'AND')
        # expected = ({'id': 1, 'name': 'testName', 'numplayers': 3, 'available': 1, 'skill': 4, 'category': 25, 'longitude': Decimal('0.0000'), 'datetime': datetime.datetime(2017, 4, 13, 18, 36, 49), 'private': 0, 'latitude': Decimal('0.0000'), 'leader': 9, 'duration': 1})
        # self.assertEqual(observed, expected)

        # Negative
        observed = db.get_activity(0, 'badName', 4, 1, 3, 1, 25, 9, 'AND')
        expected = ()
        self.assertEqual(observed, expected)

    def test_add_activity(self):
        # Positive
        # Add user
        # get user
        # store observed get_act out
        # store expected get_act out
        # assertequal observed is expected
        # Negative
        # Add user with bad info
        # get user
        # store observed get_act out
        # store expected get_act out
        # assertnotequal observed is expected
        self.fail()

    def test_get_activity_type(self):
        # positive
        db = AmmDB()
        observed = db.get_activity_type('25', 'Arts and Crafts', 'AND')
        expected = ({'id': 25, 'name': 'Arts and Crafts'},)
        self.assertEqual(observed, expected)

        # negative
        observed = db.get_activity_type('0', 'Invalid', 'AND')
        expected = ()
        self.assertEqual(observed, expected)

    def test_edit_user(self):
        # Positive
        # db = AmmDB()
        # db.edit_user()
        # observed = db.get_user()
        # expected = ()
        # self.assertEqual(observed, expected)

        # Negative
        # Add user with bad info
        # get user
        # store observed get_user out
        # store expected get_user out
        # assertnotequal observed is expected
        self.fail()

    def test_get_user_activity(self):
        # Positive
        db = AmmDB()
        #looks like we are missing private_application in the DB
        #observed = db.get_user_activity(9, 25, '', 'AND')
        #expected = ()
        #self.assertEqual(observed, expected)

        # Negative
        observed = db.get_user_activity(-1, 25, '', 'AND')
        expected = ()
        self.assertEqual(observed, expected)

if __name__ == '__main__':
    unittest.main()
