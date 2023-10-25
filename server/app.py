from flask import Flask, request, render_template, redirect, url_for, session
from flask_migrate import Migrate # import this
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asset-inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db) # import this also

@app.route('/')
def default_route():
    return "This is the homepage."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['username'] = username
            return redirect(url_for('user_dashboard'))
        else:
            return "Invalid login credentials"

    return render_template('login.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        return "User Dashboard for: " + username
    else:
        return redirect(url_for('login'))

@app.route('/manager_dashboard')
def manager_dashboard():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user.role == 'Procurement Manager':
            return "Manager Dashboard for: " + username
        else:
            return "Access denied. You are not a Procurement Manager."
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5555, debug=True)
