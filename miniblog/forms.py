from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Email
from .models import User

class RegForm(Form):
    username = StringField('Account', validators = [Length(min = 3, max = 32, message = 'Account must be between 3 and 25 characters long.')])
    nickname = StringField('Nickname', validators = [DataRequired(message = "Nickname can't be empty."),
            Length(max = 100, message = 'Nickname must be less than 100 characters.')])
    email = StringField('Email', validators = [DataRequired(message = "Email can't be empty."),
            Email(message = 'Invalid email address.')])
    password = PasswordField('Password', validators = [Length(min = 6, max = 100, message = 'Password must be between 6 and 100 characters.'), 
            EqualTo('confirm', message='Passwords does not match.' )])
    confirm = PasswordField('Confirm Password')
    signup = SubmitField('Sign up')
    
    def validate(self):
        if not Form.validate(self):
            return False
        account = self.username.data
        if User.exist(account):
            self.username.errors.append('Account already exist.')
            return False
        email = self.email.data
        if User.verify_email(email):
            self.username.errors.append('Email address already exist.')
            return False
        return True

class ProfileForm(Form):
    username = StringField('Account')
    nickname = StringField('Nickname', validators = [DataRequired(message = "Nickname can't be empty."),
            Length(max = 100, message = 'Nickname must be less than 100 characters.')])
    email = StringField('Email', validators = [DataRequired(message = "Email can't be empty."),
            Email(message = 'Invalid email address.')])
    password = PasswordField('Password', validators = [DataRequired(message = 'Please enter your password.')])
    password_new = PasswordField('New Password')
    confirm = PasswordField('Confirm Password')
    change = SubmitField('Change')

    def validate(self):
        if not Form.validate(self):
            return False
        password_new = self.password_new.data
        confirm = self.confirm.data
        if password_new or confirm:
            if len(password_new) < 6 or len(password_new) > 100 or len(confirm) < 6 or len(confirm) > 100:
                self.password_new.errors.append('New password must be between 6 and 100 characters.')
                return False
            if password_new != confirm:
                self.password_new.errors.append('New passwords does not match.')
                return False
        return True

class LoginForm(Form):
    username = StringField('Account', validators = [DataRequired(message = 'Please enter your account.')])
    password = PasswordField('Password', validators = [DataRequired(message = 'Please enter your password.')])
    remember_me = BooleanField('Remember me', default=False)
    login = SubmitField('Log in')

class PostForm(Form):
    post = StringField('Post', validators=[DataRequired()])

class ForgetForm(Form):
    email = StringField('Email', validators = [DataRequired(message = "Email can't be empty."),
            Email(message = 'Invalid email address.')])
    proceed = SubmitField('Proceed')

class ResetForm(Form):
    username = StringField('Account')
    password = PasswordField('New password', validators = [Length(min = 6, max = 100, message = 'Password must be between 6 and 100 characters.'), 
            EqualTo('confirm', message='Passwords does not match.' )])
    confirm = PasswordField('Confirm Password')
    reset = SubmitField('Reset')