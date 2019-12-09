from flask import Flask, session, render_template, request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin , current_user , login_user, login_required
from werkzeug.urls import url_parse
import os
import string
import random

#print(__file__)


#project_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# from routes import setupRoutes
# setupRoutes(app)

app.config["SECRET_KEY"] = "somesecret"

# app.secret_key = 'somesecret'

#print(project_dir)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "hackathon.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#db.create_all()

class Users(db.Model):

    email = db.Column(db.String(40), unique=True, nullable=False, primary_key = True)
    name = db.Column(db.String(120), nullable=False)
    stdclass = db.Column(db.String(40), nullable=True)
    rollnum = db.Column(db.String(40), nullable=True)
    contact = db.Column(db.String(100), nullable=True)
    qualification = db.Column(db.String(40), nullable=True)
    role = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# db.create_all()


@app.route('/')
@app.route('/index')
def home():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect('/admin')
        if session['role'] == 'Student':
                return redirect('/Student')
        if session['role'] == 'Teacher':
            return redirect('/Teacher')

    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'role' in session:
        if session['role'] == 'admin':
            username= session['username']
            teachers = Users.query.filter_by(role='Teacher').all()
            students = Users.query.filter_by(role='Student').all()
            pageTitle="Administrator"
            return render_template('adminHome.html', teachers=teachers, students=students, username=username, pageTitle=pageTitle)
    return redirect('/adminLogin')

@app.route('/adminLogin')
def adminLogin():
    if 'role' in session:
        if session['role'] == 'admin':
            return render_template('adminHome.html')
    return render_template('adminLogin.html')

@app.route('/checkAdmin', methods=["POST"])
def checkadmin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        userFound = Users.query.filter_by(email=email, password=password).first()

        if userFound:
            session['username'] = userFound.name
            session['role'] = role
            loginMsg = "You are Welcome"
            success = True
            return render_template('loginMsg.html', name=userFound.name, loginMsg=loginMsg , success = success)

            # session['key_name'] = 'key_value'
            # return redirect(url_for('index'))
        else:
            loginMsg = "username or password is incorrect , Try Again"
            return render_template('loginMsg.html', loginMsg=loginMsg)

        return redirect('adminLogin.html')

@app.route('/Teacher')
def teacher():
    if 'role' in session:
        if session['role'] == 'Teacher':
            username= session['username']
            pageTitle="Teacher"
            return render_template('teacherHome.html', username=username, pageTitle=pageTitle)
    return redirect('/teacherLogin')

@app.route('/teacherLogin')
def teacherLogin():
    if 'role' in session:
        if session['role'] == 'Teacher':
            return render_template('teacherHome.html')
    return render_template('teacherLogin.html')

@app.route('/checkTeacher', methods=["POST"])
def checkteacher():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        userFound = Users.query.filter_by(email=email, password=password).first()

        if userFound:
            session['username'] = userFound.name
            session['role'] = userFound.role
            loginMsg = "You are Welcome"
            success = True
            return render_template('loginSuccess.html', username=userFound.name, loginMsg=loginMsg , success = success)

            # session['key_name'] = 'key_value'
            # return redirect(url_for('index'))
        else:
            loginMsg = "username or password is incorrect , Try Again"
            return render_template('loginMsg.html', loginMsg=loginMsg)

        return redirect('teacherLogin.html')

@app.route('/Student')
def student():
    if 'role' in session:
        if session['role'] == 'Student':
            username= session['username']
            pageTitle="Student"
            return render_template('studentHome.html', username=username, pageTitle=pageTitle)
    return redirect('/studentLogin')

@app.route('/studentLogin')
def studentLogin():
    if 'role' in session:
        if session['role'] == 'Student':
            return render_template('studentHome.html')
    return render_template('studentLogin.html')

@app.route('/checkStudent', methods=["POST"])
def checkstudent():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        userFound = Users.query.filter_by(email=email, password=password).first()

        if userFound:
            session['username'] = userFound.name
            session['role'] = userFound.role
            loginMsg = "You are Welcome"
            success = True
            return render_template('studentHome.html', username=userFound.name, loginMsg=loginMsg , success = success)

            # session['key_name'] = 'key_value'
            # return redirect(url_for('index'))
        else:
            loginMsg = "username or password is incorrect , Try Again"
            return render_template('loginMsg.html', loginMsg=loginMsg)

        return redirect('teacherLogin.html')




@app.route('/addTeacher')
def addteacher():
    if 'role' in session:
        if session['role'] == 'admin':
            pageTitle= "Add Teacher"
            return render_template('addTeacher.html', pageTitle=pageTitle)

    return render_template('adminLogin.html')

@app.route('/newTeacher', methods=["POST"])
def newTeacher():
    if request.method == "POST":
        user = Users()
        user.name = request.form['name']
        user.email = request.form['email']
        user.role = request.form['role']
        user.qualification = request.form['qualification']
        user.contact = request.form['contact']
        # generating random password
        upperLetters = string.ascii_uppercase
        lowerLetters = string.ascii_lowercase
        digits = string.digits
        passwordLength=10
        teacherPassword = ''.join(random.choices(upperLetters + lowerLetters + digits, k=passwordLength))
        user.password = str(teacherPassword)
        Msg = "Teacher Added"
        success = True
        db.session.add(user)
        db.session.commit()
    return render_template('addSuccess.html', Msg=Msg, success=success)

@app.route('/addStudent')
def addstudent():
    if 'role' in session:
        if session['role'] == 'admin':
            pageTitle="Add Student"
            return render_template('addStudent.html', pageTitle=pageTitle)

    return render_template('adminLogin.html')

@app.route('/newStudent', methods=["POST", "GET"])
def newstudent():
    if request.method == "POST":
        user = Users()
        user.email = request.form['email']
        user.name = request.form['name']
        user.stdclass = request.form['stdclass']
        user.rollnum = request.form['rollnum']
        user.contact = request.form['contact']
        user.role = request.form['role']
        # generating random password
        upperLetters = string.ascii_uppercase
        lowerLetters = string.ascii_lowercase
        digits = string.digits
        passwordLength=10
        stdpassword = ''.join(random.choices(upperLetters + lowerLetters + digits, k=passwordLength))
        user.password = str(stdpassword)
        Msg = "Student Added"
        db.session.add(user)
        db.session.commit()
    return render_template('addSuccess.html', Msg=Msg)

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')
#
#
# @app.route('/newSignUp', methods=["POST", "GET"])
# def newSignUp():
#     if request.method == "POST":
#         user = Users()
#         user.name = request.form['username']
#         user.password = request.form['password']
#         user.email = request.form['email']
#         user.role = request.form['role']
#         signupMsg = "user created"
#         db.session.add(user)
#         db.session.commit()
#
#     return render_template('signup.html', signupMsg=signupMsg)
#
#
@app.route('/signout')
def signout():
    # remove the username from the session if it is there
    session.pop('role', None)
    return redirect('/')

@app.route('/deleteTeacher', methods=["POST"])
def delete_teacher():
    email = request.form['target_email']
    user_found = Users.query.filter_by(email=email).first()
    db.session.delete(user_found)
    db.session.commit()

    return redirect('/admin')

@app.route('/deleteStudent', methods=["POST"])
def delete_student():
    email = request.form['target_email']
    user_found = Users.query.filter_by(email=email).first()
    db.session.delete(user_found)
    db.session.commit()

    return redirect('/admin')


@app.route('/updateTeacher', methods=["POST"])
def update_teacher():
    oldemail = request.form['target_email']

    user_found = Users.query.filter_by(email=oldemail).first()

    user_found.email = request.form['email']
    user_found.name = request.form['name']
    user_found.qualification = request.form['qualification']
    user_found.contact = request.form['contact']
    user_found.password = request.form['password']
    db.session.add(user_found)
    db.session.commit()
    return redirect('/')

@app.route('/updateStudent', methods=["POST"])
def update_student():
    oldemail = request.form['target_email']

    user_found = Users.query.filter_by(email=oldemail).first()

    user_found.email = request.form['email']
    user_found.name = request.form['name']
    user_found.stdclass = request.form['stdclass']
    user_found.rollnum = request.form['rollnum']
    user_found.contact = request.form['contact']
    user_found.password = request.form['password']
    db.session.add(user_found)
    db.session.commit()

    students = Users.query.filter_by(role='Student')

    return redirect('/')

@app.route('/viewTeachers')
def view_teachers():
    if 'role' in session:
        if session['role'] == 'admin':
            username= session['username']
            teachers = Users.query.filter_by(role='Teacher').all()
            pageTitle="Teachers"
            return render_template('viewTeachers.html', teachers=teachers, username=username, pageTitle=pageTitle)
    return redirect('/admin')

@app.route('/viewStudents')
def view_students():
    if 'role' in session:
        if session['role'] == 'admin':
            username= session['username']
            students = Users.query.filter_by(role='Student').all()
            pageTitle= "Students"
            return render_template('viewStudents.html', students=students, username=username, pageTitle=pageTitle)
    return redirect('/admin')

@app.route('/test')
def test():
    def randomString(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        a = ''.join(random.choice(letters) for i in range(stringLength))
        return a
    ab=randomString()
    return render_template('test.html', ab=ab)


app.run(port=5001, debug=True)