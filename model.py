from random import SystemRandom
from flask_security import UserMixin, RoleMixin, Security
from werkzeug import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class Faculty(db.Model):
    """Base Model for the Faculty Table."""
    __tablename__ = 'faculty'
    def __init__(self, name):
        self.name = name

    faculty_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False, unique = True)

    def __repr__(self):
        return 'Faculty: %r' % self.name

class Department(db.Model):
    """Base Model for the Department Table."""
    __tablename__ = 'department'
    def __init__(self, faculty_id, name):
        self.name = name
        self.faculty_id = faculty_id

    department_id = db.Column(db.Integer, primary_key = True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable = False)
    name = db.Column(db.String(40), nullable = False, unique = True)

    def __repr__(self):
        return 'Department %r' % self.name

class Undergrad(db.Model):
    """Base Model for the research types fo undergraduate students."""
    __tablename__ = 'undergrad'
    def __init__(self, name):
        self.name = name

    u_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable = False)

    def __repr__(self):
        return 'Research Type for undergraduate students %r' % self.name

# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.roleid'))
)

class Role(db.Model, RoleMixin):
    """ Model for the creation of roles """
    __tablename__ = 'roles'
    roleid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)

    def __str__():
        return self.name

    def __hash__():
        return self.hash(name)

active = db.relationship('users')
roles = db.relationship('users')

class User(db.Model, UserMixin):
    """ Model for the users table """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    picture = db.Column(db.Text, nullable = False)
    fname = db.Column(db.String(15), nullable = False)
    lname = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(15), unique = True ,nullable = False)
    active = db.Column(db.Boolean, default=True)
    password = db.Column(db.String(120))
    faculty = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable = False)
    department = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable = False)
    description = db.Column(db.Text)
    roles = db.relationship(
            'Role',
            secondary = roles_users,
            backref = db.backref('users', lazy = 'dynamic')
            )

    def __init__(self, picture, fname, lname, email, active,\
                    password, faculty, department, description, \
                    roles):
        self.picture = picture
        self.fname = fname
        self.lname = lname
        self.email = email.lower()
        self.active = active
        self.password = self.set_password(password)
        self.faculty = faculty
        self.department = department
        self.description = description

    def set_password(self, password1):
        return generate_password_hash(password1)

    def check_password(self, password2):
        return check_password_hash(self.password, password2)



class Project(db.Model):
    """ Model for the projects table """
    __tablename__ = 'project'

    p_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    type_id = db.Column(db.Integer, db.ForeignKey('undergrad.u_id'), nullable = False)
    cv = db.Column(db.Boolean, default = True)
    cgpa = db.Column(db.Integer, default = 7)
    statement = db.Column(db.Boolean, default = False)
    other = db.Column(db.Text)
    hide = db.Column(db.Boolean, default = True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable = False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable = False)
    id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __init__(self, title, description, type_id, cv, cgpa, statement, other, useid, \
                 faculty_id, department_id):
        self.title = title
        self.description = description
        self.type_id = type_id
        self.cv = cv
        self.cgpa = cgpa
        self.statement = statement
        self.other = other
        self.id = useid
        self.faculty_id = faculty_id
        self.department_id = department_id


class Annoucements(db.Model):
    """ Tables made to welcome message on the front end"""

    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key = True)
    announce = db.Column(db.Text, nullable=False)

    def __init__(self, comment):
        self.comment = comment



# # Customized User model for SQL-Admin
# class UserAdmin(sqla.ModelView):
#
#     # Don't display the password on the list of Users
#     column_exclude_list = list = ('password',)
#
#     # Don't include the standard password field when creating or editing a User (but see below)
#     form_excluded_columns = ('password',)
#
#     # Automatically display human-readable names for the current and available Roles when creating or editing a User
#     column_auto_select_related = True
#
#     # Prevent administration of Users unless the currently logged-in user has the "admin" role
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
#     # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
#     # we want to use a password field (with the input masked) rather than a regular text field.
#     def scaffold_form(self):
#
#         # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
#         # password field from this form.
#         form_class = super(UserAdmin, self).scaffold_form()
#
#         # Add a password field, naming it "password2" and labeling it "New Password".
#         form_class.password2 = PasswordField('New Password')
#         return form_class
#
#     # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
#     # committed to the database.
#     def on_model_change(self, form, model, is_created):
#
#         # If the password field isn't blank...
#         if len(model.password2):
#
#             # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
#             # the existing password in the database will be retained.
#             model.password = utils.encrypt_password(model.password2)


# # Customized Role model for SQL-Admin
# class RoleAdmin(sqla.ModelView):
#
#     # Prevent administration of Roles unless the currently logged-in user has the "admin" role
#     def is_accessible(self):
#         return current_user.has_role('admin')
