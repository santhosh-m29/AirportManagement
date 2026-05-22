#!/usr/bin/env python3
"""
Script to populate the Airport Management database with comprehensive data.
"""

import os
import csv
from datetime import datetime, timedelta
import random
from airport_settings import get_airport

DB_PATH = os.path.join(os.path.dirname(__file__), "database")

# Comprehensive data lists
AIRLINES = [
    ("AIR001", "Emirates"),
    ("AIR002", "Qatar Airways"),
    ("AIR003", "Singapore Airlines"),
    ("AIR004", "AirAsia"),
    ("AIR005", "Etihad"),
    ("AIR006", "IndiGo"),
    ("AIR007", "SpiceJet"),
    ("AIR008", "Air India"),
    ("AIR009", "Lufthansa"),
    ("AIR010", "British Airways"),
]

FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles",
    "Joseph", "Thomas", "Daniel", "Paul", "Edward", "Steven", "Andrew", "Kenneth",
    "George", "Henry", "Arthur", "Frank", "Jennifer", "Mary", "Patricia", "Linda",
    "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy",
    "Betty", "Margaret", "Sandra", "Ashley", "Kimberly", "Emily", "Donna", "Michelle"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
    "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee",
    "Walker", "Hall", "Young", "Hernandez", "King", "Lopez", "Scott", "Green"
]

CREW_ROLES = ["Captain", "First Officer", "Flight Attendant"]

AIRPORTS = ["Dubai", "Paris", "London", "New York", "Sydney", "Bangkok", "Manila", 
            "Singapore", "Chennai", "Doha", "Abu Dhabi", "Tokyo", "Hong Kong", "Mumbai",
            "Delhi", "Frankfurt", "Amsterdam", "Madrid", "Rome", "Istanbul"]

CITIES = ["Dubai", "Paris", "London", "New York", "Sydney", "Bangkok", "Manila", 
          "Singapore", "Doha", "Abu Dhabi", "Tokyo", "Hong Kong", "Mumbai",
          "Delhi", "Frankfurt", "Amsterdam", "Madrid", "Rome", "Istanbul"]

GATES = [
    ("A1", "Terminal 1"), ("A2", "Terminal 1"),
    ("B1", "Terminal 2"), ("B2", "Terminal 2"),
    ("C1", "Terminal 3"), ("C2", "Terminal 3"),
    ("D1", "Terminal 4"), ("D2", "Terminal 4"),
]

RUNWAYS = [
    ("R1", "4000"),
    ("R2", "3500"),
]

def create_crew_csv():
    """Populate crew.csv with many crew members across all airlines."""
    path = os.path.join(DB_PATH, "crew.csv")
    
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['crew_id', 'name', 'role', 'airline_id', 'last_flight', 'rest_until'])
        writer.writeheader()
        
        crew_id = 1
        for airline_id, _ in AIRLINES:
            # Create 2 crew members per airline
            for _ in range(2):
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                role = random.choice(CREW_ROLES)
                
                writer.writerow({
                    'crew_id': f"CREW{crew_id:04d}",
                    'name': f"{first_name} {last_name}",
                    'role': role,
                    'airline_id': airline_id,
                    'last_flight': '',
                    'rest_until': ''
                })
                crew_id += 1

def create_flights_csv():
    """Populate flights.csv."""
    path = os.path.join(DB_PATH, "flights.csv")
    
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['flight_id', 'airline', 'origin', 'destination', 
                                               'departure_time', 'arrival_time', 'status', 'gate', 'runway', 
                                               'flight_type', 'fueling_status', 'crew_assigned', 'manual_override'])
        writer.writeheader()
        
        flight_id = 1
        
        # Base schedule starting from 06:00
        start_time = datetime.strptime("06:00", "%H:%M")
        
        # 1. DEPARTURE FLIGHTS
        for airline_id, _ in AIRLINES:
            # Create 3 departing flights per airline (approx 30 total)
            for i in range(3):
                dep_time = start_time + timedelta(minutes=random.randint(30, 480) + (i * 120))
                arr_time = dep_time + timedelta(minutes=random.randint(60, 300))
                
                writer.writerow({
                    'flight_id': f"FL{flight_id:04d}",
                    'airline': airline_id,
                    'origin': get_airport(),
                    'destination': random.choice(CITIES),
                    'departure_time': dep_time.strftime("%H:%M"),
                    'arrival_time': arr_time.strftime("%H:%M"),
                    'status': 'SCHEDULED',
                    'gate': '',
                    'runway': '',
                    'flight_type': 'DEPARTURE',
                    'fueling_status': 'PENDING',
                    'crew_assigned': '',
                    'manual_override': ''
                })
                flight_id += 1
                
        # 2. ARRIVAL FLIGHTS
        for airline_id, _ in AIRLINES:
            # Create 1 arriving flight per airline (approx 10 total)
            for i in range(1):
                arr_time = start_time + timedelta(minutes=random.randint(60, 600))
                dep_time = arr_time - timedelta(minutes=random.randint(60, 300))
                
                writer.writerow({
                    'flight_id': f"FL{flight_id:04d}",
                    'airline': airline_id,
                    'origin': random.choice([c for c in CITIES if c != get_airport()]),
                    'destination': get_airport(),
                    'departure_time': dep_time.strftime("%H:%M"),
                    'arrival_time': arr_time.strftime("%H:%M"),
                    'status': 'SCHEDULED',
                    'gate': '',
                    'runway': '',
                    'flight_type': 'ARRIVAL',
                    'fueling_status': 'PENDING',
                    'crew_assigned': '',
                    'manual_override': ''
                })
                flight_id += 1

def create_passengers_csv():
    """Populate passengers.csv with 10 passengers per flight."""
    flights = []
    path = os.path.join(DB_PATH, "flights.csv")
    
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            flights.append(row)
    
    pass_path = os.path.join(DB_PATH, "passengers.csv")
    
    with open(pass_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['passenger_id', 'name', 'flight_id', 'seat', 'checked_in', 'baggage_weight'])
        writer.writeheader()
        
        passenger_id = 1
        seat_assignments = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'D1', 'D2', 'D3', 'D4', 'E1', 'E2']
        
        for flight in flights:
            # 10 passengers per flight
            for i in range(10):
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                seat = f"{i+1}{seat_assignments[i % len(seat_assignments)]}"
                
                writer.writerow({
                    'passenger_id': f"PASS{passenger_id:05d}",
                    'name': f"{first_name} {last_name}",
                    'flight_id': flight['flight_id'],
                    'seat': seat,
                    'checked_in': 'No',
                    'baggage_weight': '0'
                })
                passenger_id += 1

def create_gates_csv():
    """Populate gates.csv."""
    path = os.path.join(DB_PATH, "gates.csv")
    
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['gate_id', 'terminal', 'status', 'manual_override'])
        writer.writeheader()
        
        for gate_id, terminal in GATES:
            writer.writerow({
                'gate_id': gate_id,
                'terminal': terminal,
                'status': 'AVAILABLE',
                'manual_override': ''
            })

def create_runways_csv():
    """Populate runways.csv."""
    path = os.path.join(DB_PATH, "runways.csv")
    
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['runway_id', 'length', 'status', 'manual_override'])
        writer.writeheader()
        
        for runway_id, length in RUNWAYS:
            writer.writerow({
                'runway_id': runway_id,
                'length': length,
                'status': 'AVAILABLE',
                'manual_override': ''
            })

def create_airlines_csv():
    """Populate airlines.csv."""
    path = os.path.join(DB_PATH, "airlines.csv")
    
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['airline_id', 'name', 'flights'])
        writer.writeheader()
        
        for airline_id, name in AIRLINES:
            writer.writerow({
                'airline_id': airline_id,
                'name': name,
                'flights': '0'
            })

def populate_all():
    """Populate all databases."""
    print("Populating Airlines...")
    create_airlines_csv()
    
    print("Populating Crew...")
    create_crew_csv()
    
    print("Populating Flights...")
    create_flights_csv()
    
    print("Populating Gates...")
    create_gates_csv()
    
    print("Populating Runways...")
    create_runways_csv()
    
    print("Populating Passengers...")
    create_passengers_csv()
    
    print("Database population complete!")

if __name__ == "__main__":
    populate_all()
