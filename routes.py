from flask import Flask, render_template, request, \
                    jsonify, redirect, url_for, session
from flask_security import login_required, SQLAlchemyUserDatastore
from flask_security import user_registered
from flask_login import LoginManager , login_user, current_user, logout_user
from werkzeug import secure_filename
from sqlalchemy import func


from model import *
from CustomForms import *

import os
import json
import datetime

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.StagingConfig')
    app.config.from_object('config.SecurityConfig')
    # app.config.from_object('config.EmailConfig')
    db.init_app(app)
    # mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    return app

app = create_app()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def query_department():
    data = db.session.query(Department.department_id, Department.name).\
                        filter(Department.faculty_id != 1).\
                        order_by(Department.name)
    return data

def query_faculty():
    data = db.session.query(Faculty).\
                        filter(Faculty.faculty_id != 1).\
                        order_by(Faculty.name)
    return data


def query_undergrad():
    data = db.session.query(Undergrad).order_by(Undergrad.name)
    return data

@app.route("/", methods = ['GET', 'POST'])
def index():
    form = Search()
    faculty = query_faculty()
    department = query_department()
    undergrad = query_undergrad()
    if form.validate_on_submit():
        faculty1 = request.form['faculty_name']
        department1 = request.form['department_name']
        project1 = request.form['projects']
        if faculty1 != 'Faculty' and department1 == 'Department' and project1 == 'Research Positions':
            return redirect(url_for(fal, faculty_id=faculty))
        elif faculty1 == 'Faculty' and department1 != 'Department' and project1 == 'Research Positions':
            return redirect(url_for(dept, department_id=department))
        elif faculty1 == 'Faculty' and project1 != 'Research Positions' and department1 == 'Department':
            return redirect(url_for(project_type, type_id = project))
        elif faculty1 != 'Faculty' and department1 != 'Department' and project1 == 'Research Positions':
            return redirect(url_for(dept_fal, faculty_id=faculty1, department_id=department1))
        # elif faculty1 != 'Faculty' and department1 == 'Department' and project1 != 'Research Positions':
        #     return redirect(url_for(type_and_fal, faculty_id=faculty1, type_id=project1))
        elif faculty1 == 'Faculty' and department1 != 'Department'and project1 != 'Research Positions':
            return redirect(url_for(type_and_dept, department_id=department1, type_id=project1))
        elif faculty1 != 'Faculty' and department1 != 'Department' and project1 != 'Research Positions':
            return redirect(url_for(proj_fal_dept, faculty_id=faculty1, department_id=department1, type_id=project1))
        else:
            return render_template('index.html', faculty=data[0], department=data[1], undergrad=data[2], form=form)
    return render_template('index.html', faculty=faculty, department=department, undergrad=undergrad, form=form)

@login_manager.user_loader
def load_user(userid):
    try:
        return User.query.filter(User.id == userid).first()
    except NotFoundError:
        return None

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = LoginForm(request.form)
        if request.method == 'POST':
            if(request.form['email'] and request.form['password']):
                user = User.query.filter(User.email == request.form['email']).first()
                if user and user.check_password(request.form['password']):
                    login_user(user)
                    return redirect(url_for('home'))
    return redirect('/login')


@security.register_context_processor
def security_register_processor():
    return dict(faculty=query_faculty(), \
                    department=query_department())

@app.route('/signup/', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ExtendedRegisterForm(request.form)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        pwd = request.form['password']
        cpwd = request.form['c_password']
        fal = request.form['fal']
        dept = request.form['dept']
        text = request.form['description']
        if 'file' not in request.files:
            return redirect('/signup')
        file = request.files['file']
        if(not validate(fname, lname, email, file, pwd, cpwd, fal, dept, text)):
            return 'Validation'
        filename = secure_filename(file.filename)
        create_user(fname, lname, filename, email, pwd, fal, dept, text)
        user = User.query.filter(User.email == email).first()
        login_user(user)
        return redirect(url_for('home'))
    return redirect('/signup')

@app.route('/admin/register', methods = ['GET', 'POST'])
def reg_admin():
    form = AdminRegistration(request.form)
    if form.validate_on_submit():
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        if request.form['password'] == request.form['c_password']:
            pwd = request.form['password']
            create_admin(fname, lname, email, pwd)
            user = User.query.filter(User.email == email).first()
            return redirect(url_for('home'))
    return render_template('adminreg.html', form=form)


def validate(fname, lname, email, file, pwd, cpwd, fal, dept, text):
    if not fname or not lname or not pwd or not cpwd or not email or fal == 'Faculty' or dept == 'Department' or not text:
        return False
    elif pwd != cpwd:
        return False
    else:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return True
        return False
    return False


def getComments():
    data = db.session.query(Annoucements.announce).all()
    if data is None:
        return 'Polo'
    return data[0][0]


@app.route('/uri/home')
@login_required
def home():
    data = getComments()
    active = status(True)
    inactive = status(False)
    projects = user_project()
    return render_template('home.html', fname=current_user.fname, \
                                lname=current_user.lname, data=data, \
                                active=active, inactive=inactive, \
                                projects=projects   )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def create_user(fname, lname, picture, email, \
                password, faculty, department, description):
    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='end-user', description='End user')
    if not user_datastore.get_user(email):
            user_datastore.create_user(picture=picture, fname = fname, lname = lname, \
                                        email=email, password=password, faculty=faculty,
                                        department = department, description = description)
            # Commit any database changes; the User and Roles must exist before we can add a Role to the User
            db.session.commit()
            # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
            # Users already have these Roles.) Again, commit any database changes.
            user_datastore.add_role_to_user(email, 'end-user')
            db.session.commit()

def create_admin(fname, lname, email, password):
    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    if not user_datastore.get_user(email):
            user_datastore.create_user(picture='admin_avatar.svg', fname = fname, lname = lname, \
                                        email=email, password=password, faculty=1,
                                        department = 1, description = 'Administrator')
            # Commit any database changes; the User and Roles must exist before we can add a Role to the User
            db.session.commit()
            # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
            # Users already have these Roles.) Again, commit any database changes.
            user_datastore.add_role_to_user(email, 'admin')
            db.session.commit()

@app.route("/options/<department>", methods = ['GET', 'POST'])
def get_options(department):
    if department == 0:
        depmt = query_department()
    else:
        depmt = db.session.query(Department.faculty_id, Department.name).\
                    filter(Department.faculty_id == department).\
                    order_by(Department.name)
    return jsonify(json_list = depmt.all())

@app.route("/uri/new/project", methods=['GET', 'POST'])
@login_required
def create_project():
    form = Task(request.form)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        project = request.form['project']
        cv = False
        stat = False
        gpa = 7
        other = ''
        if title and description:
            if project != 'Choose Project':
                if request.form['cv']:
                    cv = True
                if request.form['stat']:
                    stat = True
                if request.form['gpa']:
                    gpa = int(request.form['gpa'])
                if request.form['other']:
                    other = request.form['other']
                project = Project(title, description, project, \
                                  cv, gpa, stat, other, current_user.id, \
                                  current_user.faculty, current_user.department)
                db.session.add(project)
                db.session.commit()
    data = query_undergrad()
    return render_template('project.html', form=form, fname=current_user.fname, \
                                            lname=current_user.lname, data=data)

def status(val):
    data = db.session.\
        query(Project.title).\
        filter(Project.hide == val and Project.id == current_user.userid)
    return data

@app.route("/uri/update/profile", methods=['GET', 'POST'])
@login_required
def profile():
    dept = db.session.query(Department.name).filter(Department.department_id == current_user.department).first()
    flt = db.session.query(Faculty.name).filter(Faculty.faculty_id == current_user.faculty).first()
    count = db.session.query(func.count(Project.p_id)).filter(Project.id == current_user.id).first()
    return render_template('profile.html', \
                           fname=current_user.fname, lname=current_user.lname, \
                           dept = dept[0], flt = flt[0], desc = current_user.description, \
                           count = count[0])

def user_project():
    data = db.session.query(Project.title, Undergrad.name, Project.description).\
                     join(Undergrad).\
                     filter(Project.type_id == Undergrad.u_id\
                            and Project.id == current_user.id)
    for i in data:
        print(i)
    return data


if __name__ == '__main__':
    app.debug = True
    app.run()
