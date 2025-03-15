# DyanamicDuo

## Rideshare App

### Overview

The Rideshare App is a web application designed to facilitate ride-sharing specifically for IIT Indore students. Users can request, join, and drive for rides, seamlessly managing their trips through the platform.

### Features

#### User Roles

The system supports three types of users:

- **Offer Ride**
  - Displays available rides for specific dates.
  - Users can view and select rides.

- **Create Ride**
  - Users can create their own ride and allow others to join.
  - Only the creator of the ride has the authority to accept participants.

- **Ride Sharer**
  - Users can search for open ride requests based on destination, arrival time, and passenger count.
  - A sharer can join an open ride and view its status.
  - Sharers can update their participation while the ride is open.

The same user can hold different roles in different rides. For example, a user may be a ride owner, a sharer in another ride, and a driver for another ride.

### System Functionality

#### Account Management

- **Create Account** – Users can create an account.
- **Login/Logout** – Users with an account can log in and log out.

#### Ride Management

- **Ride Selection** – Users participating in multiple rides can select which ride they want to manage.
- **Ride Requesting** – Users can request a ride with specific details (destination, arrival time, passenger count, vehicle preferences, ride-sharing option, and special requests).
- **Ride Editing (Owner)** – Ride owners can edit ride details until it is confirmed.

#### Ride Status Viewing

- **Owners and sharers** can view details of non-completed rides.
- **Drivers** can view confirmed rides along with owner and sharer details.

#### Ride Searching

- **Drivers** can search for open ride requests and claim them.
- **Sharers** can search for open rides and join them.

- **Ride Completion** – Drivers can mark rides as complete.
- **Notifications** – Owners and sharers receive email notifications when a ride is confirmed.

### Installation

#### Prerequisites

Ensure you have the following installed:

- Python (>= 3.8)
- pip (Python package manager)
- Virtual environment (recommended)

#### Setup Steps

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd rideshare_app
   ```

2. **Create and Activate a Virtual Environment (optional but recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the project root.
   - Add necessary environment variables such as database credentials and API keys.

5. **Run the Application**
   ```sh
   python app.py
   ```

### Usage

- Start the server and access the app via `http://10.212.12.150:5000`.
- Navigate through the user profile and ride management sections.
- Monitor ride history and manage active rides.

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Commit changes:
   ```sh
   git commit -m "Added new feature"
   ```
4. Push to your branch:
   ```sh
   git push origin feature-branch
   ```
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

