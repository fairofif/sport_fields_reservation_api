from datetime import datetime

def check_schedule_conflict(time_start, time_end, time_start_compare, time_end_compare):
    # Convert string times to datetime objects
    start = datetime.strptime(time_start, '%H:%M:%S')
    end = datetime.strptime(time_end, '%H:%M:%S')
    start_compare = datetime.strptime(time_start_compare, '%H:%M:%S')
    end_compare = datetime.strptime(time_end_compare, '%H:%M:%S')

    # Check for conflicts
    if (start <= start_compare and end >= start_compare) or \
       (start <= end_compare and end >= end_compare) or \
       (start >= start_compare and end <= end_compare):
        return True  # Conflict exists
    else:
        return False  # No conflict

# Test cases
test_cases = [
    ('08:00:00', '13:59:59', '11:00:00', '15:59:59'),  # Case 1 -> True
    ('12:00:00', '13:59:59', '11:00:00', '15:59:59'),  # Case 2 -> True
    ('12:00:00', '16:59:59', '11:00:00', '15:59:59'),  # Case 3 -> True
    ('08:00:00', '16:59:59', '11:00:00', '15:59:59'),  # Case 4 -> True
    ('08:00:00', '09:59:59', '11:00:00', '15:59:59'),  # Case 5 -> False
    ('16:00:00', '18:59:59', '11:00:00', '15:59:59')   # Case 6 -> False
]

for time_start, time_end, time_start_compare, time_end_compare in test_cases:
    conflict = check_schedule_conflict(time_start, time_end, time_start_compare, time_end_compare)
    print(f"For times: {time_start} to {time_end} compared to {time_start_compare} to {time_end_compare}, Conflict? {conflict}")

from datetime import datetime

def check_schedule_in_range(time_start, time_end, time_open, time_closed):
    # Convert string times to datetime objects
    start = datetime.strptime(time_start, '%H:%M:%S').time()
    end = datetime.strptime(time_end, '%H:%M:%S').time()
    open_time = datetime.strptime(time_open, '%H:%M:%S').time()
    closed_time = datetime.strptime(time_closed, '%H:%M:%S').time()

    # Check if the schedule is within the open and closed times
    if start < open_time or end > closed_time:
        return True  # Schedule is out of range
    else:
        return False  # Schedule is within range

# Test cases
test_cases = [
    ('07:00:00', '10:59:59', '08:00:00', '12:00:00'),  # True
    ('08:00:00', '10:59:59', '08:00:00', '12:00:00'),  # False
    ('08:00:00', '13:59:59', '08:00:00', '12:00:00'),  # True
    ('07:00:00', '15:59:59', '08:00:00', '12:00:00'),  # True
    ('13:00:00', '16:59:59', '08:00:00', '12:00:00')   # True
]

for time_start, time_end, time_open, time_closed in test_cases:
    out_of_range = check_schedule_in_range(time_start, time_end, time_open, time_closed)
    print(f"For times: {time_start} to {time_end} compared to open time: {time_open} and closed time: {time_closed}, Out of range? {out_of_range}")
