from flask import Flask , render_template , redirect, url_for, request, flash
from form import RegisterForm, LoginForm, StudentForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import (login_required, login_user, UserMixin, LoginManager, login_manager, current_user, logout_user)
from flask_bcrypt import Bcrypt




app = Flask(__name__)


app.config['SECRET_KEY'] = '6ea6d8cd5b42a1fa12219bfdc5d86cd158f654b06282d1644ba4045e911a0b20'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1409@localhost/student'
db = SQLAlchemy(app)
migrate= Migrate(app, db) 
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
bcrypt = Bcrypt()




@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["POST", "GET"])
def register():

    if current_user.is_authenticated:
         return redirect(url_for('home'))

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(fname=form.fname.data, lname=form.lname.data, username=form.username.data, email=form.email.data, password=hashed_password, confirm_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account Has been created successfully for {form.username.data}","success")
        return redirect(url_for('login'))
    
    return render_template("register.html",title="Register", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
     
    form = LoginForm()
    if form.validate_on_submit():
              user = User.query.filter_by(email=form.email.data).first()
              if user and bcrypt.check_password_hash(user.password, form.password.data):
                   login_user(user, remember=form.remember.data)
                   flash("You have been logged in successfully ! ", "success")
              
                   return redirect(url_for('home'))
              else:
                   flash(f"Login unsuccessful, check your credentials please !", "danger")

    return render_template("login.html",title="Login", form=form)


@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if current_user.is_authenticated:
         
        students = current_user.Students
        return render_template("dashboard.html", title="Dashboard", students=students)
    else:
         flash(f"You need to log in first","danger")
         return redirect(url_for('login'))


@app.route("/dashboard/create", methods=["POST", "GET"])
def create():
     form = StudentForm()
     if request.method == 'POST':
          full_name = request.form['full_name']
          email = request.form['email']
          date_of_birth = request.form['date_of_birth']
          adresse = request.form['adresse']
          user_id = current_user.id
          db.session.add(student(full_name=full_name, email=email, date_of_birth=date_of_birth, adresse=adresse, user_id=user_id))
          db.session.commit()
          return redirect(url_for('dashboard'))
     return render_template("create.html", title="create", form=form)


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
      Student = student.query.get_or_404(id) 

      if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        adresse = request.form['adresse']

        Student.full_name = full_name
        Student.email = email
        Student.date_of_birth = date_of_birth
        Student.adresse = adresse
        db.session.commit()
        return redirect(url_for('dashboard', id=id))

      return render_template("edit.html", Student=Student)


@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    Student = student.query.filter_by(id=id).first()
    if request.method == 'POST':
        if Student:
            db.session.delete(Student)
            db.session.commit()
            return redirect('/dashboard')
        abort(404)
 
    return render_template('delete.html', Student=Student)


@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))


class User (db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True )
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    confirm_password = db.Column(db.String, nullable=False, unique=True)


    Students = db.relationship('student', backref='user', lazy=True)

    def __init__(self, fname, lname, username, email, password, confirm_password):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password


class student (db.Model):
    __tablename__='students'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, full_name, email, date_of_birth, adresse, user_id):
        self.full_name = full_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.adresse = adresse
        self.user_id = user_id


if __name__ == '__main__':
    app.run(debug=True)
