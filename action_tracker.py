import threading
from time import perf_counter_ns

class ActionTrackerPost:
    # this implementation is meant to show post processing of action data, average will be calculated on call of
    # get_stats().  Not ideal as full computational load is during one call.
    def __init__(self):
        self.lock = threading.Lock()
        self.actions = {}

    def add_action(self, json_action):
        # Attempts to parse the input string, appends ("action", time) to actions] if successful
        # time_start = perf_counter_ns()

        # Due to concurrency concerns, set a lock to prevent race conditions
        # print("Awaiting lock")
        self.lock.acquire()

        try:
            # print("Lock Acquired")
            # Typical input format is already in the form of a python dict, no need to use json module to parse
            action = json_action["action"]
            time = json_action["time"]


            if action in self.actions.keys():
                # if this action type exists in the "actions" dict, append this new time to the existing list of times
                # associated with that unique action

                act_list = self.actions[action]
                act_list.append(time)
                self.actions[action] = act_list
            else:
                self.actions[action] = [time]

            # print(self.actions)

        # TODO handle specific exceptions rather than a catch-all
        except:
            raise ValueError("JSON improperly formatted or missing keys, please check input format")

        finally:
            self.lock.release()

            # print("Lock released")
            # time_stop = perf_counter_ns()
            # print(time_stop - time_start)

    # def get_stats(self):
    #     # compute the average time of each unique "action"












