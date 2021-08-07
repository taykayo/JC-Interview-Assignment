import random
from action_tracker import ActionTrackerPost


if __name__ == '__main__':
    Action_Tracker = ActionTrackerPost()
    Action_Tracker.add_action({"action":"jump", "time":100})
    for i in range(1000000):

        Action_Tracker.add_action({'action': 'jump', 'time': random.randint(0, 5000)})






