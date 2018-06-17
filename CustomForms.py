from flask_wtf import Form
from wtforms import StringField, PasswordField, validators, IntegerField, \
                    SelectMultipleField, FileField, RadioField, \
                    TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    """ form template for creating user accounts """

    fname = StringField("First Name ", validators = [DataRequired("Please enter your first name")])
    lname = StringField("Last Name ", validators = [DataRequired("Please enter your last name")])
    email = StringField("Email ", validators = [DataRequired("Please enter your email addresss")])
    password = PasswordField("Password", validators = [DataRequired("Please enter a password")])
    c_password = PasswordField("Confirm Password", validators = [DataRequired("Please your password does not match")])
    description = TextAreaField("Description", validators = [DataRequired("Please enter a description")])
    file = FileField("Image", validators = [FileRequired(),
                                                FileAllowed(['png', 'jpeg', 'jpg'], 'Pictures only'),
                                                FileRequired('Please upload a picture')])
    submit = SubmitField('Submit')

    def validate(self):
        return super(ExtendedRegisterForm, self).validate()

class AdminRegistration(Form):
    fname = StringField("First Name ", validators = [DataRequired("Please enter your first name")])
    lname = StringField("Last Name ", validators = [DataRequired("Please enter your last name")])
    email = StringField("Email ", validators = [DataRequired("Please enter your email addresss")])
    password = PasswordField("Password", validators = [DataRequired("Please enter a password")])
    c_password = PasswordField("Confirm Password", validators = [DataRequired("Please your password does not match")])
    submit = SubmitField('Submit')


class Task(Form):
    """ form template for creating a new project """

    title = StringField("Title: ", validators = [DataRequired()])
    description = TextAreaField("Description: ", validators = [DataRequired()])
    type_id = IntegerField("Type of project: ", validators = [DataRequired()])
    submit = SubmitField('Submit')

class Search(Form):
    """ form template for searches """
    faculty = IntegerField("Faculty ")
    department = IntegerField("Department ")
    project = IntegerField("Project ")
    submit = SubmitField('Submit')

class LoginForm(Form):
    """ form template for login in """

    email = StringField("Email", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField('Submit')
