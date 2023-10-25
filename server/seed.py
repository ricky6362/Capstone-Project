from app import app, db
from models import User, Asset, AssetAllocation, Request

# Initialize the Flask app
app.app_context().push()

def create_user(username, password, role):
    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()

def create_asset(asset_name, asset_category, asset_image, user_id):
    asset = Asset(asset_name=asset_name, asset_category=asset_category, asset_image=asset_image, user_id=user_id)
    db.session.add(asset)
    db.session.commit()

def create_allocation(asset_id, employee_id):
    allocation = AssetAllocation(asset_id=asset_id, employee_id=employee_id)
    db.session.add(allocation)
    db.session.commit()

def create_request(request_reason, quantity, urgency, user_id):
    request = Request(request_reason=request_reason, quantity=quantity, urgency=urgency, user_id=user_id)
    db.session.add(request)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()

        # Create 3 admin users
        for i in range(3):
            create_user(f"admin{i+1}", f"admin_password{i+1}", "Admin")

        # Create 5 procurement manager users
        for i in range(5):
            create_user(f"manager{i+1}", f"manager_password{i+1}", "Procurement Manager")

        # Create 20 employee users
        for i in range(20):
            create_user(f"employee{i+1}", f"employee_password{i+1}", "Normal Employee")

        # Example asset, allocation, and request creation
        create_asset("Laptop", "Electronics", "laptop_image.jpg", 2)  # Associate with manager (user_id=2)
        create_asset("Printer", "Office Equipment", "printer_image.jpg", 2)
        create_asset("Desk", "Furniture", "desk_image.jpg", 2)

        create_allocation(1, 3)  # Allocate Laptop to employee1
        create_allocation(2, 4)  # Allocate Printer to employee2

        create_request("New laptop for development", 1, "High", 3)  # Employee1 requests a laptop
        create_request("Printer repair", 1, "Medium", 4)  # Employee2 requests printer repair
        create_request("Desk request", 2, "Low", 3)  # Employee1 requests a desk
        create_request("Asset request", 3, "High", 2)  # Manager (employee3) requests an asset

    print("Database seeded successfully.")
