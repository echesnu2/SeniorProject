import unittest
from amm_db import AmmDB
import datetime
from decimal import *
import utilities
import random
from flask.ext import bcrypt

global password
password = utilities.get_key('db_pass')
print(password)


class TestAmmDB(unittest.TestCase):
    def test_conn_check(self):
        db = AmmDB(password)
        self.assertFalse(db.conn.closed, self)

    def test_get_where_stmnt(self):
        db = AmmDB(password)
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
        db = AmmDB(password)
        self.assertTrue(db.check_email_exist("test@test.com"), True)

    def test_check_uname_exist(self):
        db = AmmDB(password)
        self.assertTrue(db.check_uname_exist("test"), True)

    def test_get_user(self):
        # Positive
        db = AmmDB(password)
        passwd = b'$2b$12$Z2OaKVc39OH6duIxaKFnkefKztlq7oPiYpzdNHfSwQDvBRfFjVCJ6'
        observed = db.get_user(9, fn='test', email='test@test.com', phone='5555555555', ln='test', uname='test', operator='AND', exact=False)
        expected = ({'suspension': None, 'admin': 0, 'uname': 'test', 'passwd': passwd, 'email': 'test@test.com', 'id': 9, 'phone': '5555555555', 'fn': 'test', 'ln': 'test'},)
        self.assertEqual(observed, expected)

        # Negative
        observed = db.get_user('-1', 'bad', 'bad@bad.com', '-11111111', 'bad', 'bad', 'AND', False)
        expected = ()
        self.assertEqual(observed, expected)

    def test_add_user(self):
        # Positive
        db = AmmDB(password)
        usrname = str(random.randint(1000, 9999))
        mail = str(random.randint(1000, 9999)) + '@example.com'
        passwd = 'asdf'
        db.add_user(fn='test1', email=mail, uname=usrname, ln='test', passwd=passwd, admin=0, phone='5555555555')
        observed = db.check_uname_exist(usrname)
        self.assertTrue(observed)

        # Negative, add duplicate username, should not add
        observed = db.add_user(fn='test1', email='something@example.com', uname=usrname, ln='test', passwd=passwd, admin=0, phone='5555555555')
        expected = 'Username exists'
        self.assertTrue(observed, expected)

    def test_get_activity(self):
        # Positive
        db = AmmDB(password)
        observed = db.get_activity(1, 'testName', 4, 1, 3, 1, 25, 9, 'AND')
        expected = ({'id': 1, 'name': 'testName', 'numplayers': 3, 'available': 1, 'skill': 4, 'category': 25, 'longitude': Decimal('0.0000'), 'datetime': datetime.datetime(2017, 4, 13, 18, 36, 49), 'private': 0, 'latitude': Decimal('0.0000'), 'leader': 9, 'duration': 1},)
        self.assertEqual(observed, expected)

        # Negative
        observed = db.get_activity(0, 'badName', 4, 1, 3, 1, 25, 9, 'AND')
        expected = ()
        self.assertEqual(observed, expected)

    def test_add_activity(self):
        # Positive
        # Add user
        db = AmmDB(password)
        dur = random.randint(0, 10000)
        skil = random.randint(0,4)
        nplayers = random.randint(0, 10000)
        db.add_activity('test_activity', skil, datetime.datetime(2017, 4, 13, 18, 36, 49), dur, nplayers, 0, 1, 25, 9, Decimal('0.0000'), Decimal('0.0000'))
        observed = db.get_activity(name='test_activity', skill=skil, duration=dur, numplayers=nplayers, category=25, available=1)
        #We have no way of determining id from add activity so we cannot check this against expected
        del (observed[0])['id']
        expected = ({'available': 1, 'category': 25, 'datetime': datetime.datetime(2017, 4, 13, 18, 36, 49), 'duration': dur, 'latitude': Decimal('0.0000'), 'leader': 9, 'longitude': Decimal(0.0000), 'name': 'test_activity', 'numplayers': nplayers, 'private': 0, 'skill': skil},)
        self.assertEqual(observed, expected)
        # Negative: try to add an activity that already exists, cannot do since it will just assign a new id

    def test_get_activity_type(self):
        # positive
        db = AmmDB(password)
        observed = db.get_activity_type('25', 'Arts and Crafts', 'AND')
        expected = ({'id': 25, 'name': 'Arts and Crafts'},)
        self.assertEqual(observed, expected)

        # negative
        observed = db.get_activity_type('0', 'Invalid', 'AND')
        expected = ()
        self.assertEqual(observed, expected)

    def test_edit_user(self):
        # Positive
        db = AmmDB(password)
        passwd=b'$2b$12$Z2OaKVc39OH6duIxaKFnkefKztlq7oPiYpzdNHfSwQDvBRfFjVCJ6'
        #random.seed()
        #randomfn = random.randint(1, 100)
        #randomln = random.randint(1, 100)
        db.edit_user(9, 'test@test.com', 'test', 'test', passwd, '5555555555')
        observed = db.get_user(9, 'test', 'test@test.com', '5555555555', 'test', 'test')
        expected = ({'admin': 0,'email': 'test@test.com','fn': 'test','id': 9,'ln': 'test','passwd': b'$2b$12$Z2OaKVc39OH6duIxaKFnkefKztlq7oPiYpzdNHfSwQDvBRfFjVCJ6','phone': '5555555555','suspension': None,'uname': 'test'},)
        self.assertEqual(observed, expected)

        # Negative, trying to edit a user that does not exist
        db.edit_user(0, 'test@test.com', 'test', 'test', passwd, '5555555555')
        observed = db.get_user(0, 'test', 'test@test.com', '5555555555', 'test', 'test')
        expected = ()
        self.assertEqual(observed, expected)

    def test_get_user_activity(self):
        # Positive
        db = AmmDB(password)
        #looks like we are missing private_application in the DB
        #we're not missing private_application, it was removed from UserActivity
        #a few weeks ago because it is not needed in UserActivity because private is
        #already stored in Activity, similarly to datetime from earlier
        observed = db.get_user_activity(9, 1, 'AND')
        expected = ({'activityid': 1, 'userid' : 9},)
        self.assertEqual(observed, expected)

        # Negative
        observed = db.get_user_activity(-1, 25, 'AND')
        expected = ()
        self.assertEqual(observed, expected)

    #TODO, needs add_user_activity in ammdb
    def test_add_user_activity(self):
        pass

if __name__ == '__main__':
    unittest.main()
