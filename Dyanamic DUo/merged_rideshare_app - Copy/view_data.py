from app import db, User, app

def view_all_users():
    print("\n=== Registered Users ===")
    print("-" * 80)
    print(f"{'ID':<5} {'Full Name':<20} {'Roll Number':<15} {'Email':<30}")
    print("-" * 80)
    
    users = User.query.all()
    for user in users:
        print(f"{user.id:<5} {user.full_name[:20]:<20} {user.roll_number:<15} {user.email:<30}")
    
    print("-" * 80)
    print(f"Total Users: {len(users)}")

if __name__ == '__main__':
    with app.app_context():
        view_all_users()
