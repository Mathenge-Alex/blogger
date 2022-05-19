from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    '''
    Class to create a wtf form for creating a pitch
    '''
    title = TextAreaField('Title')
    content = TextAreaField('Post')
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[DataRequired()])
    submit = SubmitField('Submit')
