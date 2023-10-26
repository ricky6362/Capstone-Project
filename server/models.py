from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    assets = db.relationship('Asset', backref='user', lazy=True)
    requests = db.relationship('Request', backref='user', lazy=True)

    def authenticate(self, password):
        return self.password == password

class Asset(db.Model):
    __tablename__ = 'assets'

    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(80), nullable=False)
    asset_category = db.Column(db.String(80))
    asset_image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    allocations = db.relationship('AssetAllocation', backref='asset', lazy=True)

class AssetAllocation(db.Model):
    __tablename__ = 'asset_allocations'

    asset_allocation_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.asset_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Request(db.Model):
    __tablename__ = 'requests'

    request_id = db.Column(db.Integer, primary_key=True)
    request_reason = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

# Add this line to create the database tables
def create_tables():
    with db.app.app_context():
        db.create_all()
