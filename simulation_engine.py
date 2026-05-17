from datetime import datetime, timedelta

SIM_TIME = datetime(2026, 1, 1, 6, 0, 0)
TIME_SPEED = 5  # 1 real second = 5 simulated minutes
running = False


def get_sim_time():
    """Return the current simulated datetime."""
    return SIM_TIME


def tick():
    """Advance the simulation time by TIME_SPEED minutes."""
    global SIM_TIME
    SIM_TIME += timedelta(minutes=TIME_SPEED)
    return SIM_TIME


def update_simulation(root):
    """Advance the simulation clock and re-schedule this update."""
    tick()

    from scheduler import process_scheduled_events, process_flights
    process_scheduled_events(SIM_TIME)
    process_flights()

    root.after(1000, lambda: update_simulation(root))


def start():
    global running
    running = True


def stop():
    global running
    running = False


def set_sim_time(new_time: datetime):
    global SIM_TIME
    SIM_TIME = new_time
    return SIM_TIME


def get_time_speed():
    return TIME_SPEED


def set_time_speed(minutes_per_second: int):
    global TIME_SPEED
    TIME_SPEED = minutes_per_second
    return TIME_SPEED


def reset(start_time: datetime | None = None):
    global SIM_TIME
    SIM_TIME = start_time or datetime(2026, 1, 1, 6, 0, 0)
