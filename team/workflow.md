# Airport Management System Workflow

## Overview

This project is a Tkinter-based airport management application backed by CSV data files. The user interface runs in a single main `tk.Tk()` window (`main.py`) and switches views by replacing the content frame.

## Entry Point

- `runmain.py`: optional intro video launcher using `pygame` and `cv2`.
- `main.py`: actual application entry point.

## Main Window Architecture

- One root window created in `main.py`.
- `main_container` is the central frame that holds the active page.
- `current_frame` stores the currently displayed page.
- `switch_page(page_function, *args)`:
  - destroys `current_frame` if it exists
  - creates a new frame inside `main_container`
  - calls `page_function(current_frame, switch_page, *args)`

## Navigation Flow

1. App start: `show_home()` displays the main menu.
2. User selects a module:
   - MANAGE AIRLINES
   - TICKET COUNTER
   - ATC
   - CHECKIN
3. Selection opens `auth_module.show_passkey_page()`.
4. User enters module-specific passkey.
5. On success, the app routes to the module dashboard.
6. Users browse module functions and navigate back using the same window.

## Modules and Key Pages

### Manage Airlines

- Dashboard: `show_airline_dashboard()`
- Edit Airlines list: `show_edit_airlines()`
- Add airline: `show_add_airline_form()`
- Edit airline: `show_edit_airline_form()`
- Add flights view exists as `show_add_flights_form()` but is not included in the main dashboard currently.

### Ticket Counter

- Dashboard: `show_ticket_dashboard()`
- View flights: `show_flights_list()`
- Book ticket: `show_booking_form()`
- View bookings: `show_bookings_list()`
- Print ticket: `show_print_ticket_prompt()`

### ATC

- Dashboard: `show_atc_dashboard()`
- Gate management: `show_gate_management()`
- Runway management: `show_runway_management()`
- Flight schedule: `show_flight_schedule()`
- Flight status updates: `show_flight_status()`

### Check-in

- Dashboard: `show_checkin_dashboard()`
- Passenger check-in form: `show_checkin_form()`
- Baggage info: `show_baggage_info()`
- Checked-in passengers: `show_checkedin_passengers()`

## Data Management

- CSV files are stored under `database/`.
- `db_utils.py` handles all file reading and writing.
- Data domains:
  - Airlines (`airlines.csv`)
  - Crew (`crew.csv`)
  - Flights (`flights.csv`)
  - Passengers (`passengers.csv`)
  - Runways (`runways.csv`)
  - Gates (`gates.csv`)

## Current Working Behavior

- The app uses a single window and performs page changes by destroying and recreating a frame inside the same window.
- `auth_module` ensures each section is protected by a passkey.
- Each module page builds its own UI inside the provided `parent` frame.
- `main.py` always calls `switch_page()` to remain inside one root Tk session.
- Only the ticket print prompt uses a separate `Toplevel` window.

## Running the Application

1. Run `runmain.py` to play the intro video then start the app.
2. Or run `main.py` directly for the GUI only.
3. Press `Escape` to exit fullscreen mode.

## Current Improvement Opportunities

- Expose all flight edit/add flows consistently in dashboard menus.
- Add validation for CSV operations and missing file handling.
- Centralize repeated UI patterns (headers, list rendering) further.
- Convert secondary `Toplevel` prompt to an in-frame page for full single-window consistency.

## Planned Architecture Extension

- Add `simulation_engine.py` to drive a virtual clock and simulation time progression.
- Add `scheduler.py` to manage ATC events, runway/gate scheduling, and flight timeline changes.
- Keep the single root Tk window and dynamic page switching while moving time-based logic into separate engine modules.
- Use simulated time to power flight status updates, schedule displays, and automated event triggers.
- In `main.py`, call `update_simulation(root)` once before `root.mainloop()` so the simulation loop runs via `root.after(1000, ...)`.
- Add `departure_time` and `arrival_time` fields to `flights.csv`, and use a scheduler engine to automatically move flight records through SCHEDULED, CHECK-IN OPEN, BOARDING, GATE CLOSED, TAXIING, DEPARTED, IN AIR, and ARRIVED states.
- Automate gate and runway occupancy when flights enter `TAXIING`, releasing them automatically after 5 simulated minutes.
- Introduce random delay logic so some flights occasionally move into `DELAYED` state and reschedule departure/arrival times by 15 minutes.
