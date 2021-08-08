import threading


class ActionTrackerPost:
    # This implementation is meant to show post processing of action data. Each action "event" is stored and so
    # this class is extensible to provide other measurements as desired. However, averaging is calculated on call of
    # get_stats() only.  No computation is done on add_action call, therefore get_stats will take longer to process
    # dependent upon how many actions have been added.

    def __init__(self):
        self.lock = threading.Lock()
        self.actions = {}

    def add_action(self, json_action):
        # Attempts to parse the input string, appends ("action", time) to actions] if successful
        # time_start = perf_counter_ns()

        # Due to concurrency concerns, set a lock to prevent race conditions

        self.lock.acquire()

        try:

            # Typical input format is already in the form of a python dict, no need to use json module to parse
            action = json_action["action"]
            time = json_action["time"]

            if action in self.actions.keys():
                # if this action type exists in the "actions" dict, append this new time to the existing list of times
                # associated with that unique action

                time_list = self.actions[action]
                time_list.append(time)
                self.actions[action] = time_list
            else:
                self.actions[action] = [time]

        # TODO handle specific exceptions rather than a catch-all
        except:
            raise ValueError("JSON improperly formatted or missing keys, please check input format")

        finally:
            self.lock.release()

    def get_stats(self):
        # compute the average time of each unique "action"

        avg_dict = {}
        self.lock.acquire()

        try:
            if self.actions:
                for _ in self.actions.keys():
                    avg_dict[_] = (sum(self.actions[_])/len(self.actions[_]))

        finally:
            self.lock.release()
        return avg_dict


class ActionTrackerRunning:
    # This implementation does not store each action "event", but rather keeps a running sum of the time values
    # associated with each unique action, along with how many times that unique action has been added.
    # The downside is that this is solely useful for calculating the average, and so other metrics cannot be added.
    # While the :add_action" is marginally slower than the post-processing implementation, the "get_stats" function here
    # performs significantly better, as only one calculation is being done per unique action.

    def __init__(self):
        self.lock = threading.Lock()
        self.actions = {}

    def add_action(self, json_action):
        # Attempts to parse the input string, appends ("action", time) to actions] if successful
        # time_start = perf_counter_ns()

        # Due to concurrency concerns, set a lock to prevent race conditions

        self.lock.acquire()

        try:

            # Typical input format is already in the form of a python dict, no need to use json module to parse
            action = json_action["action"]
            time = json_action["time"]

            if action in self.actions.keys():
                # if this action type exists in the "actions" dict, append this new time to the existing list of times
                # associated with that unique action

                time_sum = self.actions[action][0]
                time_sum += time
                action_count = self.actions[action][1]
                action_count += 1
                self.actions[action] = [time_sum, action_count]
            else:
                self.actions[action] = [time, 1]

        # TODO handle specific exceptions rather than a catch-all
        except:
            raise ValueError("JSON improperly formatted or missing keys, please check input format")

        finally:
            self.lock.release()

    def get_stats(self):
        # compute the average time of each unique "action"

        avg_dict = {}
        self.lock.acquire()

        try:
            if self.actions:
                for x in self.actions.keys():

                    avg_dict[x] = self.actions[x][0]/self.actions[x][1]

        finally:
            self.lock.release()
        return avg_dict
