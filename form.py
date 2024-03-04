from flask_wtf import FlaskForm
from wtforms import StringField , EmailField, PasswordField,SubmitField, BooleanField, DateField
from wtforms.validators import Length, DataRequired, Email, EqualTo 

class RegisterForm (FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=25)])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
     email = EmailField("Email", validators=[DataRequired(),Email()])
     password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=32)])
     remember = BooleanField("Remember Me")
     submit = SubmitField("Log in")


class StudentForm(FlaskForm):
     full_name = StringField("Full Name",  validators=[DataRequired(), Length(min=10, max=100)])
     email = EmailField("Email", validators=[DataRequired(),Email()])
     date_of_birth = DateField("Date Of Birth")
     adresse = StringField("Adresse",  validators=[DataRequired(), Length(min=10, max=100)])
     submit = SubmitField("Add Student")


