# First install Flask using: pip install flask
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import os
import re
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', '3797fc2e0dd53b62d4f857bec50dfbedecaa90c6e7d3165fa09bbdd8a632e1e5')  # Required for session management

# Data storage paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
RIDES_FILE = os.path.join(DATA_DIR, 'rides.json')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.json')
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Load data from files or initialize with defaults
def load_data():
    global users, rides, bookings, notifications
    
    # Load users
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = []
        save_data('users')
    
    # Load rides
    if os.path.exists(RIDES_FILE):
        with open(RIDES_FILE, 'r') as f:
            rides = json.load(f)
    else:
        rides = []
        save_data('rides')
    
    # Load bookings
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r') as f:
            bookings = json.load(f)
    else:
        bookings = []
        save_data('bookings')
    
    # Load notifications
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, 'r') as f:
            notifications = json.load(f)
    else:
        notifications = []
        save_data('notifications')

# Save data to file
def save_data(data_type):
    if data_type == 'users':
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, default=str)
    elif data_type == 'rides':
        with open(RIDES_FILE, 'w') as f:
            json.dump(rides, f, default=str)
    elif data_type == 'bookings':
        with open(BOOKINGS_FILE, 'w') as f:
            json.dump(bookings, f, default=str)
    elif data_type == 'notifications':
        with open(NOTIFICATIONS_FILE, 'w') as f:
            json.dump(notifications, f, default=str)
    elif data_type == 'all':
        save_data('users')
        save_data('rides')
        save_data('bookings')
        save_data('notifications')

# Initialize data
load_data()

# Create a dummy admin user if none exists
if not any(user.get('is_admin', False) for user in users):
    admin_user = {
        'id': 1,
        'username': 'admin',
        'password': 'admin123',
        'email': 'admin@iiti.ac.in',
        'is_admin': True,
        'full_name': 'Admin User',
        'roll_number': 'ADMIN001',
        'gender': 'male',
        'is_verified': True,
        'created_at': datetime.now().isoformat()
    }
    users.append(admin_user)
    save_data('users')

# Move HTML files to templates directory
if not os.path.exists('templates'):
    os.makedirs('templates')

# Move images to static directory
if not os.path.exists('static'):
    os.makedirs('static')

# Create uploads directory for ID card photos
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Route to serve uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Get current date and time
current_time = datetime.now()

# Format date for display
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Calculate expiration time (e.g., 30 minutes from now)
expiration_time = current_time + timedelta(minutes=30)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple validation
        if not username or not password:
            error = "Please fill in all fields"
        else:
            # Check if admin credentials match
            admin_username = os.getenv('ADMIN_USERNAME')
            admin_password = os.getenv('ADMIN_PASSWORD')
            
            if username == admin_username and password == admin_password:
                # Set session for admin
                session['logged_in'] = True
                session['username'] = admin_username
                session['user_id'] = 'admin'  # Special ID for admin
                session['is_admin'] = True
                flash('Admin login successful', 'success')
                return redirect(url_for('admin_dashboard'))
            
            # Check if user exists in your user database
            for user in users:
                if user['username'] == username and user['password'] == password:
                    # Set session
                    session['logged_in'] = True
                    session['username'] = username
                    session['user_id'] = user['id']  # Store user ID as is (integer)
                    session['is_admin'] = False
                    flash('You were successfully logged in', 'success')
                    return redirect(url_for('dashboard'))

            error = "Invalid credentials. Please try again."

    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        roll_number = request.form.get('roll_number')
        gender = request.form.get('gender')
        
        # Check if ID card photo was uploaded
        id_card_photo = request.files.get('id_card_photo')
        
        # Simple validation
        if not username or not email or not password or not confirm_password or not full_name or not roll_number or not gender:
            error = "Please fill in all fields"
        elif password != confirm_password:
            error = "Passwords do not match"
        elif not id_card_photo or id_card_photo.filename == '':
            error = "ID card photo is required"
        elif not allowed_file(id_card_photo.filename):
            error = "Invalid file format. Only PNG, JPG, JPEG, and GIF are allowed."
        else:
            # Check if username already exists
            for user in users:
                if user['username'] == username:
                    error = "Username already exists"
                    break
                if user['email'] == email:
                    error = "Email already registered"
                    break

            if not error:
                # Save ID card photo
                filename = secure_filename(f"{username}_{id_card_photo.filename}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                id_card_photo.save(file_path)
                
                # Add new user
                new_user = {
                    'id': len(users) + 1,
                    'username': username,
                    'email': email,
                    'password': password,  # In a real app, hash this password!
                    'full_name': full_name,
                    'roll_number': roll_number,
                    'gender': gender,
                    'id_card_photo': filename,  # Store just the filename
                    'is_verified': False,  # Users start as unverified
                    'created_at': datetime.now().isoformat(),  # Add creation timestamp
                    'rides': []
                }
                users.append(new_user)
                save_data('users')
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = new_user['id']
                session['is_admin'] = False
                flash('Registration successful! You can now access the dashboard.', 'success')
                return redirect(url_for('dashboard'))

    return render_template('signup.html', error=error)

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access the dashboard', 'danger')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', users=users)

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Get user information
    user_id = session.get('user_id')
    
    # Convert user_id to integer if it's a string but represents a number
    if isinstance(user_id, str) and user_id.isdigit():
        user_id = int(user_id)
    
    # Special case for admin
    if user_id == 'admin':
        # Admins are verified by default
        session['is_verified'] = True
        user = {'is_verified': True}
    else:
        user = next((u for u in users if u['id'] == user_id), None)
        
        # Pass verification status to template
        if user:
            session['is_verified'] = user.get('is_verified', False)
        else:
            # Handle the case where user is not found
            flash('User profile not found. Please try logging in again.', 'danger')
            return redirect(url_for('logout'))
    
    # Get search parameters
    from_location = request.args.get('from', '').strip()
    to_location = request.args.get('to', '').strip()
    search_date = request.args.get('date', '').strip()
    seats_needed = request.args.get('seats', '1')

    # Check if search is active
    search_active = bool(from_location or to_location or search_date)
    
    # Filter rides based on search criteria
    filtered_rides = rides
    if search_active:
        filtered_rides = [ride for ride in rides if (
            (not from_location or from_location.lower() in ride['pickup'].lower()) and
            (not to_location or to_location.lower() in ride['destination'].lower()) and
            (not search_date or search_date == ride['date']) and
            (int(seats_needed) <= ride['seats'])
        )]

    # Get unread notifications count for the current user
    unread_notifications_count = len([n for n in notifications if n['user_id'] == user_id and not n['read']])

    return render_template('Main.html', 
                         filtered_rides=filtered_rides,
                         search_active=search_active,
                         from_location=from_location,
                         to_location=to_location,
                         search_date=search_date,
                         unread_notifications_count=unread_notifications_count,
                         current_user_id=user_id,
                         is_verified=session.get('is_verified', False))

@app.route('/create-ride', methods=['GET', 'POST'])
def create_ride():
    # Get the current user ID
    user_id = session.get('user_id', 'user1')  # Replace with actual logged-in user's ID
    
    if request.method == 'POST':
        total_seats = int(request.form['total_seats'])
        available_seats = int(request.form['seats'])
        gender_preference = request.form['gender_preference']
        
        # Ensure available seats are never greater than total seats
        if available_seats > total_seats:
            available_seats = total_seats
            
        ride = {
            'id': len(rides) + 1,
            'creator_id': user_id,  # Use the current user's ID
            'pickup': request.form['pickup'],
            'destination': request.form['destination'],
            'date': request.form['date'],
            'time': request.form['time'],
            'total_seats': total_seats,
            'seats': available_seats,
            'price': float(request.form['price']),
            'phone': request.form['phone'],
            'vehicle': request.form['vehicle'],
            'gender_preference': gender_preference
        }
        rides.append(ride)
        save_data('rides')
        return redirect(url_for('home'))
    return render_template('CreateRide.html')

@app.route('/profile')
def profile():
    return render_template('Profile.html')

@app.route('/about')
def about():
    # We'll create a simple about page later
    return redirect(url_for('home'))

@app.route('/rides')
def rides_page():
    # For now, redirect to home since we don't have a separate rides page
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    # For now, redirect to home since we don't have a contact page
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/book-ride', methods=['POST'])
def book_ride():
    if request.method == 'POST':
        # Make sure user is logged in
        if not session.get('logged_in'):
            return jsonify({'status': 'error', 'message': 'You must be logged in to book a ride'})
            
        ride_id = int(request.form['ride_id'])
        user_id = session.get('user_id')
        
        # Admin cannot book rides
        if user_id == 'admin':
            return jsonify({'status': 'error', 'message': 'Admins cannot book rides'})
            
        # Convert user_id to integer if it's a string but represents a number
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)
        
        # Find the ride
        ride = next((r for r in rides if r['id'] == ride_id), None)
        if not ride:
            return jsonify({'status': 'error', 'message': 'Ride not found'})
        
        if ride['seats'] <= 0:
            return jsonify({'status': 'error', 'message': 'No seats available'})
        
        # Find the user - debug output added
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            # Return detailed error for debugging
            user_list = [f"ID: {u['id']} ({type(u['id']).__name__})" for u in users[:5]]
            return jsonify({
                'status': 'error', 
                'message': f'User not found. Your ID: {user_id} ({type(user_id).__name__})',
                'debug': f'First few users: {user_list}'
            })
        
        # Check if user is verified
        if not user.get('is_verified', False):
            return jsonify({'status': 'error', 'message': 'Your ID has not been verified by an admin yet. Please wait for verification before booking rides.'})
        
        # Check gender preference
        if ride['gender_preference'] != 'any' and user['gender'] != ride['gender_preference']:
            return jsonify({'status': 'error', 'message': f'This ride is for {ride["gender_preference"]} passengers only'})
        
        # Create booking request
        booking = {
            'id': len(bookings) + 1,
            'ride_id': ride_id,
            'user_id': user_id,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        bookings.append(booking)
        save_data('bookings')
        
        # Decrement available seats
        ride['seats'] -= 1
        
        # Ensure available seats are never negative
        if ride['seats'] < 0:
            ride['seats'] = 0
            
        # Create notification for ride creator
        notification = {
            'id': len(notifications) + 1,
            'user_id': ride['creator_id'],
            'type': 'booking_request',
            'title': 'New Ride Request',
            'message': f'A user wants to join your ride from {ride["pickup"]} to {ride["destination"]}',
            'booking_id': booking['id'],
            'created_at': datetime.now().isoformat(),
            'read': False
        }
        notifications.append(notification)
        save_data('notifications')
        
        return jsonify({'status': 'success', 'message': 'Booking request sent'})

@app.route('/view-notifications')
def view_notifications():
    user_id = session.get('user_id', 'user1')  # Replace with actual logged-in user's ID
    user_notifications = [n for n in notifications if n['user_id'] == user_id]
    
    # Get unread notifications count for the current user
    unread_notifications_count = len([n for n in notifications if n['user_id'] == user_id and not n['read']])
    
    # Mark all notifications as read
    for notification in user_notifications:
        notification['read'] = True
    save_data('notifications')
        
    return render_template('notifications.html', notifications=user_notifications, unread_notifications_count=unread_notifications_count)

@app.route('/approve-booking', methods=['POST'])
def approve_booking():
    booking_id = int(request.form['booking_id'])
    action = request.form['action']  # 'approve' or 'reject'
    
    # Find the booking
    booking = next((b for b in bookings if b['id'] == booking_id), None)
    if not booking:
        return jsonify({'status': 'error', 'message': 'Booking not found'})
    
    # Find the ride
    ride = next((r for r in rides if r['id'] == booking['ride_id']), None)
    if not ride:
        return jsonify({'status': 'error', 'message': 'Ride not found'})
    
    if action == 'approve':
        if ride['seats'] <= 0:
            return jsonify({'status': 'error', 'message': 'No seats available'})
        
        booking['status'] = 'approved'
        ride['seats'] -= 1
        
        # Notify the user that their request was approved
        notification = {
            'id': len(notifications) + 1,
            'user_id': booking['user_id'],
            'type': 'booking_approved',
            'title': 'Ride Request Approved',
            'message': f'Your ride request from {ride["pickup"]} to {ride["destination"]} has been approved',
            'created_at': datetime.now().isoformat(),
            'read': False
        }
    else:
        booking['status'] = 'rejected'
        
        # Notify the user that their request was rejected
        notification = {
            'id': len(notifications) + 1,
            'user_id': booking['user_id'],
            'type': 'booking_rejected',
            'title': 'Ride Request Rejected',
            'message': f'Your ride request from {ride["pickup"]} to {ride["destination"]} has been rejected',
            'created_at': datetime.now().isoformat(),
            'read': False
        }
    
    notifications.append(notification)
    save_data('notifications')
    save_data('bookings')
    return jsonify({'status': 'success', 'message': f'Booking {action}d successfully'})

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Check if user is already logged in as admin
    if session.get('logged_in') and session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Get admin credentials from environment variables
        admin_username = os.getenv('ADMIN_USERNAME')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        # Validate admin credentials
        if username == admin_username and password == admin_password:
            # Set session for admin
            session['logged_in'] = True
            session['username'] = admin_username
            session['user_id'] = 'admin'
            session['is_admin'] = True
            flash('Admin login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    
    return render_template('admin.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # Check if user is logged in and is admin
    if not session.get('logged_in') or not session.get('is_admin'):
        flash('You must be logged in as an admin to access this page', 'danger')
        return redirect(url_for('login'))
    
    # Ensure all users have created_at and is_verified fields
    for user in users:
        if 'created_at' not in user:
            # Store as ISO format string directly
            user['created_at'] = (datetime.now() - timedelta(days=user['id'])).isoformat()
            save_data('users')
        if 'is_verified' not in user:
            user['is_verified'] = user['id'] % 2 == 0  # Just for demo, alternating verification status
            save_data('users')
    
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin/toggle_user_verification/<int:user_id>', methods=['POST'])
def toggle_user_verification(user_id):
    # Check if user is logged in and is admin
    if not session.get('logged_in') or not session.get('is_admin'):
        flash('You must be logged in as an admin to perform this action', 'danger')
        return redirect(url_for('login'))
    
    # Find the user and toggle verification status
    for user in users:
        if user['id'] == user_id:
            user['is_verified'] = not user.get('is_verified', False)
            status = 'verified' if user['is_verified'] else 'unverified'
            flash(f'User {user["username"]} has been {status}', 'success')
            save_data('users')
            break
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    # Check if user is logged in and is admin
    if not session.get('logged_in') or not session.get('is_admin'):
        flash('You must be logged in as an admin to perform this action', 'danger')
        return redirect(url_for('login'))
    
    # Find the user and remove from the list
    global users
    for i, user in enumerate(users):
        if user['id'] == user_id:
            deleted_user = users.pop(i)
            flash(f'User {deleted_user["username"]} has been deleted', 'success')
            save_data('users')
            break
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        
    # Run the app on local network IP and port 5000
    app.run(host='10.212.12.150', port=5000, debug=True)
