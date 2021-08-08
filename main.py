import random
from time import perf_counter_ns
from action_tracker import ActionTrackerPost, ActionTrackerRunning


if __name__ == '__main__':
    Action_Tracker = ActionTrackerPost()
    Action_Tracker2 = ActionTrackerRunning()
    Action_Tracker.add_action({'action': 'jump', 'time': 9})
    Action_Tracker2.add_action({'action': 'jump', 'time': 2147483647})
    # for i in range(100000):
    #     randnumber = random.randint(0, 5000)
    #
    #     Action_Tracker.add_action({'action': 'jump', 'time': randnumber})
    #
    #     Action_Tracker2.add_action({'action': 'jump', 'time': randnumber})
    #
    # for i in range(100000):
    #     randnumber = random.randint(0, 5000)
    #
    #     Action_Tracker.add_action({'action': 'sprint', 'time': randnumber})
    #
    #     Action_Tracker2.add_action({'action': 'sprint', 'time': randnumber})
    #
    # for i in range(100000):
    #     randnumber = random.randint(0, 5000)
    #
    #     Action_Tracker.add_action({'action': 'hop', 'time': randnumber})
    #
    #     Action_Tracker2.add_action({'action': 'hop', 'time': randnumber})
    #
    # for i in range(100000):
    #     randnumber = random.randint(0, 5000)
    #
    #     Action_Tracker.add_action({'action': 'bow', 'time': randnumber})
    #
    #     Action_Tracker2.add_action({'action': 'bow', 'time': randnumber})

    a1 =perf_counter_ns()
    print(Action_Tracker.get_stats())
    a1s = perf_counter_ns()

    a2 = perf_counter_ns()
    print(Action_Tracker2.get_stats())
    a2s = perf_counter_ns()

    print(f"Post Process of averaging took: {a1s-a1} nanoseconds")
    print(f"Running sum averaging took {a2s-a2} nanoseconds")







