import sys
sys.path.append(r'c:\Users\PrabhuDevarajan\Desktop\LOCAL\SEM_2\Python\Project\AirportManagement')

def calculate_progress(current_time_str, dep, arr, status):
    if status in ["SCHEDULED", "CHECK-IN OPEN", "BOARDING", "GATE CLOSED", "CANCELLED"]:
        return 0.0
    if status == "ARRIVED":
        return 1.0

    def _parse_time(t_str):
        h, m = map(int, t_str.split(':'))
        return h * 60 + m

    c_mins = _parse_time(current_time_str)
    d_mins = _parse_time(dep)
    a_mins = _parse_time(arr)

    if a_mins > d_mins:
        # Same-day flight
        if c_mins <= d_mins:
            return 0.0
        elif c_mins >= a_mins:
            return 1.0
        else:
            return (c_mins - d_mins) / (a_mins - d_mins)
    else:
        # Overnight flight
        total_duration = (24 * 60 - d_mins) + a_mins
        if c_mins >= d_mins:
            return (c_mins - d_mins) / total_duration
        elif c_mins <= a_mins:
            return ((24 * 60 - d_mins) + c_mins) / total_duration
        else:
            return 1.0 if c_mins < d_mins and c_mins > a_mins else 0.0

# Run tests
# Case 1: Same day flight (08:30 -> 15:00)
# Before departure (04:05) -> should be 0.0
assert calculate_progress("04:05", "08:30", "15:00", "SCHEDULED") == 0.0, "Failed Case 1.1"
# During flight (10:00) -> should be (600 - 510) / (900 - 510) = 90 / 390 = 23%
p1 = calculate_progress("10:00", "08:30", "15:00", "IN AIR")
assert abs(p1 - 0.2307) < 0.001, f"Failed Case 1.2: {p1}"
# After arrival (16:00) -> should be 1.0
assert calculate_progress("16:00", "08:30", "15:00", "ARRIVED") == 1.0, "Failed Case 1.3"

# Case 2: Overnight flight (23:00 -> 02:00)
# Before departure (20:00) -> should be 0.0
assert calculate_progress("20:00", "23:00", "02:00", "SCHEDULED") == 0.0, "Failed Case 2.1"
# During flight before midnight (23:30) -> total duration = 180 mins. elapsed = 30 mins. progress = 30 / 180 = 16.7%
p2 = calculate_progress("23:30", "23:00", "02:00", "IN AIR")
assert abs(p2 - 0.1667) < 0.001, f"Failed Case 2.2: {p2}"
# During flight after midnight (01:00) -> elapsed = 60 + 60 = 120 mins. progress = 120 / 180 = 66.7%
p3 = calculate_progress("01:00", "23:00", "02:00", "IN AIR")
assert abs(p3 - 0.6667) < 0.001, f"Failed Case 2.3: {p3}"
# After arrival (04:00) -> should be 1.0
assert calculate_progress("04:00", "23:00", "02:00", "ARRIVED") == 1.0, "Failed Case 2.4"

print("All progress calculation assertion checks passed successfully!")
