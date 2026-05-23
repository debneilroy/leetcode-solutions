"""
LeetCode 636. Exclusive Time of Functions
Difficulty: Medium
URL: https://leetcode.com/problems/exclusive-time-of-functions/
"""

# Brute Force Approach (Brief Explanation)
# Core Idea: Simulate every single unit of time from start to finish.

# Steps:

# 1. Create a timeline array where each index represents a timestamp (0 to max_time)
# 2. Process logs chronologically to track which function is on the call stack at each moment
# 3. Fill the timeline: For each timestamp, mark which function is currently executing (the one on top of the stack)
# 4. Count occurrences: Go through the timeline array and count how many times each function ID appears

# Example:

# For logs ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]
# Create array: [0, 0, 1, 1, 1, 1, 0] (length 7)
# Count: function 0 appears 3 times, function 1 appears 4 times
# Result: [3, 4]

# Why it's bad:

# Time: O(T) where T = maximum timestamp value (could be 10^9!)
# Space: O(T) for the timeline array (could need gigabytes of memory)

class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        """
        Calculate exclusive execution time for each function based on logs.
        
        Approach:
        - Use a stack to track active function calls
        - When a function starts, pause the previous function and push new one
        - When a function ends, calculate its exclusive time and resume previous
        - Track the last timestamp to calculate time differences

        Time Complexity: O(m) where m is the number of logs
        - Single pass through all logs
        - Each log is processed in O(1) time (parsing + stack operations)
        - Example with m = 8 logs:
          logs = ["0:start:0", "1:start:1", "2:start:2", "3:start:3",
                  "3:end:4", "2:end:5", "1:end:6", "0:end:7"]
          Process all 8 logs exactly once → O(m)
        
        Space Complexity: O(n + m) where n is number of functions, m is number of logs
        - Result array: O(n)
          Allocate space for all n functions
        - Stack: O(d) where d is maximum call depth
          - In worst case, d = m/2 when all "start" logs appear before matching "end" logs
          - Stack depth depends on call nesting, not number of distinct functions
        - Worst case example (maximum stack depth):
          n = 1, m = 6
          logs = ["0:start:0", "0:start:1", "0:start:2",
                  "0:end:3", "0:end:4", "0:end:5"]
          Stack growth: [] → [0] → [0,0] → [0,0,0] → [0,0] → [0] → []
          Max stack size = 3 = m/2 (not bounded by n)
        - Overall: O(n + m)
        """
        # Base check 1: Invalid n
        if n <= 0:
            return []
        
        # Base check 2: Empty or None logs
        if not logs:
            return [0] * n
        
        # Base check 3: Single log (invalid - need at least start+end pair)
        if len(logs) < 2:
            return [0] * n

        result = [0] * n  # Store exclusive time for each function
        stack = []  # Stack to track function IDs
        prev_time = 0  # Track the previous timestamp
        
        for log in logs:
            # Parse the log entry
            fn_id, action, timestamp = log.split(":")
            fn_id, timestamp = int(fn_id), int(timestamp)
            
            if action == 'start':
                # If there's a function currently running, add its time
                if stack:
                    # Current function ran from prev_time to time (exclusive)
                    # No +1 here because 'start' means the NEW function starts AT this timestamp
                    # So the previous function's time EXCLUDES this timestamp
                    # Example: prev_time=0, time=2 → function ran at times 0,1 (not 2)
                    result[stack[-1]] += timestamp - prev_time
                
                # Push new function onto stack
                stack.append(fn_id)
                prev_time = timestamp

            else:  # action == 'end'
                # Function ending - it ran from prev_time to time (inclusive)
                # We add +1 here because 'end' means the function INCLUDES this timestamp
                # The function completes AT this timestamp, so we count it
                # Example: prev_time=2, time=5 → function ran at times 2,3,4,5 
                # That's (5-2)+1 = 4 time units
                result[stack[-1]] += timestamp - prev_time + 1 
                
                # Remove completed function from stack
                stack.pop()

                # or, in one line, result[stack.pop()] += timestamp - prev_time + 1 
                
                # Update prev_time to the next timestamp after this function ends
                # We add +1 because the function finished at 'time', 
                # so next function (if any) will start from time+1
                prev_time = timestamp + 1
        
        return result


# Variant : App profiler

# You are tasked to profile the performance of an application. Specifically, you are given a list of logs representing the execution of function calls in the single-threaded application. Each log records the function name, the event type ("start" or "end"), and the timestamp when the event occurred.
# A function's exclusive time is defined as the total time it spends executing, excluding any time spent in its sub-functions (i.e., functions it calls directly).
# Write a function profile_app that takes in the list of logs and returns a dictionary mapping each function name to its exclusive execution time. You may define the schema of each log however you choose.

# Example:
# Input: logs = [["foo","start",10],["bar","start",20],["bar","end",50],["foo","end",100]]
# Output: {"foo": 60, "bar": 30}

# Constraints:

# 1. 2 <= logs.length <= 500
# 2. Function names are limited to lowercase English letters.
# 3. 1 <= name.length < 100
# 4. 0 <= time <= 10^9
# 5. No two start events will happen at the same timestamp.
# 6. No two end events will happen at the same timestamp.
# 7. Each function has an "end" log for each "start" log.

# class Solution:
#     def profile_app(self, logs: List[List]) -> Dict[str, int]:
#         """
#         Calculate exclusive execution time for each function.

#         DIFFERENCE FROM LEETCODE 636 (Original Problem):
#         This variant uses EXCLUSIVE end timestamps [start, end) - half-open intervals
#         - Example: start=10, end=50 → runs during [10,11,...,49] = 40 units
        
#         LeetCode 636 uses INCLUSIVE end timestamps [start, end] - closed intervals
#         - Example: start=10, end=50 → runs during [10,11,...,50] = 41 units
        
#         Key Insight:
#         - Uses half-open intervals [start, end)
#         - End timestamp is exclusive (unlike LeetCode 636 which uses inclusive)
#         - Example: start=10, end=50 → function runs during [10,11,...,49] = 40 units
        
#         Assumptions:
#         - Logs are sorted by timestamp (chronological order)
#         - Logs are properly nested (valid call stack)
        
#         Time Complexity (Worst Case): O(m) where m = number of logs
#         - Single pass through all logs
#         - Each log processed in O(1) time (parsing + stack operations)
#         - Worst case example with m = 6:
#           logs = [["a","start",0], ["b","start",1], ["c","start",2],
#                   ["c","end",3], ["b","end",4], ["a","end",5]]
#           Process all 6 logs exactly once → O(6) = O(m)
        
#         Note: If logs are NOT sorted, must sort first → O(m log m) time complexity
        
#         Space Complexity (Worst Case): O(m) where m = number of logs
#         - Stack: O(d) where d = maximum call depth
#           Worst case: d = m/2 when all "start" logs before all "end" logs
#           Example with m = 6:
#           logs = [["foo","start",0], ["foo","start",1], ["foo","start",2],
#                   ["foo","end",3], ["foo","end",4], ["foo","end",5]]
#           Stack grows: [] → [foo] → [foo,foo] → [foo,foo,foo] (size 3 = m/2)
#         - Result dictionary: O(k) where k = unique function names
#           Worst case: k = m/2 when all functions are different
#           Example with m = 6:
#           logs = [["a","start",0], ["b","start",1], ["c","start",2],
#                   ["c","end",3], ["b","end",4], ["a","end",5]]
#           Dictionary has 3 entries (a, b, c) = m/2
#         - Overall: O(m/2) + O(m/2) = O(m)
#         """
#         # Edge case 1: Empty logs
#         if not logs:
#             return {}
        
#         # Edge case 2: Single log (invalid - need at least start+end pair)
#         if len(logs) < 2:
#             return {}
        
#         # Case 1: If logs are NOT sorted by timestamp
#         # Uncomment the following line to sort (changes TC to O(m log m)):
#         # logs = sorted(logs, key=lambda x: x[2])
        
#         # Case 2: Same timestamp events (if constraints don't guarantee uniqueness)
#         # If two events can have same timestamp, we need stable ordering:
#         # - 'end' events should come before 'start' events at same timestamp
#         # - This ensures a function completes before another starts
#         # Alternative sort: logs = sorted(logs, key=lambda x: (x[2], x[1] == 'start'))
        
#         result = defaultdict(int)
#         stack = []
#         prev_time = 0
        
#         for log in logs:

#             # Case 3: Malformed log (wrong number of fields)
#             # if len(log) != 3:
#             #     continue  # Skip invalid log
            
#             name, fn_type, timestamp = log[0], log[1], log[2]
            
#             # # Case 4: Invalid event type (not 'start' or 'end')
#             # if fn_type not in ['start', 'end']:
#             #     continue  # Skip invalid event type
            
#             # # Case 5: Negative or invalid timestamp
#             # # In real systems, timestamps should be non-negative
#             # if timestamp < 0:
#             #     continue  # Skip invalid timestamp
            
#             # # Case 6: Timestamp goes backward (indicates unsorted or corrupted data)
#             # # This check only makes sense if we assume logs should be sorted
#             # if timestamp < prev_time:
#             #     continue  # Skip out-of-order timestamp
            
#             if fn_type == 'start':
#                 if stack:
#                     # Update the currently running function's time
#                     result[stack[-1]] += timestamp - prev_time
                
#                 # Push new function onto stack
#                 stack.append(name)
#                 prev_time = timestamp

#             else:  # action == 'end'
#                 # Function completes - add its final execution time
#                 # Runs from prev_time to timestamp (EXCLUSIVE of end timestamp)
#                 # No +1 here because end timestamp is NOT included in this variant
#                 # Example: prev_time=20, timestamp=50 → runs [20,21,...,49] = 30 units
#                 # 
#                 # DIFFERENCE FROM LEETCODE 636:
#                 # - LeetCode 636: result[stack.pop()] += timestamp - prev_time + 1 (inclusive)
#                 # - This variant: result[stack.pop()] += timestamp - prev_time (exclusive)
#                 result[stack.pop()] += timestamp - prev_time
                
#                 # Update prev_time to timestamp (NOT timestamp + 1)
#                 # Because the next function starts right at this timestamp
#                 # 
#                 # DIFFERENCE FROM LEETCODE 636:
#                 # - LeetCode 636: prev_time = timestamp + 1 (next starts after this timestamp)
#                 # - This variant: prev_time = timestamp (next starts at this timestamp)
#                 prev_time = timestamp
        
#         # Case 9: Unclosed function calls (stack not empty at end)
#         # If stack is not empty, some functions never had 'end' events
#         # We could either:
#         # - Ignore them 
#         # - Log a warning (current approach)
#         if stack:
#             raise ValueError("Unclosed function calls detected")
        
#         # Case 10: Return type - convert defaultdict to regular dict
#         # This ensures the return value is a plain dict, not defaultdict
#         return dict(result)

# # # If result is just a simple dictionary

# def profile_app(logs):
#     result = {}
#     stack = []
#     prev_time = 0

#     for log in logs:
#         name, fn_type, time = log[0], log[1], log[2]

#         if fn_type == 'start':
#             if stack:
#                 result[stack[-1]] = result.get(stack[-1], 0) + time - prev_time
#             stack.append(name)
#             prev_time = time
#         else:
#             func_name = stack.pop() # Pop once and store in a variable
#             result[func_name] = result.get(func_name, 0) + time - prev_time
#             prev_time = time

#     return result

# # Another approach (using a Log class)

# class Log:
#     def __init__(self, name, fn_type, time):
#         self.name = name
#         self.fn_type = fn_type
#         self.time = time

# class Solution:
#     def profile_app(self, logs: List[Log]) -> Dict[str, int]:
#         result = defaultdict(int)  # Store exclusive time for each function
#         stack = []  # Track currently executing functions
#         prev_time = 0  # Track previous timestamp
        
#         for log in logs:
#             # Access log attributes directly
#             name = log.name
#             fn_type = log.fn_type
#             time = log.time
            
#             if fn_type == 'start':
#                 # If a function is running, add its execution time before pausing
#                 if stack:
#                     # Previous function ran from prev_time to time (exclusive)
#                     result[stack[-1]] += time - prev_time
                
#                 # Start new function
#                 stack.append(name)
                
#             else:  # type == 'end'
#                 # Function completes - add its final execution time
#                 # Runs from prev_time to time (exclusive of end timestamp)
#                 result[stack.pop()] += time - prev_time

#             prev_time = time
        
#         return dict(result)

# logs = [
#         Log("foo", "start", 10),
#         Log("bar", "start", 20),
#         Log("bar", "end", 50),
#         Log("foo", "end", 100)
#     ]
# sol = Solution()
# sol.profile_app(logs)
        