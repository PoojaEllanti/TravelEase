# 🧳 TravelEase - Airline & Train Reservation System

**TravelEase** is a modern, user-friendly travel booking application built with **Python** and **Streamlit**. It allows users to book **train** and **flight** tickets, view or cancel bookings, and search routes by location. Admins can manage routes and bookings in a dedicated admin panel — all styled with a radiant interface.

---

## ✨ Features

### 👥 User Panel
- 🔐 Login / Register as User
- 🚆 Book Train Tickets
- 🛫 Book Flight Tickets
- 📋 View Bookings
- ❌ Cancel Bookings
- 🔎 Search by Location (From → To)

### 🛠 Admin Panel
- 🔐 Login as Admin
- ➕ Add Train/Flight Routes
- 🗑️ Delete Existing Routes
- 📦 Manage Train and Flight Data

### 🎨 UI Styling
- Radiating gradient background
- Sidebar navigation with stylish buttons
- Smooth interaction using Streamlit widgets

---

## 📁 Project Structure

TravelEase/
├── app.py # Main Streamlit app
├── users.json # Registered user credentials
├── bookings.json # Booking records for all users
├── trains.json # Available train routes
├── flights.json # Available flight routes
├── README.md # Project documentation


## 🚀 Getting Started

### ✅ Requirements
- Python 3.7+
- `pip` package manager

### 🔧 Setup Instructions

1. Clone the Repository
   ```bash
   git clone https://github.com/your-username/TravelEase.git
   cd TravelEase
   
Create a Virtual Environment (optional)
python -m venv .venv
.venv\Scripts\activate        # On Windows
source .venv/bin/activate     # On macOS/Linux

Install Dependencies
pip install streamlit

Run the App
streamlit run app.py
👤 Default Admin Login
Role	Username	Password
Admin	admin	admin

📝 Users can register directly through the app interface.

🧪 Data Handling
The app uses simple .json files to manage all data:

users.json → Stores registered usernames and passwords.

bookings.json → Stores each user’s bookings (flights/trains).

trains.json / flights.json → Routes managed by Admin.
