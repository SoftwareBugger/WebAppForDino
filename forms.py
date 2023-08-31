from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, FileField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class FieldsRequiredForm(FlaskForm):
  """Require radio fields to have content. This works around the bug that WTForms radio fields don't honor the `DataRequired` or `InputRequired` validators."""
  class Meta:
    def render_field(self, field, render_kw):
      if field.type == "_Option":
        render_kw.setdefault("required", True)
      return super().render_field(field, render_kw)
ratings = [(1, '1 Poor'), (2, '2 Fair'), (3, '3 Good'), (4, '4 Decent'), (5, '5 Excellent')]

class ReviewForm(FieldsRequiredForm):
  name = StringField("Name(Only add unreviewed in this section)",validators=[DataRequired()])
  description = TextAreaField("Description",validators=[DataRequired()])
  rating = RadioField("Rating", choices = ratings)
  # item_image
  file = FileField("image",validators=[DataRequired()])
  submit = SubmitField("submit")

class ItemReviewForm(FieldsRequiredForm):
  description = TextAreaField("Description",validators=[DataRequired()])
  rating = RadioField("Rating", choices = ratings)
  file = FileField("image(Show us another great pose!)",validators=[DataRequired()])
  submit = SubmitField("submit")
   
class BrandForm(FieldsRequiredForm):
  name = StringField("Name",validators=[DataRequired()])
  file = FileField("image",validators=[DataRequired()])
  description = TextAreaField("Description",validators=[DataRequired()])
  submit = SubmitField("submit")

# registration form
class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

# login form
class LoginForm(FlaskForm):
  email = StringField('Email',
                      validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')



  