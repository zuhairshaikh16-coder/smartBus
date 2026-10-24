# Smart Bus Ticket Booking & Reservation System

A text-based Python 3 console application for a small bus service. Browse routes,
search, book seats, cancel bookings, check availability, and view reports.

## Requirements
- Python 3.6 or newer
- No external libraries (built-in Python only)

## How to run
```
python main.py
```

## Menu guide
| Option | Action |
|---|---|
| 1 | View routes: all, only those with seats available, or the schedule grouped by departure city |
| 2 | Search by route ID or city (case-insensitive) |
| 3 | Book a ticket (name, age, route ID, seats) |
| 4 | View all bookings, including cancelled ones |
| 5 | Cancel a Confirmed booking by ID |
| 6 | View seat availability (Available / Partially Booked / Fully Booked) |
| 7 | Generate booking report |
| 8 | Exit |

## Sample workflow
1. Choose `3`, enter `Ahmed`, `24`, `R101`, `2` -> Booking B1001 confirmed, Rs. 2400.
2. Choose `6` -> R101 shows 38/40 seats.
3. Choose `5`, enter `B1001` -> booking cancelled, 2 seats restored.
4. Choose `7` -> report shows 1 cancelled booking and Rs. 0 confirmed revenue.

## Data structures
- **List of dicts**: routes and bookings
- **Tuple**: supported cities
- **Set**: issued booking IDs (guarantees uniqueness)

## Limitations
- All data is stored **in memory only**. Records are lost when the program closes.
- No login, database, payment, or GUI.

## Live website (GitHub Pages)
`index.html` is a browser version of the same system (same routes, rules and
messages) that needs no server. To publish it:

1. Create a new **public** repository on GitHub (e.g. `smart-bus-reservation`).
2. Upload all files from this folder (or push with git, see below).
3. Go to **Settings -> Pages**. Under *Build and deployment* choose
   **Deploy from a branch**, branch **main**, folder **/ (root)**, then Save.
4. After about a minute your site is live at
   `https://<your-username>.github.io/smart-bus-reservation/`.

```
git init
git add .
git commit -m "Smart Bus Reservation System"
git branch -M main
git remote add origin https://github.com/<your-username>/smart-bus-reservation.git
git push -u origin main
```

## Repository contents
| File | Purpose |
|---|---|
| `main.py` | Console application (the PRD deliverable) |
| `index.html` | Browser version for the public website |
| `test_cases.txt` | Test scenarios and results |
| `README.md` | This file |
