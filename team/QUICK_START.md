# Quick Start Guide - Airport Management System

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- tkinter (usually included with Python)
- pygame
- opencv-python

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Populate database with sample data
python populate_database.py

# Verify system
python verify_system.py

# Run comprehensive tests
python test_all_features.py
```

### Run Application
```bash
python main.py
```
or
```bash
python runmain.py
```

---

## 📋 Key Features

### 1. Manual Gate/Runway Override
- **Location:** ATC Operations → Gate Management / Runway Management
- **Action:** Click "Mark Occupied" to close a gate/runway
- **Effect:** All flights assigned to that gate/runway are delayed by 15 minutes
- **To Release:** Click "Mark Available"

### 2. Crew Management
- **Automatic Assignment:** Crew automatically assigned when flights enter CHECK-IN OPEN
- **Rest Periods:** 30 minutes mandatory rest after each flight
- **View:** Manage Airlines → Edit Crew
- **Assign:** System auto-selects available crew per airline

### 3. Passenger Check-in
- **Auto Check-in:** 10-40% of passengers auto check-in when CHECK-IN OPEN
- **Manual Check-in:** Checkin Desk → Check-in Passenger
- **Threshold:** Flights delayed if <50% checked in at gate closure
- **Baggage:** Track baggage weight per passenger (max 25kg)

### 4. Arriving Flights
- **View:** Home screen → "ARRIVING FLIGHTS" module
- **Display:** Shows all flights arriving to current airport
- **Info:** Status, arrival time, gate, runway, fueling status
- **Airport:** All arrivals are to Chennai by default

### 5. Airport Selection
- **Change Airport:** ⚙ Settings → Current Airport dropdown
- **Available Airports:** 10 major international airports
- **Verification:** Current airport shown in bottom status bar
- **Effect:** Only shows arriving flights for selected airport

### 6. Fueling Tracking
- **Status States:** PENDING → IN PROGRESS → COMPLETED
- **Timing:** 45 minutes default (configurable)
- **Auto Start:** Begins when arrival flight lands (ARRIVED status)
- **View:** Arriving Flights dashboard

---

## ⚙️ Settings Configuration

### How to Access
1. Click "⚙ Settings" button in top bar
2. Configure any of these settings:

### Available Settings

| Setting | Default | Range | Purpose |
|---------|---------|-------|---------|
| **Simulation Time** | 2026-01-01 06:00 | Any valid datetime | Set simulation start time |
| **Growth Rate** | 5 min/sec | 1-30 | Speed up simulation time |
| **Current Airport** | Chennai | 10 cities | Select home airport |
| **Crew Rest Time** | 30 min | Any positive | Rest period after flight |
| **Fueling Time** | 45 min | Any positive | Duration for aircraft fueling |
| **Check-in Threshold** | 50% | 0-100% | Minimum % for departure |
| **Auto Check-in** | Enabled | On/Off | Random passenger check-in |

### How to Apply
1. Modify any settings
2. Click "Apply Settings"
3. Changes saved to `settings.json`
4. UI updates immediately

### Reset Database
- Click "Reset Database" button
- Restores all flights to SCHEDULED status
- Clears gate/runway assignments
- Starts simulation fresh

---

## 📊 Dashboard Overview

### Home Screen
- **MANAGE AIRLINES:** Manage airlines, flights, crews
- **TICKET COUNTER:** Book tickets, view flights
- **ATC OPERATIONS:** Manage gates and runways
- **ARRIVING FLIGHTS:** Monitor inbound aircraft (NEW)

### Airlines Module
- Edit Airlines
- Edit Flights
- Airline Information
- Aircraft Information
- Edit Crew
- Pilot/Crew Data

### ATC Operations
- Gate Management (Mark gates closed)
- Runway Management (Mark runways closed)
- Flight Schedule
- Flight Status Updates

---

## 🎯 Common Workflows

### Close a Gate (to delay flights)
1. Go to: ATC Operations → Gate Management
2. Find target gate
3. Click "Mark Occupied"
4. All flights using that gate will delay 15 min
5. To reopen: Click "Mark Available"

### Assign Crew to a Flight
1. Go to: Manage Airlines → Edit Crew
2. System automatically assigns during simulation
3. Or manually in database

### Check-in Passengers
1. Go to: Checkin Desk → Check-in Passenger
2. Enter passenger ID (e.g., PASS00001)
3. Enter baggage weight (max 25kg)
4. Press Enter to complete

### View Arriving Flights
1. Click "ARRIVING FLIGHTS" module from home
2. See all flights arriving to current airport
3. Check fueling status and gate assignments
4. Monitor arrival status in real-time

### Change Airport
1. Click "⚙ Settings"
2. Select new airport from dropdown
3. Click "Apply Settings"
4. Arriving flights list updates automatically

---

## 📈 Simulation Flow

```
START SIMULATION
    ↓
CHECK-IN OPEN (120 min before departure)
    ↓ [Auto-check passengers 10-40%]
    ↓ [Auto-assign crew if available]
    ↓
BOARDING (30 min before departure)
    ↓
GATE CLOSED (10 min before)
    ↓ [Check if 50%+ passengers checked in]
    ↓ [If <50%: Delay 15 min and restart]
    ↓
TAXIING (5 min before)
    ↓ [Assign runway]
    ↓
DEPARTED (at departure time)
    ↓ [Release gate]
    ↓
IN AIR (between departure and arrival)
    ↓
ARRIVED (at arrival time)
    ↓ [Release gate/runway]
    ↓ [For ARRIVAL flights: Start fueling 45 min]
    ↓
FUELING COMPLETE
    ↓
Ready for next assignment
```

---

## 🐛 Troubleshooting

### Application won't start
- Check Python version: `python --version`
- Install requirements: `pip install -r requirements.txt`
- Check tkinter: `python -m tkinter`

### Database issues
- Run: `python populate_database.py`
- Verify: `python verify_system.py`
- Reset: Use Settings → Reset Database

### Settings not saving
- Check `settings.json` exists in project folder
- Verify file permissions
- Try Settings → Apply Settings again

### Flights not delaying
- Check manual override is set to "CLOSED"
- Verify check-in % is below threshold
- Check simulation time (must be in check-in window)

---

## 📁 File Structure

```
AirportManagement/
├── main.py                      # Main application
├── scheduler.py                 # Flight scheduler (enhanced)
├── db_utils.py                  # Database functions
├── airport_settings.py          # Settings management
├── simulation_engine.py         # Simulation time control
├── airline_module.py            # Airline UI
├── ticket_module.py             # Ticket counter UI
├── atc_module.py                # ATC operations UI
├── checkin_module.py            # Check-in desk UI
├── auth_module.py               # Authentication
├── populate_database.py         # Database populator
├── verify_system.py             # System verification
├── test_all_features.py         # Feature tests
├── settings.json                # Configuration (auto-created)
└── database/
    ├── flights.csv              # All flights
    ├── passengers.csv           # All passengers
    ├── crew.csv                 # All crew
    ├── airlines.csv             # Airline info
    ├── gates.csv                # Gate info
    └── runways.csv              # Runway info
```

---

## 💡 Tips & Tricks

1. **Speed up simulation:** Settings → Growth Rate 30 (1 sec = 30 min)
2. **Test delays:** Close all gates, then watch flights delay
3. **Monitor fueling:** Watch ARRIVING FLIGHTS dashboard for status changes
4. **Crew tracking:** Closed crew members show rest period countdown
5. **Batch check-in:** Auto-check-in runs automatically in CHECK-IN phase
6. **Threshold testing:** Lower threshold makes delays less likely

---

## 📞 Support

For issues or questions:
1. Check IMPLEMENTATION_SUMMARY.md for detailed feature info
2. Review test output: `python test_all_features.py`
3. Check database: `python verify_system.py`
4. Review logs and error messages in terminal

---

## 🎓 Example Scenario

### Test Manual Override Delays

1. **Setup:**
   - Start app: `python main.py`
   - Set simulation time to 07:00
   - Set growth rate to 10 (faster simulation)

2. **Execute:**
   - Go to ATC Operations → Gate Management
   - Find gate A1
   - Click "Mark Occupied"

3. **Observe:**
   - Go to View Flights
   - Watch flights departing around 07:00
   - Flights using gate A1 shift to DELAYED
   - Departure time moves to next slot

4. **Verify:**
   - Check flight status changes
   - Confirm passengers still on flight
   - Release gate when ready

---

**System Status: ✅ PRODUCTION READY**

All 10 features implemented and tested successfully!
