"""
Smart Bus Ticket Booking & Reservation System
---------------------------------------------
A Python 3 console application (built-in features only).
All data lives in memory and is lost when the program ends.
"""

# ----------------------------------------------------------------------
# DATA
# ----------------------------------------------------------------------

# Tuple: supported departure/destination cities
SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

# List of dictionaries: bus routes
routes = [
    {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad",
     "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur",
     "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas",
     "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore",
     "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad",
     "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30},
]

bookings = []            # list of booking dictionaries
issued_booking_ids = set()  # set of IDs already issued (guarantees uniqueness)
next_booking_number = 1001  # counter used to build IDs like B1001


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------

def read_positive_int(prompt):
    """Ask for a whole number greater than zero. Return None if invalid."""
    text = input(prompt).strip()
    try:
        value = int(text)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def find_route(route_id):
    """Return the route dictionary with this ID, or None."""
    for route in routes:
        if route["route_id"] == route_id:
            return route
    return None


def seat_status(route):
    """Classify a route's seat availability."""
    if route["available_seats"] == 0:
        return "Fully Booked"
    if route["available_seats"] == route["total_seats"]:
        return "Available"
    return "Partially Booked"


def generate_booking_id():
    """Create a booking ID that is not already in the issued set."""
    global next_booking_number
    new_id = "B" + str(next_booking_number)
    while new_id in issued_booking_ids:
        next_booking_number += 1
        new_id = "B" + str(next_booking_number)
    issued_booking_ids.add(new_id)
    next_booking_number += 1
    return new_id


def print_route_table(route_list):
    """Print a numbered table of routes (shows Fully Booked when full)."""
    print("\nAVAILABLE BUS ROUTES")
    print("{:<4} {:<6} {:<26} {:<9} {:<9} {}".format(
        "No.", "Route", "Journey", "Depart", "Fare", "Seats"))
    for number, route in enumerate(route_list, start=1):
        journey = route["departure_city"] + " -> " + route["destination_city"]
        if route["available_seats"] == 0:
            seats = "Fully Booked"
        else:
            seats = "{}/{}".format(route["available_seats"], route["total_seats"])
        print("{:<4} {:<6} {:<26} {:<9} {:<9} {}".format(
            number, route["route_id"], journey, route["departure_time"],
            "Rs." + str(route["ticket_price"]), seats))


# ----------------------------------------------------------------------
# FEATURES
# ----------------------------------------------------------------------

def view_routes():
    """Feature 3 (plus Feature 10: schedule) - view routes."""
    print("\n1. All routes")
    print("2. Only routes with seats available")
    print("3. Schedule by departure city")
    choice = input("Choose a view (1-3): ").strip()

    if choice == "1":
        print_route_table(routes)
    elif choice == "2":
        visible = []
        for route in routes:
            if route["available_seats"] == 0:
                continue  # skip fully booked routes
            visible.append(route)
        if visible:
            print_route_table(visible)
        else:
            print("No routes have seats available.")
    elif choice == "3":
        show_schedule()
    else:
        print("Invalid choice. Please enter 1, 2 or 3.")


def show_schedule():
    """Feature 10 - nested loops: cities (outer) x routes (inner)."""
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")
    for city in SUPPORTED_CITIES:
        print(city)
        found_any = False
        for route in routes:
            if route["departure_city"] == city:
                print("  {} -> {} | {}".format(
                    route["route_id"], route["destination_city"], route["departure_time"]))
                found_any = True
        if not found_any:
            print("  No scheduled departures.")


def search_routes():
    """Feature 4 - search by route ID or city (case-insensitive)."""
    term = input("Search by route ID or city: ").strip()
    if term == "":
        print("Search term cannot be empty.")
        return
    term_lower = term.lower()

    # Step 1: unique route ID match (stop at the first hit with break)
    for route in routes:
        if route["route_id"].lower() == term_lower:
            print("{} | {} -> {} | {} | Rs. {} | {} seats available".format(
                route["route_id"], route["departure_city"], route["destination_city"],
                route["departure_time"], route["ticket_price"], route["available_seats"]))
            break
    else:
        # Step 2: no route ID matched, so look for every city match
        matches = 0
        for route in routes:
            if (route["departure_city"].lower() == term_lower
                    or route["destination_city"].lower() == term_lower):
                print("{} | {} -> {} | Rs. {} | {} seats available".format(
                    route["route_id"], route["departure_city"], route["destination_city"],
                    route["ticket_price"], route["available_seats"]))
                matches += 1
        if matches == 0:
            print("No routes found matching '{}'.".format(term))


def book_ticket():
    """Feature 5 - validate everything first, then change state."""
    print("\nBOOK A TICKET")

    name = input("Passenger name: ").strip()
    if name == "":
        print("Booking failed: name cannot be empty.")
        return

    age = read_positive_int("Passenger age: ")
    if age is None:
        print("Booking failed: age must be a positive whole number.")
        return

    route_id = input("Route ID: ").strip().upper()
    route = find_route(route_id)
    if route is None:
        print("Booking failed: route '{}' does not exist.".format(route_id))
        return

    seats = read_positive_int("Number of seats: ")
    if seats is None:
        print("Booking failed: seats must be a whole number greater than zero.")
        return

    if seats > route["available_seats"]:
        print("Booking failed: only {} seat(s) available on {}.".format(
            route["available_seats"], route["route_id"]))
        return

    # All checks passed - now create the record and update seats
    total_fare = route["ticket_price"] * seats
    booking_id = generate_booking_id()
    bookings.append({
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route["route_id"],
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    })
    route["available_seats"] -= seats

    print("\nBooking confirmed!")
    print("Booking ID: " + booking_id)
    print("Passenger: " + name)
    print("Route: {} ({} -> {})".format(
        route["route_id"], route["departure_city"], route["destination_city"]))
    print("Seats booked: {}".format(seats))
    print("Fare per seat: Rs. {}".format(route["ticket_price"]))
    print("Total fare: Rs. {}".format(total_fare))
    print("Status: Confirmed")


def view_bookings():
    """Feature 6 - list all bookings, including cancelled ones."""
    if not bookings:
        print("No bookings found.")
        return
    print("\nBOOKING HISTORY")
    for number, booking in enumerate(bookings, start=1):
        route = find_route(booking["route_id"])
        journey = route["departure_city"] + " -> " + route["destination_city"]
        print("{}. {} | {} (age {}) | {} ({}) | Seats: {} | Fare: Rs. {} | {}".format(
            number, booking["booking_id"], booking["passenger_name"],
            booking["passenger_age"], booking["route_id"], journey,
            booking["seats"], booking["total_fare"], booking["status"]))


def cancel_booking():
    """Feature 7 - cancel a Confirmed booking and restore seats once."""
    booking_id = input("Enter booking ID to cancel: ").strip().upper()

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking["status"] != "Confirmed":
                print("Booking {} is already cancelled. No changes made.".format(booking_id))
            else:
                route = find_route(booking["route_id"])
                # Status change and seat restoration happen together
                booking["status"] = "Cancelled"
                route["available_seats"] += booking["seats"]
                print("Booking {} has been cancelled.".format(booking_id))
                print("Seats restored: {}".format(booking["seats"]))
                print("Route {} available seats: {}".format(
                    route["route_id"], route["available_seats"]))
            break
    else:
        print("Booking ID '{}' was not found. No changes made.".format(booking_id))


def view_availability():
    """Feature 8 - seats available versus total capacity."""
    only_free = input("Show only routes with seats available? (y/n): ").strip().lower()
    print("\nSEAT AVAILABILITY")
    shown = 0
    for route in routes:
        if only_free == "y" and route["available_seats"] == 0:
            continue
        print("{} | {} -> {} | {}/{} seats | {}".format(
            route["route_id"], route["departure_city"], route["destination_city"],
            route["available_seats"], route["total_seats"], seat_status(route)))
        shown += 1
    if shown == 0:
        print("No routes to show.")


def generate_report():
    """Feature 9 - totals; cancelled bookings are excluded from revenue."""
    total_created = len(bookings)
    confirmed_count = 0
    cancelled_count = 0
    for booking in bookings:
        if booking["status"] == "Confirmed":
            confirmed_count += 1
        else:
            cancelled_count += 1

    seats_reserved = 0
    confirmed_revenue = 0
    fully_booked_routes = 0
    per_route_lines = []

    # Nested loops: outer = routes, inner = matching confirmed bookings
    for route in routes:
        route_bookings = 0
        route_seats = 0
        route_revenue = 0
        for booking in bookings:
            if booking["route_id"] == route["route_id"] and booking["status"] == "Confirmed":
                route_bookings += 1
                route_seats += booking["seats"]
                route_revenue += booking["total_fare"]
        seats_reserved += route_seats
        confirmed_revenue += route_revenue
        if route["available_seats"] == 0:
            fully_booked_routes += 1
        if route_bookings > 0:
            per_route_lines.append("  {}: {} booking(s), {} seat(s), Rs. {:,}".format(
                route["route_id"], route_bookings, route_seats, route_revenue))

    print("\nBOOKING REPORT")
    print("Total bookings created: {}".format(total_created))
    print("Confirmed bookings: {}".format(confirmed_count))
    print("Cancelled bookings: {}".format(cancelled_count))
    print("Seats currently reserved: {}".format(seats_reserved))
    print("Confirmed revenue: Rs. {:,}".format(confirmed_revenue))
    print("Fully booked routes: {}".format(fully_booked_routes))
    if per_route_lines:
        print("Confirmed bookings by route:")
        for line in per_route_lines:
            print(line)


# ----------------------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------------------

def show_menu():
    print("\nSMART BUS RESERVATION SYSTEM")
    print("================================")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("================================")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if not choice.isdigit():
            print("Invalid input. Please enter a number from 1 to 8.")
            continue

        choice = int(choice)
        if choice == 1:
            view_routes()
        elif choice == 2:
            search_routes()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_availability()
        elif choice == 7:
            generate_report()
        elif choice == 8:
            print("Thank you for using Smart Bus. Goodbye!")
            break
        else:
            print("Unsupported option. Please choose between 1 and 8.")


if __name__ == "__main__":
    main()
