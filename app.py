
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

# Database
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home
@app.route('/')
def home():
    return render_template('home.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return render_template('afterlogin.html')

        return "Invalid username or password"

    return render_template('login.html')


# Logout
@app.route('/logout')
@login_required
def logout():

    logout_user()

    return render_template('afterlogout.html')


# Create database
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

