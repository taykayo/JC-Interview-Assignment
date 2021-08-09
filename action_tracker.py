import threading


class ActionTrackerPost:
    # This implementation is meant to show post processing of action data. Each action "event" is stored and so
    # this class is extensible to provide other measurements as desired. However, averaging is calculated on call of
    # get_stats() only.  No computation is done on add_action call, therefore get_stats will take longer to process
    # dependent upon how many actions have been added.  More add_action calls = more values to summate.

    def __init__(self):
        # Each instance gets their own Lock object
        self.lock = threading.Lock()
        self.actions = {}

    def add_action(self, json_action):
        # Due to concurrency concerns, set a lock to prevent race conditions
        self.lock.acquire()

        try:
            # Typical input format is already in the form of a python dict, no need to use json module to parse

            action = json_action["action"]
            time = json_action["time"]

            # General error handling
            if not isinstance(action, str):
                raise ValueError("Action value must be a string")
            if not action:
                # if action was an empty string
                raise ValueError("Action value cannot be empty")

            if not isinstance(time, int):
                raise ValueError("Time value must be a integer")
            if time < 0:
                # if time is negative
                raise ValueError("Time cannot be negative!!!")

            if action in self.actions.keys():
                # if this action type exists in the "actions" dict, append this new time to the existing list of times
                # associated with that unique action

                time_list = self.actions[action]
                time_list.append(time)
                self.actions[action] = time_list

            else:
                # If action does not have  a key within the actions dict already, create it

                self.actions[action] = [time]

        # So long as the inputs are valid, exceptions should not occur. This generic raise will re-raise any prior
        # exceptions, so will not overwrite custom ones, and will allow for unexpected exceptions to be raised.
        except:
            raise

        finally:
            self.lock.release()

    def get_stats(self):
        # compute the average time of each unique "action"

        avg_list = []
        # Due to concurrency concerns, set a lock to prevent race conditions. Less important here as no data is being
        # saved, but this still ensures action data is added while calculations are being run
        self.lock.acquire()

        try:
            if self.actions:
                # if dict is not empty (empty dicts return false)

                for key in self.actions.keys():
                    # calculate average for each unique key in actions dict
                    avg_list.append({"action": key, "avg": (sum(self.actions[key])/len(self.actions[key]))})

        finally:
            self.lock.release()
        return avg_list


class ActionTrackerRunning:
    # This implementation does not store each action "event", but rather keeps a running sum of the time values
    # associated with each unique action, along with how many times that unique action has been added.
    # The downside is that this is solely useful for calculating the average, and so other metrics cannot be added.
    # While the :add_action" is marginally slower than the post-processing implementation, the "get_stats" function here
    # performs significantly better, as only one calculation is being done per unique action.

    def __init__(self):
        # Each instance gets their own Lock object
        self.lock = threading.Lock()

        # Actions dict will be in format of {'action'= [(cumulative sum of time for this specific action key), (number
        # of times this key has appeared)]
        self.actions = {}

    def add_action(self, json_action):
        # Due to concurrency concerns, set a lock to prevent race conditions
        self.lock.acquire()

        try:
            # Typical input format is already in the form of a python dict, no need to use json module to parse

            action = json_action["action"]
            time = json_action["time"]

            # General error handling
            if not isinstance(action, str):
                raise ValueError("Action value must be a string")
            if not action:
                # if action was an empty string
                raise ValueError("Action value cannot be empty")

            if not isinstance(time, int):
                raise ValueError("Time value must be an integer")
            if time < 0:
                # if time is negative
                raise ValueError("Time cannot be negative!!!")

            if action in self.actions.keys():
                # if this action type exists in the "actions" dict, increment the counter for that key, and add the new
                # time value to the running sum for that key

                time_sum = self.actions[action][0]
                time_sum += time

                action_count = self.actions[action][1]
                action_count += 1

                self.actions[action] = [time_sum, action_count]

            else:
                # If action does not have a key in the actions dict, create one.

                self.actions[action] = [time, 1]

        # So long as the inputs are valid, exceptions should not occur. This generic raise will re-raise any prior
        # exceptions, so will not overwrite custom ones, and will allow for unexpected exceptions to be raised.
        except:
            raise

        finally:
            self.lock.release()

    def get_stats(self):
        # compute the average time of each unique "action"

        avg_list = []

        # Due to concurrency concerns, set a lock to prevent race conditions. Less important here as no data is being
        # saved, but this still ensures action data is added while calculations are being run
        self.lock.acquire()

        try:
            if self.actions:
                for key in self.actions.keys():
                    # calculate average for each unique key in actions dict
                    avg_list.append({"action": key, "avg": self.actions[key][0]/self.actions[key][1]})

        finally:
            self.lock.release()
        return avg_list
