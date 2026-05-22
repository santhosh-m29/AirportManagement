# db_utils.py
import csv
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database")

# ===================== AIRLINES =====================
def get_all_airlines():
    airlines = []
    path = os.path.join(DB_PATH, "airlines.csv")
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            airlines.append(row)
            
    # Dynamically compute flight count
    try:
        flights = get_all_flights()
        counts = {}
        for flight in flights:
            airline_id = flight.get('airline')
            if airline_id:
                counts[airline_id] = counts.get(airline_id, 0) + 1
        for airline in airlines:
            aid = airline['airline_id']
            airline['flights'] = str(counts.get(aid, 0))
    except Exception as e:
        pass
        
    return airlines

def add_airline(airline_id, name, flights="0"):
    path = os.path.join(DB_PATH, "airlines.csv")
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([airline_id, name, flights])

def update_airline(airline_id, name, flights):
    path = os.path.join(DB_PATH, "airlines.csv")
    airlines = get_all_airlines()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['airline_id', 'name', 'flights'])
        writer.writeheader()
        for airline in airlines:
            if airline['airline_id'] == airline_id:
                writer.writerow({'airline_id': airline_id, 'name': name, 'flights': flights})
            else:
                writer.writerow(airline)

def delete_airline(airline_id):
    path = os.path.join(DB_PATH, "airlines.csv")
    airlines = get_all_airlines()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['airline_id', 'name', 'flights'])
        writer.writeheader()
        for airline in airlines:
            if airline['airline_id'] != airline_id:
                writer.writerow(airline)

# ===================== CREW =====================
def get_all_crew():
    crew = []
    path = os.path.join(DB_PATH, "crew.csv")
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            crew.append(row)
    return crew

def get_crew_status(crew_member, current_time_str=None):
    """Get status of crew member: 'Available', 'On Rest', or 'Assigned'."""
    import simulation_engine
    if current_time_str is None:
        try:
            current_time_str = simulation_engine.get_sim_time().strftime("%H:%M")
        except:
            current_time_str = "06:00"
            
    flights = get_all_flights()
    active_flight = None
    for f in flights:
        if f.get('crew_assigned') == crew_member['crew_id'] and f.get('status') not in ['ARRIVED', 'CANCELLED']:
            active_flight = f['flight_id']
            break
            
    if active_flight:
        return f"Assigned to {active_flight}"
        
    rest_until = crew_member.get('rest_until', '')
    if rest_until:
        try:
            from datetime import datetime
            rest_time = datetime.strptime(rest_until, "%H:%M")
            curr_time = datetime.strptime(current_time_str, "%H:%M")
            if curr_time < rest_time:
                return f"Resting (until {rest_until})"
        except:
            pass
            
    return "Available"

def add_crew(crew_id, name, role, airline_id):
    path = os.path.join(DB_PATH, "crew.csv")
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([crew_id, name, role, airline_id])

def get_crew_by_airline(airline_id):
    crew = []
    all_crew = get_all_crew()
    for member in all_crew:
        if member.get('airline_id') == airline_id:
            crew.append(member)
    return crew

# ===================== CREW MANAGEMENT =====================
def update_crew_assignment(crew_id, last_flight, rest_until):
    """Update crew member's last flight and rest period."""
    path = os.path.join(DB_PATH, "crew.csv")
    crew = get_all_crew()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['crew_id', 'name', 'role', 'airline_id', 'last_flight', 'rest_until'])
        writer.writeheader()
        for member in crew:
            if member['crew_id'] == crew_id:
                member['last_flight'] = last_flight
                member['rest_until'] = rest_until
            writer.writerow(member)

def get_available_crew(airline_id, current_time):
    """Get crew members available for assignment (not on rest)."""
    from datetime import datetime
    crew_list = get_crew_by_airline(airline_id)
    available = []
    for member in crew_list:
        rest_until = member.get('rest_until', '')
        if not rest_until:
            available.append(member)
        else:
            try:
                rest_time = datetime.strptime(rest_until, "%H:%M")
                current = datetime.strptime(current_time, "%H:%M")
                if current >= rest_time:
                    available.append(member)
            except:
                available.append(member)
    return available

def assign_crew_to_flight(flight_id, crew_id):
    """Assign a crew member to a flight."""
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] == flight_id:
                flight['crew_assigned'] = crew_id
            writer.writerow({
                'flight_id': flight['flight_id'],
                'airline': flight.get('airline', flight.get('airline_id', '')),
                'origin': flight.get('origin', ''),
                'destination': flight.get('destination', ''),
                'departure_time': flight.get('departure_time', ''),
                'arrival_time': flight.get('arrival_time', ''),
                'status': flight.get('status', ''),
                'gate': flight.get('gate', ''),
                'runway': flight.get('runway', ''),
                'flight_type': flight.get('flight_type', 'DEPARTURE'),
                'fueling_status': flight.get('fueling_status', 'PENDING'),
                'crew_assigned': flight.get('crew_assigned', '')
            })

# ===================== FLIGHTS =====================
FLIGHT_FIELDS = ['flight_id', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'status', 'gate', 'runway', 'flight_type', 'fueling_status', 'crew_assigned', 'manual_override']


def _normalize_flight_row(row):
    airline = row.get('airline') or row.get('airline_id', '')
    departure = row.get('departure_time') or row.get('departure', '')
    arrival = row.get('arrival_time') or row.get('arrival', '')

    normalized = {
        'flight_id': row.get('flight_id', ''),
        'airline': airline,
        'airline_id': airline,
        'origin': row.get('origin', ''),
        'destination': row.get('destination', ''),
        'departure_time': departure,
        'departure': departure,
        'arrival_time': arrival,
        'arrival': arrival,
        'status': row.get('status', ''),
        'gate': row.get('gate', ''),
        'runway': row.get('runway', ''),
        'flight_type': row.get('flight_type', 'DEPARTURE'),
        'fueling_status': row.get('fueling_status', 'PENDING'),
        'crew_assigned': row.get('crew_assigned', ''),
        'manual_override': row.get('manual_override', '')
    }
    return normalized


def get_all_flights():
    flights = []
    path = os.path.join(DB_PATH, "flights.csv")
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            flights.append(_normalize_flight_row(row))
    return flights


def add_flight(flight_id, airline_id, origin, destination, departure, arrival, gate, runway):
    path = os.path.join(DB_PATH, "flights.csv")
    with open(path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writerow({
            'flight_id': flight_id,
            'airline': airline_id,
            'origin': origin,
            'destination': destination,
            'departure_time': departure,
            'arrival_time': arrival,
            'status': "SCHEDULED",
            'gate': gate,
            'runway': runway,
            'flight_type': 'DEPARTURE',
            'fueling_status': 'PENDING',
            'crew_assigned': '',
            'manual_override': ''
        })


def update_flight_status(flight_id, status, manual_override=None):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] == flight_id:
                flight['status'] = status
                if manual_override is not None:
                    flight['manual_override'] = manual_override
            writer.writerow({
                'flight_id': flight['flight_id'],
                'airline': flight.get('airline', flight.get('airline_id', '')),
                'origin': flight.get('origin', ''),
                'destination': flight.get('destination', ''),
                'departure_time': flight.get('departure_time', ''),
                'arrival_time': flight.get('arrival_time', ''),
                'status': flight.get('status', ''),
                'gate': flight.get('gate', ''),
                'runway': flight.get('runway', ''),
                'flight_type': flight.get('flight_type', 'DEPARTURE'),
                'fueling_status': flight.get('fueling_status', 'PENDING'),
                'crew_assigned': flight.get('crew_assigned', ''),
                'manual_override': flight.get('manual_override', '')
            })


def reschedule_flight(flight_id, departure_time, arrival_time, status=None):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] == flight_id:
                writer.writerow({
                    'flight_id': flight['flight_id'],
                    'airline': flight.get('airline', flight.get('airline_id', '')),
                    'origin': flight.get('origin', ''),
                    'destination': flight.get('destination', ''),
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'status': status if status is not None else flight.get('status', ''),
                    'gate': flight.get('gate', ''),
                    'runway': flight.get('runway', ''),
                    'flight_type': flight.get('flight_type', 'DEPARTURE'),
                    'fueling_status': flight.get('fueling_status', 'PENDING'),
                    'crew_assigned': flight.get('crew_assigned', ''),
                    'manual_override': flight.get('manual_override', '')
                })
            else:
                writer.writerow({
                    'flight_id': flight['flight_id'],
                    'airline': flight.get('airline', flight.get('airline_id', '')),
                    'origin': flight.get('origin', ''),
                    'destination': flight.get('destination', ''),
                    'departure_time': flight.get('departure_time', ''),
                    'arrival_time': flight.get('arrival_time', ''),
                    'status': flight.get('status', ''),
                    'gate': flight.get('gate', ''),
                    'runway': flight.get('runway', ''),
                    'flight_type': flight.get('flight_type', 'DEPARTURE'),
                    'fueling_status': flight.get('fueling_status', 'PENDING'),
                    'crew_assigned': flight.get('crew_assigned', ''),
                    'manual_override': flight.get('manual_override', '')
                })


def update_flight_fields(flight_id, **fields):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] == flight_id:
                updated = {
                    'flight_id': flight['flight_id'],
                    'airline': flight.get('airline', flight.get('airline_id', '')),
                    'origin': flight.get('origin', ''),
                    'destination': flight.get('destination', ''),
                    'departure_time': flight.get('departure_time', ''),
                    'arrival_time': flight.get('arrival_time', ''),
                    'status': flight.get('status', ''),
                    'gate': flight.get('gate', ''),
                    'runway': flight.get('runway', ''),
                    'flight_type': flight.get('flight_type', 'DEPARTURE'),
                    'fueling_status': flight.get('fueling_status', 'PENDING'),
                    'crew_assigned': flight.get('crew_assigned', ''),
                    'manual_override': flight.get('manual_override', '')
                }
                updated.update(fields)
                writer.writerow(updated)
            else:
                writer.writerow({
                    'flight_id': flight['flight_id'],
                    'airline': flight.get('airline', flight.get('airline_id', '')),
                    'origin': flight.get('origin', ''),
                    'destination': flight.get('destination', ''),
                    'departure_time': flight.get('departure_time', ''),
                    'arrival_time': flight.get('arrival_time', ''),
                    'status': flight.get('status', ''),
                    'gate': flight.get('gate', ''),
                    'runway': flight.get('runway', ''),
                    'flight_type': flight.get('flight_type', 'DEPARTURE'),
                    'fueling_status': flight.get('fueling_status', 'PENDING'),
                    'crew_assigned': flight.get('crew_assigned', ''),
                    'manual_override': flight.get('manual_override', '')
                })


def update_flight(flight_id, new_flight_id, airline_id, origin, destination, departure, arrival, gate, runway, status):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] == flight_id:
                writer.writerow({
                    'flight_id': new_flight_id,
                    'airline': airline_id,
                    'origin': origin,
                    'destination': destination,
                    'departure_time': departure,
                    'arrival_time': arrival,
                    'status': status,
                    'gate': gate,
                    'runway': runway,
                    'flight_type': flight.get('flight_type', 'DEPARTURE'),
                    'fueling_status': flight.get('fueling_status', 'PENDING'),
                    'crew_assigned': flight.get('crew_assigned', ''),
                    'manual_override': flight.get('manual_override', '')
                })
            else:
                writer.writerow({
                    'flight_id': flight['flight_id'],
                    'airline': flight.get('airline', flight.get('airline_id', '')),
                    'origin': flight.get('origin', ''),
                    'destination': flight.get('destination', ''),
                    'departure_time': flight.get('departure_time', ''),
                    'arrival_time': flight.get('arrival_time', ''),
                    'status': flight.get('status', ''),
                    'gate': flight.get('gate', ''),
                    'runway': flight.get('runway', ''),
                    'flight_type': flight.get('flight_type', 'DEPARTURE'),
                    'fueling_status': flight.get('fueling_status', 'PENDING'),
                    'crew_assigned': flight.get('crew_assigned', ''),
                    'manual_override': flight.get('manual_override', '')
                })


def delete_flight(flight_id):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] != flight_id:
                writer.writerow({
                    'flight_id': flight['flight_id'],
                    'airline': flight.get('airline', flight.get('airline_id', '')),
                    'origin': flight.get('origin', ''),
                    'destination': flight.get('destination', ''),
                    'departure_time': flight.get('departure_time', ''),
                    'arrival_time': flight.get('arrival_time', ''),
                    'status': flight.get('status', ''),
                    'gate': flight.get('gate', ''),
                    'runway': flight.get('runway', ''),
                    'flight_type': flight.get('flight_type', 'DEPARTURE'),
                    'fueling_status': flight.get('fueling_status', 'PENDING'),
                    'crew_assigned': flight.get('crew_assigned', ''),
                    'manual_override': flight.get('manual_override', '')
                })


def get_flights_by_airline(airline_id):
    flights = []
    all_flights = get_all_flights()
    for flight in all_flights:
        if flight.get('airline_id') == airline_id or flight.get('airline') == airline_id:
            flights.append(flight)
    return flights

# ===================== PASSENGERS =====================
def get_all_passengers():
    passengers = []
    path = os.path.join(DB_PATH, "passengers.csv")
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            passengers.append(row)
    return passengers

def add_passenger(passenger_id, name, flight_id, seat, checked_in="No", baggage_weight="0"):
    path = os.path.join(DB_PATH, "passengers.csv")
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([passenger_id, name, flight_id, seat, checked_in, baggage_weight])

def update_passenger_checkin(passenger_id, checked_in, baggage_weight):
    path = os.path.join(DB_PATH, "passengers.csv")
    passengers = get_all_passengers()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['passenger_id', 'name', 'flight_id', 'seat', 'checked_in', 'baggage_weight'])
        writer.writeheader()
        for passenger in passengers:
            if passenger['passenger_id'] == passenger_id:
                passenger['checked_in'] = checked_in
                passenger['baggage_weight'] = baggage_weight
            writer.writerow(passenger)

def get_passengers_by_flight(flight_id):
    passengers = []
    all_passengers = get_all_passengers()
    for passenger in all_passengers:
        if passenger.get('flight_id') == flight_id:
            passengers.append(passenger)
    return passengers

# ===================== RUNWAYS =====================
def get_all_runways():
    runways = []
    path = os.path.join(DB_PATH, "runways.csv")
    if not os.path.exists(path):
        return []
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            runways.append(row)
    return runways

def add_runway(runway_id, length, status="Available"):
    path = os.path.join(DB_PATH, "runways.csv")
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['runway_id', 'length', 'status', 'manual_override'])
            writer.writeheader()
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([runway_id, length, status, ''])

def update_runway_status(runway_id, status):
    path = os.path.join(DB_PATH, "runways.csv")
    runways = get_all_runways()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['runway_id', 'length', 'status', 'manual_override'])
        writer.writeheader()
        for runway in runways:
            if runway['runway_id'] == runway_id:
                runway['status'] = status
            writer.writerow(runway)

# ===================== GATES =====================
def get_all_gates():
    gates = []
    path = os.path.join(DB_PATH, "gates.csv")
    if not os.path.exists(path):
        return []
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gates.append(row)
    return gates

def add_gate(gate_id, terminal, status="Available"):
    path = os.path.join(DB_PATH, "gates.csv")
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['gate_id', 'terminal', 'status', 'manual_override'])
            writer.writeheader()
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([gate_id, terminal, status, ''])

def update_gate_status(gate_id, status):
    path = os.path.join(DB_PATH, "gates.csv")
    gates = get_all_gates()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['gate_id', 'terminal', 'status', 'manual_override'])
        writer.writeheader()
        for gate in gates:
            if gate['gate_id'] == gate_id:
                gate['status'] = status
            writer.writerow(gate)


def reset_simulation_data():
    # Reset all flights to scheduled state
    flights = get_all_flights()
    flight_path = os.path.join(DB_PATH, "flights.csv")
    with open(flight_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FLIGHT_FIELDS)
        writer.writeheader()
        for flight in flights:
            writer.writerow({
                'flight_id': flight['flight_id'],
                'airline': flight.get('airline', flight.get('airline_id', '')),
                'origin': flight.get('origin', ''),
                'destination': flight.get('destination', ''),
                'departure_time': flight.get('departure_time', ''),
                'arrival_time': flight.get('arrival_time', ''),
                'status': 'SCHEDULED',
                'gate': flight.get('gate', ''),
                'runway': flight.get('runway', ''),
                'flight_type': flight.get('flight_type', 'DEPARTURE'),
                'fueling_status': flight.get('fueling_status', 'PENDING'),
                'crew_assigned': flight.get('crew_assigned', ''),
                'manual_override': ''
            })

    # Reset all gate and runway statuses to available
    gate_path = os.path.join(DB_PATH, "gates.csv")
    gates = get_all_gates()
    with open(gate_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['gate_id', 'terminal', 'status', 'manual_override'])
        writer.writeheader()
        for gate in gates:
            writer.writerow({
                'gate_id': gate['gate_id'],
                'terminal': gate['terminal'],
                'status': 'AVAILABLE',
                'manual_override': ''
            })

    runway_path = os.path.join(DB_PATH, "runways.csv")
    runways = get_all_runways()
    with open(runway_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['runway_id', 'length', 'status', 'manual_override'])
        writer.writeheader()
        for runway in runways:
            writer.writerow({
                'runway_id': runway['runway_id'],
                'length': runway.get('length', ''),
                'status': 'AVAILABLE',
                'manual_override': ''
            })

# ===================== AUTO CHECK-IN =====================
def auto_checkin_passengers(flight_id, percentage=50):
    """Automatically check-in a percentage of passengers for a flight."""
    import random
    passengers = get_passengers_by_flight(flight_id)
    num_to_checkin = max(1, int(len(passengers) * percentage / 100))
    passengers_to_checkin = random.sample(passengers, min(num_to_checkin, len(passengers)))
    
    for passenger in passengers_to_checkin:
        baggage = random.randint(5, 25)
        update_passenger_checkin(passenger['passenger_id'], "Yes", str(baggage))

def get_checkin_percentage(flight_id):
    """Get the percentage of passengers checked in for a flight."""
    passengers = get_passengers_by_flight(flight_id)
    if not passengers:
        return 0
    checked_in = sum(1 for p in passengers if p.get('checked_in', '').strip().lower() == 'yes')
    return int(checked_in * 100 / len(passengers))

# ===================== FUELING =====================
def update_fueling_status(flight_id, status):
    """Update fueling status for a flight."""
    update_flight_fields(flight_id, fueling_status=status)

def get_fueling_status(flight_id):
    """Get fueling status for a flight."""
    flights = get_all_flights()
    for flight in flights:
        if flight['flight_id'] == flight_id:
            return flight.get('fueling_status', 'PENDING')
    return None

# ===================== MANUAL OVERRIDE =====================
def set_gate_override(gate_id, override_status):
    """Set manual override for a gate (CLOSED/AVAILABLE)."""
    path = os.path.join(DB_PATH, "gates.csv")
    gates = get_all_gates()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['gate_id', 'terminal', 'status', 'manual_override'])
        writer.writeheader()
        for gate in gates:
            if gate['gate_id'] == gate_id:
                gate_row = {
                    'gate_id': gate['gate_id'],
                    'terminal': gate['terminal'],
                    'status': gate.get('status', 'AVAILABLE'),
                    'manual_override': override_status
                }
            else:
                gate_row = {
                    'gate_id': gate['gate_id'],
                    'terminal': gate['terminal'],
                    'status': gate.get('status', 'AVAILABLE'),
                    'manual_override': gate.get('manual_override', '')
                }
            writer.writerow(gate_row)

def set_runway_override(runway_id, override_status):
    """Set manual override for a runway (CLOSED/AVAILABLE)."""
    path = os.path.join(DB_PATH, "runways.csv")
    runways = get_all_runways()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['runway_id', 'length', 'status', 'manual_override'])
        writer.writeheader()
        for runway in runways:
            if runway['runway_id'] == runway_id:
                runway_row = {
                    'runway_id': runway['runway_id'],
                    'length': runway.get('length', ''),
                    'status': runway.get('status', 'AVAILABLE'),
                    'manual_override': override_status
                }
            else:
                runway_row = {
                    'runway_id': runway['runway_id'],
                    'length': runway.get('length', ''),
                    'status': runway.get('status', 'AVAILABLE'),
                    'manual_override': runway.get('manual_override', '')
                }
            writer.writerow(runway_row)

def get_gate_override(gate_id):
    """Get manual override status for a gate."""
    gates = get_all_gates()
    for gate in gates:
        if gate['gate_id'] == gate_id:
            return gate.get('manual_override', '')
    return ''

def get_runway_override(runway_id):
    """Get manual override status for a runway."""
    runways = get_all_runways()
    for runway in runways:
        if runway['runway_id'] == runway_id:
            return runway.get('manual_override', '')
    return ''
