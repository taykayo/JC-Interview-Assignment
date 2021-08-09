# JumpCloud Interview Assignment

## Stack Requirements:
- Windows 10
- Python 3.9

No specific virtual environment is necessary to install as only built-in modules were utilized.

## Functionality
This small chunk of python code is meant to satisfy the requirements specified
in \docs\Backend Assignment - Senior Software.pdf

Contains two classes that are identical in terms of current function, but present two differing
implementations to achieve their goal.

Both classes feature an "add_action(json_serialized_string)" function, and a "get_stats()" function.

### ActionTrackerPost
- Stores the inputted actions in a dictionary, where the key is the action name, and the value
is a list of all the times associated with that action, e.g. {'Jump': [100,20,25,99], 'run': [1,2,3,4]}
- Calling "get_stats()" will calculate the average of all items in the list for each unique action/key:
```python
for key in self.actions.keys():
    # calculate average for each unique key in actions dict
    avg_dict['action'] = key
    avg_dict['avg'] = (sum(self.actions[key])/len(self.actions[key]))
```
- Large amounts of actions & times will cause the get_stats() function to perform slower as each list inside the
dictionary is undergoing summation.
- As each action "event" is stored with the calculations happening only when desired, adding additional
metrics is trivial

### ActionTrackerRunning
- Stores the inputted actions in a dictionary, where the key is the action name, and the value
is a list containing a running sum of time for that particular action, and the # of times that particular
action has been added, e.g. {'jump': [244, 4], 'run': [10,4]}
- Calling "get_stats()" will calculate the average time for each action/key using the sum and
count:
```python
for key in self.actions.keys():
    # calculate average for each unique key in actions dict

    avg_dict['action'] = key
    avg_dict['avg'] = self.actions[key][0]/self.actions[key][1]
```
- The "add_action" function is marginally slower than in ActionTrackerPost as it continuously updates
the running sum of time values for the inputted action. 
- The "get_stats" function does NOT speed up with number of inputted time values, but rather with number of unique
actions, as it performs one calculation per unique action, rather than summating through the lists of each
inputted time value. As such, this performs **far** better on average than in ActionTrackerPost.
- Due to how the values are stored, this implementation is only useful for calculating averages as the
original data is altered.  Ideally these implementations could be merged, but I wanted to highlight two
different solutions for different use cases.

## Usage
Run the the following to scripts from command line. 

- main.py runs 4 batches of 100,000 actions through the objects, then spits out the averages, along with
the time each implementation took to run the get_stats() function (just to highlight the difference in speed)
- test.py runs automated tests.

No assumptions were made regarding the "add_action" input - negative times are handled exceptions, as are blank actions,
among various other fringe cases.  Extra keys in the json input are unused and will not cause an exception unless
they contain invalid json formatting.  Actions other than 'jump' and 'run' are allowed.  Concurrent actions
should not present an issue as each object contains a Lock that prevents race conditions.

##Future Considerations
- Clean the test code a bit, and add more tests. Not every single fringe case has an automated test. In particular,
write a test case to verify the threading.Lock() objects are functioning as desired to prevent issues with concurrent
calls.
- Consider merging implementations to keep the extensibility of post-processing the averages, along with
the speed of keeping a running sum.







