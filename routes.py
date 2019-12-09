from flask import Flask, session, render_template, request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
# from app import app

def setupRoutes(app):

        @app.route('/')
        @app.route('/index')
        def home():
            if 'username' in session:
                username = session['username']
                return render_template('index.html')
                #return 'Logged in as ' + username
            #return "You are not logged in <br><a href='/login'></b>" + "click here to log in </b></a>"
            return redirect('/login')

        @app.route('/login', methods=["POST", "GET"])
        def login():
            if 'username' in session:
                username = session['username']
                return redirect('/index')

            return render_template('login.html')

        @app.route('/userLogin', methods=["POST", "GET"])
        def userlogin():
            if request.method == "POST":
                name = request.form['username']
                password = request.form['password']

                userFound = User.query.filter_by(name=name, password = password).first()

                if userFound:
                    session['username'] = request.form['username']
                    return render_template('index.html')
                    #loginMsg = "You are Welcome"
                    #success = True
                    #session['key_name'] = 'key_value'
                    #return render_template('loginMsg.html', name=userFound.name, loginMsg=loginMsg , success = success)
                    #return redirect(url_for('index'))
                else:
                    loginMsg = "username or password is incorrect , Try Again"
                    return render_template('loginMsg.html', loginMsg=loginMsg)

                return render_template('login.html')

        @app.route('/signup')
        def signup():
            return render_template('signup.html')

        @app.route('/newSignUp', methods=["POST", "GET"])
        def newSignUp():
            if request.method == "POST":
                user = User()
                user.name = request.form['username']
                user.password = request.form['password']
                user.city = request.form['city']
                signupMsg = "user created"
                db.session.add(user)
                db.session.commit()

            return render_template('signup.html', signupMsg = signupMsg)

        @app.route('/signout')
        def signout():
        # remove the username from the session if it is there
            session.pop('username', None)
            return render_template('login.html')