"""Scheduler and flight status engine for the airport simulation."""

import random
from datetime import datetime, timedelta

import simulation_engine
from db_utils import get_all_flights, update_flight_status, update_gate_status, update_runway_status, reschedule_flight, update_flight_fields, get_all_runways

scheduled_events = []


def _time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes


def _subtract_minutes(time_str, minutes):
    hours, mins = map(int, time_str.split(':'))
    total = hours * 60 + mins - minutes
    total %= 24 * 60
    return f"{total // 60:02d}:{total % 60:02d}"


def _add_minutes(time_str, minutes):
    hours, mins = map(int, time_str.split(':'))
    dt = datetime(2026, 1, 1, hours, mins) + timedelta(minutes=minutes)
    return f"{dt.hour:02d}:{dt.minute:02d}"


def _should_delay():
    return random.randint(1, 10) == 1


def _release_resources(gate_id, runway_id):
    if gate_id:
        update_gate_status(gate_id, "AVAILABLE")
    if runway_id:
        update_runway_status(runway_id, "AVAILABLE")


def _occupy_gate(gate_id):
    if gate_id:
        update_gate_status(gate_id, "OCCUPIED")


def _release_gate(gate_id):
    if gate_id:
        update_gate_status(gate_id, "AVAILABLE")


def _occupy_runway(runway_id, flight_id):
    """Occupy runway and schedule release 15 minutes after departure."""
    if runway_id:
        update_runway_status(runway_id, "OCCUPIED")
        flight = next((f for f in get_all_flights() if f['flight_id'] == flight_id), None)
        if flight:
            departure = flight.get('departure_time') or flight.get('departure')
            if departure:
                # Release runway 15 minutes after departure
                release_time = _add_minutes(departure, 15)
                # Schedule the release event
                release_dt = datetime(2026, 1, 1, int(release_time.split(':')[0]), int(release_time.split(':')[1]))
                current_dt = simulation_engine.SIM_TIME
                if release_dt <= current_dt:
                    release_dt += timedelta(days=1)
                schedule_event(release_dt, _release_runway, runway_id)


def _release_runway(runway_id):
    if runway_id:
        update_runway_status(runway_id, "AVAILABLE")


def _get_available_runways():
    runways = get_all_runways()
    return [r['runway_id'] for r in runways if r.get('status', '').strip().lower() == 'available']


def _assign_runway(flight):
    """Assign an available runway to a flight, avoiding conflicts."""
    departure = flight.get('departure_time') or flight.get('departure')
    if not departure:
        return None

    # Get all flights with the same departure time that already have runways
    same_dep_runways = [f.get('runway') for f in get_all_flights()
                        if f['flight_id'] != flight['flight_id'] and
                        (f.get('departure_time') or f.get('departure')) == departure and
                        f.get('runway')]

    # Find available runways that don't conflict
    available = [r for r in _get_available_runways() if r not in same_dep_runways]
    if available:
        assigned = available[0]
        update_flight_fields(flight['flight_id'], runway=assigned)
        return assigned

    # Fallback: use any available runway
    fallback = _get_available_runways()
    if fallback:
        assigned = fallback[0]
        update_flight_fields(flight['flight_id'], runway=assigned)
        return assigned

    # Ultimate Fallback: use absolutely any runway in the system
    all_runways = get_all_runways()
    if all_runways:
        # Prioritize runways that don't conflict with same departure time
        non_conflict = [r['runway_id'] for r in all_runways if r['runway_id'] not in same_dep_runways]
        if non_conflict:
            assigned = non_conflict[0]
        else:
            assigned = all_runways[0]['runway_id']
        update_flight_fields(flight['flight_id'], runway=assigned)
        return assigned

    return None


def schedule_event(event_time: datetime, callback, *args, **kwargs):
    scheduled_events.append({
        'time': event_time,
        'callback': callback,
        'args': args,
        'kwargs': kwargs
    })
    scheduled_events.sort(key=lambda e: e['time'])


def process_scheduled_events(current_time: datetime):
    due = [event for event in scheduled_events if event['time'] <= current_time]
    for event in due:
        try:
            event['callback'](*event['args'], **event['kwargs'])
        except Exception:
            pass
        scheduled_events.remove(event)


def process_flights():
    flights = get_all_flights()
    current = simulation_engine.SIM_TIME.strftime("%H:%M")

    for flight in flights:
        departure = flight.get("departure_time") or flight.get("departure")
        arrival = flight.get("arrival_time") or flight.get("arrival")
        status = flight.get("status", "")

        if not departure or not arrival:
            continue

        # Automatically allocate a runway if it is missing
        if not flight.get("runway"):
            assigned_runway = _assign_runway(flight)
            if assigned_runway:
                flight["runway"] = assigned_runway

        if status == "ARRIVED":
            continue

        check_in_open = _subtract_minutes(departure, 120)
        boarding = _subtract_minutes(departure, 30)
        gate_closed = _subtract_minutes(departure, 10)
        taxiing = _subtract_minutes(departure, 5)

        if current == check_in_open:
            if status != "DELAYED" and _should_delay():
                new_departure = _add_minutes(departure, 15)
                new_arrival = _add_minutes(arrival, 15)
                reschedule_flight(flight["flight_id"], new_departure, new_arrival, status="DELAYED")
                continue
            update_flight_status(flight["flight_id"], "CHECK-IN OPEN")
            if flight.get("gate"):
                _occupy_gate(flight.get("gate"))
            continue

        if current == boarding:
            if status != "DELAYED" and _should_delay():
                new_departure = _add_minutes(departure, 15)
                new_arrival = _add_minutes(arrival, 15)
                reschedule_flight(flight["flight_id"], new_departure, new_arrival, status="DELAYED")
                continue
            update_flight_status(flight["flight_id"], "BOARDING")
            if flight.get("gate"):
                _occupy_gate(flight.get("gate"))
            continue

        if current == gate_closed:
            update_flight_status(flight["flight_id"], "GATE CLOSED")
            continue

        if current == taxiing:
            assigned_runway = _assign_runway(flight)
            if assigned_runway:
                update_flight_fields(flight["flight_id"], runway=assigned_runway)
            if flight.get("gate"):
                _release_gate(flight.get("gate"))
            update_flight_status(flight["flight_id"], "TAXIING")
            if assigned_runway:
                _occupy_runway(assigned_runway, flight["flight_id"])
            continue

        if current == departure:
            update_flight_status(flight["flight_id"], "DEPARTED")
            continue

        if _time_to_minutes(departure) < _time_to_minutes(current) < _time_to_minutes(arrival):
            if status != "IN AIR":
                update_flight_status(flight["flight_id"], "IN AIR")
            continue

        if current == arrival:
            update_flight_status(flight["flight_id"], "ARRIVED")


def get_pending_events():
    return list(scheduled_events)
