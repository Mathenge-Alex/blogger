import unittest
from app import db
from app.models import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username='Zander',password='zander123')

    def test_password_setter(self):
        self.assertTrue(self.new_user.password is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('zander123'))