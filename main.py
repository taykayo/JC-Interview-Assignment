import random
from time import perf_counter_ns
from action_tracker import ActionTrackerPost, ActionTrackerRunning


if __name__ == '__main__':
    Action_Tracker = ActionTrackerPost()
    Action_Tracker2 = ActionTrackerRunning()

    for i in range(100000):
        randnumber = random.randint(0, 5000)

        Action_Tracker.add_action({'action': 'jump', 'time': randnumber})

        Action_Tracker2.add_action({'action': 'jump', 'time': randnumber})

    for i in range(100000):
        randnumber = random.randint(0, 5000)

        Action_Tracker.add_action({'action': 'sprint', 'time': randnumber})

        Action_Tracker2.add_action({'action': 'sprint', 'time': randnumber})

    for i in range(100000):
        randnumber = random.randint(0, 5000)

        Action_Tracker.add_action({'action': 'hop', 'time': randnumber})

        Action_Tracker2.add_action({'action': 'hop', 'time': randnumber})

    for i in range(100000):
        randnumber = random.randint(0, 5000)

        Action_Tracker.add_action({'action': 'barrel roll', 'time': randnumber})

        Action_Tracker2.add_action({'action': 'barrel roll', 'time': randnumber})

    a1 = perf_counter_ns()
    print(f"ActionTrackPost Data: {Action_Tracker.get_stats()}")
    a1s = perf_counter_ns()
    print(f"ActionTrackerPost took: {a1s - a1} nanoseconds to calculate the averages.\n")

    a2 = perf_counter_ns()
    print(f"ActionTrackerRunning Data: {Action_Tracker2.get_stats()}")
    a2s = perf_counter_ns()
    print(f"ActionTrackerRunning took {a2s-a2} nanoseconds to calculate the averages.\n")
