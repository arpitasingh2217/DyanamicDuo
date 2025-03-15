# DyanamicDuo
#Rideshare App

Overview

The Rideshare App is a web application that implements a ride-sharing system specifically for IIT Indore students. Students can request, join, and drive for rides, managing their trips seamlessly through the platform.

Features

User Roles

The system supports three types of users:

Offer Ride
Here available rides are shown , rides are shown on specific dates
Create Ride 
Users can create their own ride and allow people to access it
Only the creater of the ride can accept it

Ride Sharer

Users can search for open ride requests based on destination, arrival time, and passenger count.

A sharer can join an open ride and view its status.

Sharers can update their participation while the ride is open.

The same user can hold different roles in different rides. For example, a user may be a ride owner, a sharer in another ride, and a driver for another ride.

System Functionality

Account Management

Create Account – Users can create an account.

Login/Logout – Users with an account can log in and log out.

Ride Management

Ride Selection – Users part of multiple rides can select the ride they want to manage.

Ride Requesting – Users can request a ride with specific details (destination, arrival time, passenger count, vehicle preferences, ride-sharing option, and special requests).

Ride Editing (Owner) – Ride owners can edit ride details until it is confirmed.

Ride Status Viewing

Owners and sharers can view non-complete rides and details.

Drivers can view confirmed rides with owner and sharer details.

Ride Searching

Drivers can search for open ride requests and claim them.

Sharers can search for open rides and join them.

Ride Completion – Drivers can mark rides as complete.

Notifications – When a ride is confirmed, owners and sharers receive email notifications.

Installation

Prerequisites

Ensure you have the following installed:

Python (>= 3.8)

pip (Python package manager)

Virtual environment (recommended)

Setup Steps

Clone the Repository

git clone <repository-url>
cd rideshare_app

Create and Activate a Virtual Environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Set Up Environment Variables

Create a .env file in the project root.

Add necessary environment variables such as database credentials and API keys.

Run the Application

python app.py

Usage

Start the server and access the app via http://localhost:5000

Navigate through the user profile and ride management sections

Monitor ride history and manage active rides
