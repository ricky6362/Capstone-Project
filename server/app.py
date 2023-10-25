from flask import Flask, request, render_template, redirect, url_for, session
from models import db, User, Asset, AssetAllocation, Request

app = Flask(__name__, template_folder='templates')  # Specify the 'templates' directory

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///central_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Fixed the config key
db.init_app(app)

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
    from models import create_tables

    with app.app_context():
        create_tables()
    
    app.run(port=5555, debug=True)
