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

# ===================== FLIGHTS =====================
def get_all_flights():
    flights = []
    path = os.path.join(DB_PATH, "flights.csv")
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            flights.append(row)
    return flights

def add_flight(flight_id, airline_id, origin, destination, departure, arrival, gate, runway):
    path = os.path.join(DB_PATH, "flights.csv")
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([flight_id, airline_id, origin, destination, departure, arrival, gate, runway, "On Schedule"])

def update_flight_status(flight_id, status):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['flight_id', 'airline_id', 'origin', 'destination', 'departure', 'arrival', 'gate', 'runway', 'status'])
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] == flight_id:
                flight['status'] = status
            writer.writerow(flight)

def update_flight(flight_id, new_flight_id, airline_id, origin, destination, departure, arrival, gate, runway, status):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['flight_id', 'airline_id', 'origin', 'destination', 'departure', 'arrival', 'gate', 'runway', 'status'])
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] == flight_id:
                writer.writerow({'flight_id': new_flight_id, 'airline_id': airline_id, 'origin': origin, 'destination': destination, 'departure': departure, 'arrival': arrival, 'gate': gate, 'runway': runway, 'status': status})
            else:
                writer.writerow(flight)

def delete_flight(flight_id):
    path = os.path.join(DB_PATH, "flights.csv")
    flights = get_all_flights()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['flight_id', 'airline_id', 'origin', 'destination', 'departure', 'arrival', 'gate', 'runway', 'status'])
        writer.writeheader()
        for flight in flights:
            if flight['flight_id'] != flight_id:
                writer.writerow(flight)

def get_flights_by_airline(airline_id):
    flights = []
    all_flights = get_all_flights()
    for flight in all_flights:
        if flight.get('airline_id') == airline_id:
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
            writer = csv.DictWriter(f, fieldnames=['runway_id', 'length', 'status'])
            writer.writeheader()
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([runway_id, length, status])

def update_runway_status(runway_id, status):
    path = os.path.join(DB_PATH, "runways.csv")
    runways = get_all_runways()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['runway_id', 'length', 'status'])
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
            writer = csv.DictWriter(f, fieldnames=['gate_id', 'terminal', 'status'])
            writer.writeheader()
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([gate_id, terminal, status])

def update_gate_status(gate_id, status):
    path = os.path.join(DB_PATH, "gates.csv")
    gates = get_all_gates()
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['gate_id', 'terminal', 'status'])
        writer.writeheader()
        for gate in gates:
            if gate['gate_id'] == gate_id:
                gate['status'] = status
            writer.writerow(gate)
