import unittest
from action_tracker import *
import random
from time import perf_counter_ns


class TestAverages(unittest.TestCase):

    def test_averages(self):
        # Test that averages are calculating correctly, also reports timing statistics
        # TODO clean up variable names in this test, getting a bit wordy/unintuitive

        # Instantiate both objects
        action_tracker_post = ActionTrackerPost()
        action_tracker_running = ActionTrackerRunning()

        values = []
        post_times = []
        running_times = []

        # add a bunch of randomized times for action "jump", track times as well
        for i in range(100000):
            randnumber = random.randint(0, 5000)
            values.append(randnumber)

            post_start = perf_counter_ns()
            action_tracker_post.add_action({'action': 'jump', 'time': randnumber})
            post_stop = perf_counter_ns()

            running_start = perf_counter_ns()
            action_tracker_running.add_action({'action': 'jump', 'time': randnumber})
            running_stop = perf_counter_ns()

            post_times.append(post_stop-post_start)
            running_times.append(running_stop - running_start)

        # Calculate average runtime for "add_action" methods
        post_average_calc_time = sum(post_times) / len(post_times)
        running_sum_calc_time = sum(running_times) / len(running_times)

        # call get stats and measure the runtime
        post_stats_start = perf_counter_ns()
        post_average = action_tracker_post.get_stats()[0]['avg']
        post_stats_elapsed = perf_counter_ns() - post_stats_start

        running_stats_start = perf_counter_ns()
        running_sum_average = action_tracker_running.get_stats()[0]['avg']
        running_stats_elapsed = perf_counter_ns() - running_stats_start

        control_average = sum(values)/len(values)

        print(f"\nPost Process object\n"
              f"add_action average runtime: {post_average_calc_time}ns\n"
              f"get_stats runtime: {post_stats_elapsed}ns\n\n")
        print(f"Running Sum object\n"
              f"add_action average runtime: {running_sum_calc_time}ns\n"
              f"get_stats runtime: {running_stats_elapsed}ns")

        self.assertEqual(control_average, running_sum_average, "Running sum reported an incorrect average")
        self.assertEqual(control_average, post_average, "Post processing reported an incorrect average")

    def test_inputs(self):
        # Probably a way to iterate/loop this testing since both objects behave the same from the user perspective
        action_tracker_post = ActionTrackerPost()
        action_tracker_running = ActionTrackerRunning()

        # Blank action strings
        with self.assertRaises(ValueError, msg="Blank action string did not raise ValueError exception"):
            action_tracker_post.add_action({'action': '', 'time': 10})
        with self.assertRaises(ValueError, msg="Blank action string did not raise ValueError exception"):
            action_tracker_running.add_action({'action': '', 'time': 10})

        # non-string action values
        with self.assertRaises(ValueError, msg="Non-string action value did not raise a ValueError exception"):
            action_tracker_post.add_action({'action': 123, 'time': 10})
        with self.assertRaises(ValueError, msg="Non-string action value did not raise a ValueError exception"):
            action_tracker_running.add_action({'action': 123, 'time': 10})

        # Negative time values
        with self.assertRaises(ValueError, msg="Negative time did not raise ValueError exception"):
            action_tracker_post.add_action({'action': 'jump', 'time': -1})
        with self.assertRaises(ValueError, msg="Negative time did not raise ValueError exception"):
            action_tracker_running.add_action({'action': 'jump', 'time': -1})

        # non-integer time values
        with self.assertRaises(ValueError, msg="Non-integer time value did not raise ValueError exception"):
            action_tracker_post.add_action({'action': 'jump', 'time': 'time is subjective'})
        with self.assertRaises(ValueError, msg="Non-integer time value did not raise ValueError exception"):
            action_tracker_running.add_action({'action': 'jump', 'time': 'time is subjective'})

        # Unspecified errors relating to the input json.  These are the ones I've found in manual testing by using a
        # range of incorrect formats.  Ignore the warnings, assertRaises can accept a tuple of exception classes
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_running.add_action({})
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_post.add_action({})
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_running.add_action({'action'})
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_post.add_action({'action'})
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_running.add_action({'action'})
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_post.add_action({'action'})
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_running.add_action({'action': 'hello'})
        with self.assertRaises((TypeError, SyntaxError, KeyError)):
            action_tracker_post.add_action({'action': 'hello'})


if __name__ == '__main__':
    unittest.main()
