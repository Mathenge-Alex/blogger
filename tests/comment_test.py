from app.models import Comment, User
from app import db
import unittest

class UserTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(username = 'Blogman',password = 'blogman', email = 'apptestermind@gmail.com')
        self.new_comment = Comment(id=3,user_id=5,comment='Awesome Blog', post_id = 3 )

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()
            
    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.id,3)
        self.assertEquals(self.new_comment.user_id,5)
        self.assertEquals(self.new_comment.comment,'Amazing Post')
        self.assertEquals(self.new_comment.post_id,3)
            
    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)
            
    def test_get_comment_by_id(self):
        self.new_comment.save_comment()
        got_comments = Comment.get_comments(3)
        self.assertTrue(len(got_comments) == 1)