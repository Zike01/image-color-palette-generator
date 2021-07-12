from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, URL


class ImageForm(FlaskForm):
    name = StringField('Image Name:', validators=[DataRequired()])
    img_url = StringField('Image URL:', validators=[DataRequired(), URL(message="Invalid URL")])
    num_colors = IntegerField('Number of colors', validators=[DataRequired(), NumberRange(min=1, max=25, message="Number of colors must be between 1 and 25")])
    submit = SubmitField("Add Image")


class EditForm(FlaskForm):
    name = StringField('Image Name:', validators=[DataRequired()])
    img_url = StringField('Image URL:', validators=[DataRequired(), URL(message="Invalid URL")])
    num_colors = IntegerField('Number of colors', validators=[DataRequired(), NumberRange(min=1, max=25, message="Number of colors must be between 1 and 25")])
    submit = SubmitField("Save Changes")
