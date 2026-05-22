# Database Schema Documentation

## Overview
The Airport Management System uses CSV-based storage with JSON settings persistence. This document describes the schema of each database file.

---

## flights.csv

**Purpose:** Stores all flights (departures and arrivals)
**Total Records:** 106 flights (80 departing, 26 arriving)

### Schema

| Column | Type | Description | Example | New? |
|--------|------|-------------|---------|------|
| flight_id | String | Unique flight identifier | FL0001 | ❌ |
| airline_id | String | Operating airline | AIR001 | ❌ |
| origin | String | Departure airport | Chennai | ❌ |
| destination | String | Arrival airport | Paris | ❌ |
| departure_time | Time | Scheduled departure time | 06:30 | ❌ |
| arrival_time | Time | Scheduled arrival time | 14:45 | ❌ |
| aircraft_type | String | Aircraft model | Boeing 777 | ❌ |
| gate | String | Assigned gate | A1 | ❌ |
| runway | String | Assigned runway | R1 | ❌ |
| status | String | Current flight status | SCHEDULED | ❌ |
| **flight_type** | String | DEPARTURE or ARRIVAL | DEPARTURE | ✅ |
| **fueling_status** | String | PENDING, IN PROGRESS, COMPLETED | PENDING | ✅ |
| **crew_assigned** | String | Crew member ID assigned | CREW0001 | ✅ |

### Valid Flight Types
- **DEPARTURE:** Flight departs from airport
- **ARRIVAL:** Flight arrives at airport

### Valid Flight Statuses
- **SCHEDULED:** Flight not yet active
- **CHECK-IN OPEN:** Check-in counter open (120 min before)
- **BOARDING:** Boarding in progress (30 min before)
- **GATE CLOSED:** Gate closed, ready for push-back (10 min before)
- **TAXIING:** Aircraft taxiing to runway (5 min before)
- **DEPARTED:** Aircraft left airport
- **IN AIR:** Aircraft in flight
- **ARRIVED:** Aircraft landed at destination
- **DELAYED:** Flight is delayed
- **CANCELLED:** Flight cancelled

### Valid Fueling Status (Arrival Flights Only)
- **PENDING:** Waiting to start fueling
- **IN PROGRESS:** Currently being fueled
- **COMPLETED:** Fueling finished (ready for next flight)

### Sample Records

**Departure Flight:**
```
FL0001,AIR001,Chennai,Paris,06:30,14:45,Boeing 777,A1,R1,SCHEDULED,DEPARTURE,PENDING,
```

**Arrival Flight:**
```
FL0081,AIR002,Mumbai,Chennai,00:45,00:45,Airbus A380,D1,R2,SCHEDULED,ARRIVAL,PENDING,
```

---

## passengers.csv

**Purpose:** Stores all passengers for all flights
**Total Records:** 1,060 passengers (10 per flight)

### Schema

| Column | Type | Description | Example | New? |
|--------|------|-------------|---------|------|
| passenger_id | String | Unique passenger ID | PASS00001 | ❌ |
| flight_id | String | Flight booked | FL0001 | ❌ |
| name | String | Full name | John Smith | ❌ |
| seat | String | Seat assignment | 12A | ❌ |
| checked_in | Integer | Check-in status (0/1) | 0 | ❌ |
| baggage_weight | Float | Baggage weight (kg) | 22.5 | ❌ |

### Valid Checked-in Values
- **0:** Not checked in
- **1:** Checked in

### Baggage Constraints
- Maximum: 25.0 kg
- Minimum: 0.0 kg
- Default: 20.0 kg (average)

### Sample Records
```
PASS00001,FL0001,John Smith,12A,0,20.5
PASS00002,FL0001,Sarah Johnson,12B,1,22.0
PASS00003,FL0001,Michael Brown,13A,0,18.5
```

---

## crew.csv

**Purpose:** Stores all crew members across airlines
**Total Records:** 100 crew members (10 per airline)

### Schema

| Column | Type | Description | Example | New? |
|--------|------|-------------|---------|------|
| crew_id | String | Unique crew identifier | CREW0001 | ❌ |
| name | String | Full name | Robert Martinez | ❌ |
| airline_id | String | Airline ID | AIR001 | ❌ |
| role | String | Position | Captain | ❌ |
| **last_flight** | String | Last assigned flight | FL0045 | ✅ |
| **rest_until** | Datetime | When rest period ends | 2026-01-01 07:00 | ✅ |

### Valid Crew Roles
- **Captain:** Pilot in command
- **First Officer:** Copilot
- **Flight Attendant:** Cabin crew

### Rest Period Logic
- Default rest time: 30 minutes (configurable in settings)
- Rest starts: When flight departs
- Rest ends: 30 minutes after departure
- During rest: Crew unavailable for assignment

### Sample Records
```
CREW0001,Robert Martinez,AIR001,First Officer,FL0045,2026-01-01 07:00
CREW0002,Jennifer Lee,AIR001,Flight Attendant,,Available
CREW0003,David Johnson,AIR001,Captain,FL0050,2026-01-02 08:30
```

---

## gates.csv

**Purpose:** Stores all gates at the airport
**Total Records:** 16 gates (4 terminals × 4 gates)

### Schema

| Column | Type | Description | Example | New? |
|--------|------|-------------|---------|------|
| gate_id | String | Unique gate identifier | A1 | ❌ |
| terminal | String | Terminal name | Terminal A | ❌ |
| status | String | Gate status | AVAILABLE | ❌ |
| **manual_override** | String | Override status (CLOSED or empty) | CLOSED | ✅ |

### Valid Gate Statuses
- **AVAILABLE:** Ready for assignment
- **OCCUPIED:** Flight currently using gate
- **UNDER_MAINTENANCE:** Gate closed for maintenance

### Manual Override Values
- **Empty string:** No override (normal operation)
- **"CLOSED":** Gate manually closed, flights delayed

### Terminal Structure
- **Terminal A:** Gates A1, A2, A3, A4
- **Terminal B:** Gates B1, B2, B3, B4
- **Terminal C:** Gates C1, C2, C3, C4
- **Terminal D:** Gates D1, D2, D3, D4

### Sample Records
```
A1,Terminal A,OCCUPIED,
A2,Terminal A,AVAILABLE,CLOSED
A3,Terminal A,AVAILABLE,
B1,Terminal B,AVAILABLE,
D1,Terminal D,OCCUPIED,
```

---

## runways.csv

**Purpose:** Stores all runways at the airport
**Total Records:** 4 runways

### Schema

| Column | Type | Description | Example | New? |
|--------|------|-------------|---------|------|
| runway_id | String | Unique runway identifier | R1 | ❌ |
| length | String | Runway length (meters) | 4500m | ❌ |
| status | String | Runway status | AVAILABLE | ❌ |
| **manual_override** | String | Override status (CLOSED or empty) | CLOSED | ✅ |

### Valid Runway Statuses
- **AVAILABLE:** Ready for landing/takeoff
- **IN_USE:** Aircraft currently on runway
- **CLOSED:** Runway closed for maintenance

### Manual Override Values
- **Empty string:** No override (normal operation)
- **"CLOSED":** Runway manually closed, flights delayed

### Runway Properties
- **R1:** 4500m (long-haul capable)
- **R2:** 4200m (long-haul capable)
- **R3:** 3500m (medium-haul)
- **R4:** 3000m (short-haul)

### Sample Records
```
R1,4500m,AVAILABLE,
R2,4200m,IN_USE,
R3,3500m,AVAILABLE,CLOSED
R4,3000m,AVAILABLE,
```

---

## airlines.csv

**Purpose:** Stores airline information
**Total Records:** 10 airlines

### Schema

| Column | Type | Description | Example | New? |
|--------|------|-------------|---------|------|
| airline_id | String | Unique airline identifier | AIR001 | ❌ |
| airline_name | String | Full airline name | Indian Airlines | ❌ |
| country | String | Country of origin | India | ❌ |
| established_year | Integer | Year established | 1932 | ❌ |
| fleet_size | Integer | Total aircraft | 45 | ❌ |

### Airlines in Database
| Code | Name | Country |
|------|------|---------|
| AIR001 | Indian Airlines | India |
| AIR002 | Emirates | UAE |
| AIR003 | Air France | France |
| AIR004 | British Airways | UK |
| AIR005 | United Airlines | USA |
| AIR006 | Qantas | Australia |
| AIR007 | Thai Airways | Thailand |
| AIR008 | Singapore Airlines | Singapore |
| AIR009 | Japan Airlines | Japan |
| AIR010 | Cathay Pacific | Hong Kong |

### Sample Record
```
AIR001,Indian Airlines,India,1932,45
```

---

## settings.json

**Purpose:** Stores simulation and operational configuration
**Location:** Root directory (created on first run)
**Format:** JSON

### Schema

```json
{
  "current_airport": "Chennai",
  "auto_checkin_enabled": true,
  "crew_rest_time": 30,
  "fueling_time": 45,
  "checkin_threshold": 50
}
```

### Settings Reference

| Setting | Type | Default | Range | Description |
|---------|------|---------|-------|-------------|
| current_airport | String | Chennai | 10 cities | Home airport for arriving flights |
| auto_checkin_enabled | Boolean | true | true/false | Enable automatic passenger check-in |
| crew_rest_time | Integer | 30 | 1-480 | Rest period after flight (minutes) |
| fueling_time | Integer | 45 | 1-480 | Time to fuel arrival aircraft (minutes) |
| checkin_threshold | Integer | 50 | 0-100 | Minimum % for departure (will delay if below) |

### Available Airports
- Chennai
- Dubai
- Paris
- London
- New York
- Sydney
- Bangkok
- Singapore
- Tokyo
- Hong Kong

### Example Configuration
```json
{
  "current_airport": "Dubai",
  "auto_checkin_enabled": true,
  "crew_rest_time": 45,
  "fueling_time": 60,
  "checkin_threshold": 60
}
```

---

## Data Relationships

### Flight → Passengers
```
One Flight → Many Passengers (1:N)
flight_id (flights.csv) → flight_id (passengers.csv)
Ratio: 1 flight → 10 passengers
Total: 106 flights × 10 = 1,060 passengers
```

### Flight → Crew
```
One Flight → One Crew (N:1, at assignment time)
crew_assigned (flights.csv) → crew_id (crew.csv)
Assignment: Done when flight enters CHECK-IN OPEN
```

### Flight → Gate
```
One Gate → One Flight (at any time)
gate (flights.csv) → gate_id (gates.csv)
Assignment: Done when flight enters BOARDING
Release: When flight departs
```

### Flight → Runway
```
One Runway → One Flight (at any time)
runway (flights.csv) → runway_id (runways.csv)
Assignment: Done when flight enters TAXIING
Release: When flight departs
```

### Flight → Airline
```
Many Flights → One Airline (N:1)
airline_id (flights.csv) → airline_id (airlines.csv)
```

### Crew → Airline
```
Many Crew → One Airline (N:1)
airline_id (crew.csv) → airline_id (airlines.csv)
Ratio: 10 crew per airline
```

---

## Data Integrity Rules

### Flights
- ✅ flight_id must be unique
- ✅ status must be valid state
- ✅ flight_type must be DEPARTURE or ARRIVAL
- ✅ arrival_flights have destination = current_airport

### Passengers
- ✅ passenger_id must be unique
- ✅ flight_id must exist in flights.csv
- ✅ seat format: [row][A-D] (e.g., 12A)
- ✅ checked_in must be 0 or 1
- ✅ baggage_weight must be ≥ 0 and ≤ 25

### Crew
- ✅ crew_id must be unique
- ✅ airline_id must exist in airlines.csv
- ✅ role must be valid
- ✅ rest_until timestamp must be valid datetime

### Gates
- ✅ gate_id must be unique
- ✅ gate_id format: [Terminal][1-4] (e.g., A1)
- ✅ status must be valid
- ✅ manual_override must be empty or "CLOSED"

### Runways
- ✅ runway_id must be unique
- ✅ runway_id format: R[1-4]
- ✅ status must be valid
- ✅ manual_override must be empty or "CLOSED"

### Settings
- ✅ All required fields present
- ✅ current_airport in available list
- ✅ crew_rest_time > 0
- ✅ fueling_time > 0
- ✅ checkin_threshold between 0-100
- ✅ auto_checkin_enabled is boolean

---

## CSV Format

### Character Encoding
- **Encoding:** UTF-8
- **Line Terminator:** CRLF (\r\n)
- **Delimiter:** Comma (,)
- **Quote Character:** Double quote (")

### Escaping Rules
- Fields containing commas enclosed in quotes
- Fields containing quotes: quote doubled
- Example: `"Field with, comma"`, `"Field with "" quote"`

### Data Types
- **String:** Text values, no quotes needed for simple strings
- **Integer:** Whole numbers, no quotes
- **Float:** Decimal numbers with dots, no quotes
- **Datetime:** ISO format YYYY-MM-DD HH:MM[:SS]
- **Time:** HH:MM format for times of day

---

## Migration Guide

### Adding New Columns
1. Add column name to FLIGHT_FIELDS/PASSENGER_FIELDS tuples in db_utils.py
2. Update _normalize_flight_row() with default value
3. Existing records auto-populate with default
4. New records populate in CSV writes

### Changing Field Values
1. Use db_utils functions (update_flight_status, etc.)
2. Never edit CSV directly with text editor
3. Functions ensure all fields preserved

### Backing Up Database
```bash
# Copy entire database directory
cp -r database database.backup.$(date +%Y%m%d_%H%M%S)

# Copy specific CSV
cp database/flights.csv database/flights.csv.backup
```

---

## Database Validation

Run `verify_system.py` to check:
- ✅ All CSV files present and readable
- ✅ All required columns present
- ✅ Record counts correct
- ✅ Sample records display properly
- ✅ Settings file loads correctly
- ✅ No data integrity issues

```bash
python verify_system.py
```

---

**Last Updated:** 2026-01-01
**Schema Version:** 2.0 (with new fields for crew, fueling, overrides)
**Production Ready:** ✅ YES
