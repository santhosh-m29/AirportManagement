# API Reference & Function Documentation

## Quick Reference

This document provides a complete function reference for the Airport Management System. Use this to understand available functions and how to use them.

---

## db_utils.py - Database Operations

### Flight Operations

#### `get_all_flights() → List[Dict]`
Get all flights in the system.

**Returns:**
- List of flight dictionaries with all fields

**Example:**
```python
from db_utils import get_all_flights
flights = get_all_flights()
for flight in flights:
    print(f"{flight['flight_id']}: {flight['origin']} → {flight['destination']}")
```

---

#### `get_flight(flight_id: str) → Dict`
Get a specific flight by ID.

**Parameters:**
- `flight_id`: Flight ID (e.g., "FL0001")

**Returns:**
- Flight dictionary or None if not found

**Example:**
```python
from db_utils import get_flight
flight = get_flight("FL0001")
if flight:
    print(f"Status: {flight['status']}")
```

---

#### `update_flight_status(flight_id: str, new_status: str) → bool`
Update flight status and save to database.

**Parameters:**
- `flight_id`: Flight ID
- `new_status`: New status (SCHEDULED, CHECK-IN OPEN, BOARDING, etc.)

**Returns:**
- True if successful, False if flight not found

**Valid Statuses:**
- SCHEDULED, CHECK-IN OPEN, BOARDING, GATE CLOSED, TAXIING
- DEPARTED, IN AIR, ARRIVED, DELAYED, CANCELLED

**Example:**
```python
from db_utils import update_flight_status
update_flight_status("FL0001", "BOARDING")
```

---

#### `reschedule_flight(flight_id: str, new_departure: str, new_arrival: str) → bool`
Change departure and/or arrival times.

**Parameters:**
- `flight_id`: Flight ID
- `new_departure`: New departure time (HH:MM format)
- `new_arrival`: New arrival time (HH:MM format)

**Returns:**
- True if successful, False if flight not found

**Example:**
```python
from db_utils import reschedule_flight
reschedule_flight("FL0001", "07:00", "15:15")
```

---

#### `update_flight_fields(flight_id: str, updates: Dict) → bool`
Update multiple flight fields at once.

**Parameters:**
- `flight_id`: Flight ID
- `updates`: Dictionary of field names to new values

**Returns:**
- True if successful, False if flight not found

**Updateable Fields:**
- gate, runway, status, flight_type, fueling_status, crew_assigned, aircraft_type

**Example:**
```python
from db_utils import update_flight_fields
update_flight_fields("FL0001", {
    "gate": "A1",
    "runway": "R1",
    "crew_assigned": "CREW0001"
})
```

---

### Passenger Operations

#### `get_all_passengers() → List[Dict]`
Get all passengers.

**Returns:**
- List of passenger dictionaries

**Example:**
```python
from db_utils import get_all_passengers
passengers = get_all_passengers()
print(f"Total passengers: {len(passengers)}")
```

---

#### `get_flight_passengers(flight_id: str) → List[Dict]`
Get all passengers for a specific flight.

**Parameters:**
- `flight_id`: Flight ID

**Returns:**
- List of passenger dictionaries for that flight

**Example:**
```python
from db_utils import get_flight_passengers
passengers = get_flight_passengers("FL0001")
print(f"Passengers on FL0001: {len(passengers)}")
```

---

#### `auto_checkin_passengers(flight_id: str, percentage: int = 50) → int`
Automatically check-in a random percentage of passengers.

**Parameters:**
- `flight_id`: Flight ID
- `percentage`: % of passengers to check in (default 50)

**Returns:**
- Number of passengers checked in

**Behavior:**
- Selects random passengers not yet checked in
- Assigns random baggage weight (18-25 kg)
- Updates database

**Example:**
```python
from db_utils import auto_checkin_passengers
checked_in = auto_checkin_passengers("FL0001", 60)
print(f"Checked in {checked_in} passengers")
```

---

#### `get_checkin_percentage(flight_id: str) → float`
Get percentage of passengers checked in for a flight.

**Parameters:**
- `flight_id`: Flight ID

**Returns:**
- Percentage (0-100) of checked-in passengers

**Example:**
```python
from db_utils import get_checkin_percentage
percentage = get_checkin_percentage("FL0001")
if percentage < 50:
    print(f"Warning: Only {percentage}% checked in")
```

---

#### `update_passenger_checkin(passenger_id: str, checked_in: int, baggage_weight: float) → bool`
Manually update passenger check-in status.

**Parameters:**
- `passenger_id`: Passenger ID (e.g., "PASS00001")
- `checked_in`: 0 (not checked) or 1 (checked)
- `baggage_weight`: Weight in kg (0-25)

**Returns:**
- True if successful, False if passenger not found

**Example:**
```python
from db_utils import update_passenger_checkin
update_passenger_checkin("PASS00001", 1, 22.5)
```

---

### Crew Operations

#### `get_all_crew() → List[Dict]`
Get all crew members.

**Returns:**
- List of crew dictionaries

**Example:**
```python
from db_utils import get_all_crew
crew = get_all_crew()
print(f"Total crew: {len(crew)}")
```

---

#### `get_airline_crew(airline_id: str) → List[Dict]`
Get all crew members for an airline.

**Parameters:**
- `airline_id`: Airline ID (e.g., "AIR001")

**Returns:**
- List of crew members for that airline

**Example:**
```python
from db_utils import get_airline_crew
crew = get_airline_crew("AIR001")
print(f"Crew at {airline_id}: {len(crew)}")
```

---

#### `get_available_crew(airline_id: str, current_time: datetime) → List[Dict]`
Get crew members available for assignment (not in rest period).

**Parameters:**
- `airline_id`: Airline ID
- `current_time`: Current simulation time

**Returns:**
- List of available crew members

**Logic:**
- Excludes crew where rest_until > current_time
- Returns only crew without assigned flights

**Example:**
```python
from db_utils import get_available_crew
from datetime import datetime

current_time = datetime(2026, 1, 1, 7, 0)
available = get_available_crew("AIR001", current_time)
print(f"Available crew: {len(available)}")
```

---

#### `assign_crew_to_flight(flight_id: str, crew_id: str) → bool`
Assign crew member to flight.

**Parameters:**
- `flight_id`: Flight ID
- `crew_id`: Crew ID

**Returns:**
- True if successful, False if not found

**Behavior:**
- Sets crew_assigned field in flight
- Updates last_flight in crew record

**Example:**
```python
from db_utils import assign_crew_to_flight
assign_crew_to_flight("FL0001", "CREW0001")
```

---

#### `update_crew_assignment(crew_id: str, last_flight: str, rest_until: datetime) → bool`
Update crew rest period after flight assignment.

**Parameters:**
- `crew_id`: Crew ID
- `last_flight`: Flight ID just completed
- `rest_until`: Datetime when rest period ends

**Returns:**
- True if successful

**Example:**
```python
from db_utils import update_crew_assignment
from datetime import datetime, timedelta

rest_until = datetime.now() + timedelta(minutes=30)
update_crew_assignment("CREW0001", "FL0001", rest_until)
```

---

### Gate & Runway Operations

#### `get_all_gates() → List[Dict]`
Get all gates.

**Returns:**
- List of gate dictionaries

**Example:**
```python
from db_utils import get_all_gates
gates = get_all_gates()
for gate in gates:
    print(f"{gate['gate_id']}: {gate['status']}")
```

---

#### `get_all_runways() → List[Dict]`
Get all runways.

**Returns:**
- List of runway dictionaries

**Example:**
```python
from db_utils import get_all_runways
runways = get_all_runways()
for runway in runways:
    print(f"{runway['runway_id']}: {runway['status']}")
```

---

#### `set_gate_override(gate_id: str, override_status: str) → bool`
Mark gate as closed (override).

**Parameters:**
- `gate_id`: Gate ID (e.g., "A1")
- `override_status`: "CLOSED" to close, "" to open

**Returns:**
- True if successful, False if gate not found

**Effect:**
- Closed gates cause 15-min delays for assigned flights

**Example:**
```python
from db_utils import set_gate_override
set_gate_override("A1", "CLOSED")  # Close gate
set_gate_override("A1", "")         # Open gate
```

---

#### `set_runway_override(runway_id: str, override_status: str) → bool`
Mark runway as closed (override).

**Parameters:**
- `runway_id`: Runway ID (e.g., "R1")
- `override_status`: "CLOSED" to close, "" to open

**Returns:**
- True if successful, False if runway not found

**Effect:**
- Closed runways cause 15-min delays for assigned flights

**Example:**
```python
from db_utils import set_runway_override
set_runway_override("R1", "CLOSED")  # Close runway
set_runway_override("R1", "")         # Open runway
```

---

#### `get_gate_override(gate_id: str) → str`
Get override status of a gate.

**Parameters:**
- `gate_id`: Gate ID

**Returns:**
- "CLOSED" if closed, "" if open

**Example:**
```python
from db_utils import get_gate_override
status = get_gate_override("A1")
if status == "CLOSED":
    print("Gate A1 is closed")
```

---

#### `get_runway_override(runway_id: str) → str`
Get override status of a runway.

**Parameters:**
- `runway_id`: Runway ID

**Returns:**
- "CLOSED" if closed, "" if open

**Example:**
```python
from db_utils import get_runway_override
status = get_runway_override("R1")
if status == "CLOSED":
    print("Runway R1 is closed")
```

---

### Fueling Operations

#### `update_fueling_status(flight_id: str, status: str) → bool`
Update fueling status for an arrival flight.

**Parameters:**
- `flight_id`: Flight ID
- `status`: "PENDING", "IN PROGRESS", or "COMPLETED"

**Returns:**
- True if successful, False if flight not found

**Example:**
```python
from db_utils import update_fueling_status
update_fueling_status("FL0081", "IN PROGRESS")
update_fueling_status("FL0081", "COMPLETED")
```

---

#### `get_fueling_status(flight_id: str) → str`
Get current fueling status.

**Parameters:**
- `flight_id`: Flight ID

**Returns:**
- "PENDING", "IN PROGRESS", "COMPLETED", or None

**Example:**
```python
from db_utils import get_fueling_status
status = get_fueling_status("FL0081")
print(f"Fueling status: {status}")
```

---

### Airlines Operations

#### `get_all_airlines() → List[Dict]`
Get all airlines.

**Returns:**
- List of airline dictionaries

**Example:**
```python
from db_utils import get_all_airlines
airlines = get_all_airlines()
for airline in airlines:
    print(f"{airline['airline_id']}: {airline['airline_name']}")
```

---

### Simulation Control

#### `reset_simulation_data() → bool`
Reset all flights to SCHEDULED status and clear assignments.

**Returns:**
- True if successful

**Effect:**
- All flights → SCHEDULED
- All gates → AVAILABLE
- All runways → AVAILABLE
- All crew → Available
- All passengers → Not checked in

**Warning:** This resets the entire simulation

**Example:**
```python
from db_utils import reset_simulation_data
reset_simulation_data()
```

---

## airport_settings.py - Configuration Management

### Settings Loading & Saving

#### `load_settings() → Dict`
Load settings from settings.json file.

**Returns:**
- Dictionary with all settings

**Auto-Creates:**
- If settings.json doesn't exist, creates with defaults

**Example:**
```python
from airport_settings import load_settings
settings = load_settings()
print(f"Airport: {settings['current_airport']}")
```

---

#### `save_settings(settings: Dict) → None`
Save settings to settings.json file.

**Parameters:**
- `settings`: Settings dictionary

**Example:**
```python
from airport_settings import save_settings
settings = {
    "current_airport": "Dubai",
    "auto_checkin_enabled": True,
    "crew_rest_time": 40,
    "fueling_time": 50,
    "checkin_threshold": 60
}
save_settings(settings)
```

---

### Airport Configuration

#### `get_airport() → str`
Get current airport.

**Returns:**
- Airport name (e.g., "Chennai")

**Example:**
```python
from airport_settings import get_airport
airport = get_airport()
print(f"Current airport: {airport}")
```

---

#### `set_airport(airport: str) → None`
Set current airport.

**Parameters:**
- `airport`: Airport name from available list

**Available Airports:**
- Chennai, Dubai, Paris, London, New York, Sydney, Bangkok, Singapore, Tokyo, Hong Kong

**Example:**
```python
from airport_settings import set_airport
set_airport("Dubai")
```

---

### Operational Settings

#### `get_crew_rest_time() → int`
Get crew rest period duration.

**Returns:**
- Minutes (default 30)

**Example:**
```python
from airport_settings import get_crew_rest_time
rest_time = get_crew_rest_time()
print(f"Crew must rest {rest_time} minutes")
```

---

#### `set_crew_rest_time(minutes: int) → None`
Set crew rest period duration.

**Parameters:**
- `minutes`: Duration in minutes

**Example:**
```python
from airport_settings import set_crew_rest_time
set_crew_rest_time(45)
```

---

#### `get_fueling_time() → int`
Get aircraft fueling duration.

**Returns:**
- Minutes (default 45)

**Example:**
```python
from airport_settings import get_fueling_time
fueling = get_fueling_time()
print(f"Fueling takes {fueling} minutes")
```

---

#### `set_fueling_time(minutes: int) → None`
Set aircraft fueling duration.

**Parameters:**
- `minutes`: Duration in minutes

**Example:**
```python
from airport_settings import set_fueling_time
set_fueling_time(60)
```

---

#### `get_checkin_threshold() → int`
Get minimum check-in percentage for departures.

**Returns:**
- Percentage (0-100, default 50)

**Example:**
```python
from airport_settings import get_checkin_threshold
threshold = get_checkin_threshold()
print(f"Need {threshold}% checked in to depart")
```

---

#### `set_checkin_threshold(percentage: int) → None`
Set minimum check-in percentage.

**Parameters:**
- `percentage`: 0-100

**Example:**
```python
from airport_settings import set_checkin_threshold
set_checkin_threshold(60)
```

---

### Auto Check-in Control

#### `is_auto_checkin_enabled() → bool`
Check if auto check-in is enabled.

**Returns:**
- True if enabled, False if disabled

**Example:**
```python
from airport_settings import is_auto_checkin_enabled
if is_auto_checkin_enabled():
    print("Auto check-in is ON")
```

---

#### `set_auto_checkin(enabled: bool) → None`
Enable or disable auto check-in.

**Parameters:**
- `enabled`: True to enable, False to disable

**Example:**
```python
from airport_settings import set_auto_checkin
set_auto_checkin(False)  # Disable auto check-in
```

---

## scheduler.py - Flight Processing

### Event Scheduling

#### `schedule_event(event_time: datetime, event_type: str, **kwargs) → bool`
Schedule an event for processing.

**Parameters:**
- `event_time`: When event occurs
- `event_type`: Type of event
- `kwargs`: Event-specific data

**Event Types:**
- "crew_rest_ends": Crew rest period complete
- "fueling_complete": Aircraft fueling finished
- "gate_release": Gate becomes available
- "runway_release": Runway becomes available

**Example:**
```python
from scheduler import schedule_event
from datetime import datetime, timedelta

event_time = datetime.now() + timedelta(minutes=30)
schedule_event(event_time, "crew_rest_ends", crew_id="CREW0001")
```

---

#### `process_flights(current_time: datetime, dt: int) → Dict`
Main flight processing loop.

**Parameters:**
- `current_time`: Current simulation time
- `dt`: Time step in simulation minutes

**Returns:**
- Dictionary with processing results

**Processing Steps:**
1. Check manual overrides
2. Handle state transitions
3. Auto-assign crew
4. Auto-check-in passengers
5. Verify thresholds
6. Start fueling for arrivals

**Called By:**
- simulation_engine.py every time step

**Example:**
```python
from scheduler import process_flights
from datetime import datetime

results = process_flights(datetime.now(), 5)
print(f"Flights updated: {results.get('flights_processed')}")
```

---

## Common Workflows

### Complete Flight Processing
```python
from db_utils import *
from airport_settings import *
from datetime import datetime

# 1. Get flight
flight = get_flight("FL0001")

# 2. Update status
update_flight_status("FL0001", "CHECK-IN OPEN")

# 3. Auto-assign crew
from scheduler import process_flights
process_flights(datetime.now(), 5)

# 4. Check auto check-in
checkin_pct = get_checkin_percentage("FL0001")
print(f"Check-in: {checkin_pct}%")

# 5. Move to boarding
update_flight_status("FL0001", "BOARDING")
```

---

### Close Gate & Observe Delays
```python
from db_utils import set_gate_override, get_flight
from scheduler import process_flights
from datetime import datetime

# 1. Close gate
set_gate_override("A1", "CLOSED")

# 2. Process flights (will detect override)
process_flights(datetime.now(), 5)

# 3. Check flight status
flight = get_flight("FL0001")  # Uses gate A1
if flight['status'] == "DELAYED":
    print("Flight delayed due to gate closure")

# 4. Open gate
set_gate_override("A1", "")
```

---

### Manual Crew Assignment
```python
from db_utils import *
from airport_settings import get_crew_rest_time
from datetime import datetime, timedelta

# 1. Get available crew
current_time = datetime.now()
crew = get_available_crew("AIR001", current_time)

# 2. Assign to flight
if crew:
    selected = crew[0]
    assign_crew_to_flight("FL0001", selected['crew_id'])
    
    # 3. Schedule rest period
    rest_time = get_crew_rest_time()
    rest_until = current_time + timedelta(minutes=rest_time)
    update_crew_assignment(selected['crew_id'], "FL0001", rest_until)
```

---

### Track Fueling Process
```python
from db_utils import *
from airport_settings import get_fueling_time
from datetime import datetime, timedelta

# 1. Flight arrives
flight = get_flight("FL0081")
if flight['status'] == "ARRIVED":
    
    # 2. Start fueling
    update_fueling_status("FL0081", "IN PROGRESS")
    
    # 3. Schedule completion
    fueling_time = get_fueling_time()
    completion = datetime.now() + timedelta(minutes=fueling_time)
    
    # Process will auto-complete when time reached
```

---

## Error Handling

### Safe Flight Update
```python
from db_utils import get_flight, update_flight_status

flight = get_flight("FL0001")
if flight:
    success = update_flight_status("FL0001", "BOARDING")
    if success:
        print("Status updated")
    else:
        print("Update failed")
else:
    print("Flight not found")
```

---

### Validate Check-in Before Departure
```python
from db_utils import get_checkin_percentage
from airport_settings import get_checkin_threshold

flight_id = "FL0001"
checkin_pct = get_checkin_percentage(flight_id)
threshold = get_checkin_threshold()

if checkin_pct < threshold:
    print(f"Delay: Only {checkin_pct}% checked in (need {threshold}%)")
else:
    print("Clear to depart")
```

---

### Handle Missing Crew
```python
from db_utils import get_available_crew
from datetime import datetime

airline = "AIR001"
available = get_available_crew(airline, datetime.now())

if not available:
    print(f"No available crew for {airline}")
else:
    print(f"Found {len(available)} available crew members")
```

---

## Performance Tips

1. **Cache Results:** Store flight list in memory if querying repeatedly
2. **Batch Updates:** Use update_flight_fields() for multiple changes
3. **Limit Queries:** Filter in Python rather than loading all records
4. **Off-peak Processing:** Schedule heavy operations during off-peak times

---

## Debugging

### Print Flight Details
```python
from db_utils import get_flight
import json

flight = get_flight("FL0001")
print(json.dumps(flight, indent=2))
```

### Verify Settings
```python
from airport_settings import load_settings
import json

settings = load_settings()
print(json.dumps(settings, indent=2))
```

### Check Database State
```python
python verify_system.py
```

---

**API Version:** 2.0
**Last Updated:** 2026-01-01
**Status:** Production Ready ✅
