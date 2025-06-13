import streamlit as st
import json
import os

# ---------- Constants ----------
USER_DATA = "users.json"
BOOKING_DATA = "bookings.json"
TRAIN_DATA = "trains.json"
FLIGHT_DATA = "flights.json"

# ---------- Utility Functions ----------
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Authentication ----------
def login_user(username, password):
    users = load_data(USER_DATA)
    for user in users:
        if isinstance(user, dict) and user.get("username") == username and user.get("password") == password:
            return True
    return False

def register_user(username, password):
    users = load_data(USER_DATA)
    for user in users:
        if isinstance(user, dict) and user.get("username") == username:
            return False
    users.append({"username": username, "password": password})
    save_data(USER_DATA, users)
    return True

# ---------- Booking Functions ----------
def book_ticket(data_file, booking_type):
    st.subheader(f"Book {booking_type} Ticket")
    routes = load_data(data_file)
    if not routes:
        st.info("No routes available. Please try later.")
        return

    selected = st.selectbox(f"Select {booking_type} Route", routes, format_func=lambda x: f"{x['From']} to {x['To']} @ {x['Time']}")
    num_seats = st.number_input("Number of Seats", min_value=1, max_value=selected["Seats"], step=1)

    if st.button("Confirm Booking"):
        booking = {
            "user": st.session_state.username,
            "type": booking_type,
            "From": selected["From"],
            "To": selected["To"],
            "Time": selected["Time"],
            "Fare": selected["Fare"],
            "Seats": num_seats
        }
        bookings = load_data(BOOKING_DATA)
        bookings.append(booking)
        save_data(BOOKING_DATA, bookings)
        st.success("Booking Confirmed!")

# ---------- View Bookings ----------
def view_bookings():
    st.subheader("My Bookings")
    bookings = load_data(BOOKING_DATA)
    user_bookings = [b for b in bookings if isinstance(b, dict) and b.get("user") == st.session_state.username]
    if user_bookings:
        st.table(user_bookings)
    else:
        st.info("No bookings found.")

# ---------- Cancel Booking ----------
def cancel_booking():
    st.subheader("Cancel a Booking")
    bookings = load_data(BOOKING_DATA)
    user_bookings = [b for b in bookings if isinstance(b, dict) and b.get("user") == st.session_state.username]

    if not user_bookings:
        st.info("No bookings to cancel.")
        return

    selected = st.selectbox("Select Booking to Cancel", user_bookings, format_func=lambda x: f"{x['type']} from {x['From']} to {x['To']} at {x['Time']}")
    if st.button("Cancel Booking"):
        bookings.remove(selected)
        save_data(BOOKING_DATA, bookings)
        st.success("Booking Cancelled")

# ---------- Admin Panel ----------
def admin_panel():
    st.subheader("Admin Panel")
    mode = st.radio("Select Mode", ["Train", "Flight"])
    data_file = TRAIN_DATA if mode == "Train" else FLIGHT_DATA

    st.markdown("### Add New Route")
    From = st.text_input("From")
    To = st.text_input("To")
    Time = st.text_input("Time")
    Fare = st.number_input("Fare", min_value=100)
    Seats = st.number_input("Seats", min_value=1)

    if st.button("Add Route"):
        data = load_data(data_file)
        route = {
            f"{mode} No": f"{mode[:1]}{1000 + len(data)}",
            "From": From,
            "To": To,
            "Time": Time,
            "Fare": Fare,
            "Seats": Seats
        }
        data.append(route)
        save_data(data_file, data)
        st.success("Route Added")

    st.markdown("### Existing Routes")
    routes = load_data(data_file)
    if routes:
        selected = st.selectbox("Delete a Route", routes, format_func=lambda x: f"{x['From']} to {x['To']} @ {x['Time']}")
        if st.button("Delete Selected Route"):
            routes.remove(selected)
            save_data(data_file, routes)
            st.success("Route Deleted")
    else:
        st.info("No routes available.")

# ---------- Search Function ----------
def search_routes():
    st.subheader("Search Routes")
    mode = st.radio("Search", ["Train", "Flight"])
    data_file = TRAIN_DATA if mode == "Train" else FLIGHT_DATA

    From = st.text_input("From Location")
    To = st.text_input("To Location")

    if st.button("Search"):
        data = load_data(data_file)
        results = [r for r in data if r["From"].lower() == From.lower() and r["To"].lower() == To.lower()]
        if results:
            st.table(results)
        else:
            st.warning("No matching routes found.")

# ---------- Dashboard ----------
def dashboard():
    st.sidebar.subheader(f"Welcome, {st.session_state.username}!")

    action_list = ["Book Train", "Book Flight", "My Bookings", "Cancel Booking", "Search by Location", "Logout"]
    if st.session_state.role == "Admin":
        action_list.insert(-1, "Admin Panel")

    action = st.sidebar.radio("Navigation", action_list)

    if action == "Book Train":
        book_ticket(TRAIN_DATA, "Train")
    elif action == "Book Flight":
        book_ticket(FLIGHT_DATA, "Flight")
    elif action == "My Bookings":
        view_bookings()
    elif action == "Cancel Booking":
        cancel_booking()
    elif action == "Search by Location":
        search_routes()
    elif action == "Admin Panel":
        admin_panel()
    elif action == "Logout":
        st.session_state.logged_in = False
        st.rerun()

# ---------- UI Styling ----------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #ffecd2, #fcb69f, #ff9a9e);
        color: #1f1f1f;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #fdfcfb, #e2d1c3);
    }
    .stButton>button {
        background-color: #ff6e7f;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5em 1em;
    }
    .stButton>button:hover {
        background-color: #ffa07a;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Main ----------
def main():
    st.title("🧳 TravelEase Reservation System")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("Login to your account")
            login_role = st.radio("Login as", ["User", "Admin"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = login_role

                    # Load sample data for users
                    if login_role == "User":
                        if not load_data(TRAIN_DATA):
                            save_data(TRAIN_DATA, [
                                {"Train No": "12345", "From": "Chennai", "To": "Bangalore", "Time": "07:00 AM", "Seats": 100, "Fare": 500},
                                {"Train No": "54321", "From": "Delhi", "To": "Agra", "Time": "06:30 PM", "Seats": 80, "Fare": 350}
                            ])

                        if not load_data(FLIGHT_DATA):
                            save_data(FLIGHT_DATA, [
                                {"Flight No": "AI101", "From": "Mumbai", "To": "Hyderabad", "Time": "09:30 AM", "Seats": 60, "Fare": 2500},
                                {"Flight No": "SG303", "From": "Kolkata", "To": "Delhi", "Time": "01:45 PM", "Seats": 55, "Fare": 3200}
                            ])

                    st.success(f"Welcome {login_role} {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        elif choice == "Register":
            st.subheader("Create New Account")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Register"):
                if register_user(username, password):
                    st.success("Registration Successful. Please login.")
                else:
                    st.warning("Username already exists.")

    else:
        dashboard()

if __name__ == "__main__":
    main()