from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from models import db, User, Asset, AssetAllocation, Request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asset-inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# User authentication
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.authenticate(password):
        session['username'] = username
        return "Login successful"
    else:
        return "Invalid login credentials"

# Manager dashboard
@app.route('/manager_dashboard')
def manager_dashboard():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user.role == 'Procurement Manager':
            # Access manager features
            asset_data = Asset.query.all()
            allocation_data = AssetAllocation.query.all()
            request_data = Request.query.all()

            return jsonify({
                "username": username,
                "assets": [{"id": asset.id, "asset_name": asset.asset_name, "asset_category": asset.asset_category,
                            "asset_image": asset.asset_image} for asset in asset_data],
                "allocations": [{"id": allocation.id, "asset_id": allocation.asset_id, "employee_id": allocation.employee_id}
                                for allocation in allocation_data],
                "requests": [{"id": request.id, "request_reason": request.request_reason, "quantity": request.quantity,
                              "urgency": request.urgency, "user_id": request.user_id} for request in request_data]
            })
        else:
            return "Access denied. You are not a Procurement Manager."
    else:
        return "Access denied. You are not logged in."

# User dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        # Access user features
        request_data = Request.query.filter_by(user_id=user.id).all()

        return jsonify({
            "username": username,
            "requests": [{"id": request.id, "request_reason": request.request_reason, "quantity": request.quantity,
                          "urgency": request.urgency, "user_id": request.user_id} for request in request_data]
        })
    else:
        return "Access denied. You are not logged in."

# CRUD Operations for Assets
@app.route('/assets', methods=['GET', 'POST'])
def assets():
    if request.method == 'GET':
        assets = Asset.query.all()
        asset_data = [{"id": asset.id, "asset_name": asset.asset_name, "asset_category": asset.asset_category,
                       "asset_image": asset.asset_image} for asset in assets]
        return jsonify(asset_data)
    elif request.method == 'POST':
        asset_name = request.form['asset_name']
        asset_category = request.form['asset_category']
        asset_image = request.form['asset_image']

        asset = Asset(asset_name=asset_name, asset_category=asset_category, asset_image=asset_image)
        db.session.add(asset)
        db.session.commit()
        return "Asset created successfully"

# CRUD Operations for Asset Allocation
@app.route('/asset_allocations', methods=['GET', 'POST'])
def asset_allocations():
    if request.method == 'GET':
        allocations = AssetAllocation.query.all()
        allocation_data = [{"id": allocation.id, "asset_id": allocation.asset_id, "employee_id": allocation.employee_id}
                           for allocation in allocations]
        return jsonify(allocation_data)
    elif request.method == 'POST':
        asset_id = request.form['asset_id']
        employee_id = request.form['employee_id']

        allocation = AssetAllocation(asset_id=asset_id, employee_id=employee_id)
        db.session.add(allocation)
        db.session.commit()
        return "Asset allocation created successfully"

# CRUD Operations for Requests
@app.route('/requests', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':
        all_requests = Request.query.all()
        request_data = [{"id": req.id, "request_reason": req.request_reason, "quantity": req.quantity,
                        "urgency": req.urgency, "user_id": req.user_id} for req in all_requests]
        return jsonify(request_data)
    elif request.method == 'POST':
        request_reason = request.form['request_reason']
        quantity = request.form['quantity']
        urgency = request.form['urgency']
        user_id = User.query.filter_by(username=session['username']).first().id

        new_request = Request(request_reason=request_reason, quantity=quantity, urgency=urgency, user_id=user_id)
        db.session.add(new_request)
        db.session.commit()
        return "Request created successfully"

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(port=5555, debug=True)
