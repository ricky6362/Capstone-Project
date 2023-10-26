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
            asset_data = Asset.query.all()
            allocation_data = AssetAllocation.query.all()
            request_data = Request.query.all()
            return jsonify({
                "username": username,
                "assets": [{"id": asset.asset_id, "asset_name": asset.asset_name, "asset_category": asset.asset_category,
                            "asset_image": asset.asset_image} for asset in asset_data],
                "allocations": [{"id": allocation.asset_allocation_id, "asset_id": allocation.asset_id, "employee_id": allocation.employee_id}
                                for allocation in allocation_data],
                "requests": [{"id": request.request_id, "request_reason": request.request_reason, "quantity": request.quantity,
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
        request_data = Request.query.filter_by(user_id=user.user_id).all()
        return jsonify({
            "username": username,
            "requests": [{"id": request.request_id, "request_reason": request.request_reason, "quantity": request.quantity,
                          "urgency": request.urgency, "user_id": request.user_id} for request in request_data]
        })
    else:
        return "Access denied. You are not logged in."

# CRUD route operation
@app.route('/assets', methods=['GET', 'POST', 'DELETE'])
def assets():
    if request.method == 'GET':
        assets = Asset.query.all()
        asset_data = [{"id": asset.asset_id, "asset_name": asset.asset_name, "asset_category": asset.asset_category,
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
    elif request.method == 'DELETE':
        asset_id = request.args.get('asset_id')
        asset = Asset.query.get(asset_id)
        if asset:
            db.session.delete(asset)
            db.session.commit()
            return "Asset deleted successfully"
        else:
            return "Asset not found"

# CRUD Operations for Asset Allocation
@app.route('/asset_allocations', methods=['GET', 'POST', 'DELETE'])
def asset_allocations():
    if request.method == 'GET':
        allocations = AssetAllocation.query.all()
        allocation_data = [{"id": allocation.asset_allocation_id, "asset_id": allocation.asset_id, "employee_id": allocation.employee_id}
                           for allocation in allocations]
        return jsonify(allocation_data)
    elif request.method == 'POST':
        asset_id = request.form['asset_id']
        employee_id = request.form['employee_id']
        allocation = AssetAllocation(asset_id=asset_id, employee_id=employee_id)
        db.session.add(allocation)
        db.session.commit()
        return "Asset allocation created successfully"
    elif request.method == 'DELETE':
        allocation_id = request.args.get('allocation_id')
        allocation = AssetAllocation.query.get(allocation_id)
        if allocation:
            db.session.delete(allocation)
            db.session.commit()
            return "Asset allocation deleted successfully"
        else:
            return "Asset allocation not found"

# CRUD Operations for Requests
@app.route('/requests', methods=['GET', 'POST', 'DELETE'])
def requests():
    if request.method == 'GET':
        all_requests = Request.query.all()
        request_data = [{"id": req.request_id, "request_reason": req.request_reason, "quantity": req.quantity,
                        "urgency": req.urgency, "user_id": req.user_id} for req in all_requests]
        return jsonify(request_data)
    elif request.method == 'POST':
        request_reason = request.form['request_reason']
        quantity = request.form['quantity']
        urgency = request.form['urgency']
        user_id = User.query.filter_by(username=session['username']).first().user_id
        new_request = Request(request_reason=request_reason, quantity=quantity, urgency=urgency, user_id=user_id)
        db.session.add(new_request)
        db.session.commit()
        return "Request created successfully"
    elif request.method == 'DELETE':
        request_id = request.args.get('request_id')
        req = Request.query.get(request_id)
        if req:
            db.session.delete(req)
            db.session.commit()
            return "Request deleted successfully"
        else:
            return "Request not found"

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run
