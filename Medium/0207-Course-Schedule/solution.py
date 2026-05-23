"""
LeetCode 207. Course Schedule
Difficulty: Medium
URL: https://leetcode.com/problems/course-schedule/
"""

 # A brute-force approach would be to repeatedly pick any course whose prerequisites are already satisfied and remove it from the dependency list. If all courses can be removed, it means there’s no cycle.

# This approach requires scanning all courses in each iteration and may run up to numCourses times, giving a 
# time complexity of O(V² + E) (we may have to scan all V courses up to V times — once per removal — in the worst case, leading to O(V²), plus O(E) for handling edge updates) and 

# space complexity of O(V + E) (O(V) to track the courses and their completion status, and O(E) to store the prerequisite relationships in an adjacency list).

# To optimize, we can use DFS cycle detection or Kahn’s algorithm (topological sort), both of which achieve O(V + E) time and O(V + E) space.


# Approach : Topological Sort with BFS

class Solution:
    def canFinish(self, numCourses, prerequisites):
        """
        Determines if all courses can be completed given prerequisites.
        Uses Topological Sort (Kahn's Algorithm) with BFS.
        
        Approach: If there's a cycle in the prerequisite graph, courses cannot be completed.
        We process courses starting from those with no prerequisites, removing them one by one.
        If we can process all courses, there's no cycle.

        Time Complexity: O(V + E) where V = numCourses, E = len(prerequisites)
        - Build graph: O(V) to initialize + O(E) to add edges
        - Initialize in_degree: O(V)
        - Initialize queue: O(V) to scan all courses
        - BFS processing: O(V) to process all courses + O(E) to examine all edges
        - Total: O(V) + O(E) + O(V) + O(V + E) = O(V + E)
        
        Space Complexity: O(V + E)
        - Graph adjacency list: O(V + E) - V lists with total E edges stored
        - in_degree array: O(V)
        - Queue: O(V) worst case when all courses have no prerequisites
        - Total: O(V + E) (graph dominates)
        """

        # BASE CASE 1: Invalid number of courses
        # Handle negative or zero courses
        if numCourses <= 0:
            return True  # or False, clarify with interviewer
        
        # BASE CASE 2: No prerequisites (optional optimization)
        # All courses can be taken independently
        if not prerequisites:
            return True
        
        # Build adjacency list representation of the graph
        # graph[i] contains all courses that have course i as a prerequisite
        # Example: if [1,0] exists, graph[0] will contain 1
        graph = [[] for _ in range(numCourses)]
        
        # in_degree[i] tracks how many prerequisites course i has
        # A course with in_degree 0 has no prerequisites and can be taken immediately
        in_degree = [0] * numCourses
        
        # Build the graph and calculate in-degrees
        for course, prereq in prerequisites:
            # prereq -> course (prereq must be taken before course)
            graph[prereq].append(course)
            # Course has one more prerequisite
            in_degree[course] += 1

        print(graph)
        
        # Initialize queue with all courses that have no prerequisites
        # These courses can be taken immediately (in_degree == 0)
        queue = deque()
        for course in range(numCourses):
            if in_degree[course] == 0:
                queue.append(course)
        
        # Track how many courses we've successfully processed
        # If this equals numCourses at the end, all courses can be completed
        courses_taken = 0
        
        # Process courses using BFS
        while queue:
            # Take a course (simulate completing it)
            course = queue.popleft()
            courses_taken += 1
            
            # For each course that depends on the current course
            for neighbor in graph[course]:
                # Remove the dependency (decrease in-degree by 1)
                in_degree[neighbor] -= 1
                
                # If this course now has no more prerequisites, it can be taken
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # If we processed all courses, there's no cycle
        # If courses_taken < numCourses, some courses are stuck in a cycle
        # Example of cycle: [0,1] and [1,0] means neither can ever have in_degree 0
        return courses_taken == numCourses

# Example without a Cycle

# numCourses = 3
# prerequisites = [[1,0], [2,1]]

# # What this means:
# # Course 1 needs Course 0
# # Course 2 needs Course 1
# # No cycle! Linear chain: 0 → 1 → 2

# # Step-by-Step Execution
# # Initial Setup:

# # Build the graph
# graph[0] = [1]  # Course 0 unlocks Course 1
# graph[1] = [2]  # Course 1 unlocks Course 2
# graph[2] = []   # Course 2 unlocks nothing

# # Calculate in-degrees (how many prerequisites each course has)
# in_degree[0] = 0  # Course 0 needs nothing! ✓
# in_degree[1] = 1  # Course 1 needs Course 0
# in_degree[2] = 1  # Course 2 needs Course 1

# # Initialize queue with courses that have no prerequisites
# queue = [0]  # Course 0 can start immediately!

# # Processing:
# course_order = []

# # Step 1: Process Course 0
# while queue:  # queue = [0]
#     course = queue.popleft()  # course = 0
#     course_order.append(0)     # course_order = [0]
#     courses_taken = 1
    
#     for neighbor in graph[0]:  # neighbor = 1
#         in_degree[1] -= 1       # in_degree[1] becomes 0
#         queue.append(1)         # queue = [1]

# # Step 2: Process Course 1
#     course = queue.popleft()  # course = 1
#     course_order.append(1)     # course_order = [0, 1]
#     courses_taken = 2
    
#     for neighbor in graph[1]:  # neighbor = 2
#         in_degree[2] -= 1       # in_degree[2] becomes 0
#         queue.append(2)         # queue = [2]

# # Step 3: Process Course 2
#     course = queue.popleft()  # course = 2
#     course_order.append(2)     # course_order = [0, 1, 2]
#     courses_taken = 3
    
#     for neighbor in graph[2]:  # No neighbors
#         pass
#     # queue is now empty

# # Final check
# len(course_order) == 3
# numCourses == 3
# 3 == 3  → Return True (all courses completed, no cycle!) ✓

# Valid course order: [0, 1, 2]



# Example with a Cycle
# numCourses = 3
# prerequisites = [[1,0], [2,1], [0,2]]

# What this means:
# Course 1 needs Course 0
# Course 2 needs Course 1  
# Course 0 needs Course 2  ← This creates a cycle!

# # The cycle: 0 → 1 → 2 → 0 (back to start)
# Step-by-Step Execution
# Initial Setup:
# # Build the graph
# graph[0] = [1]  # Course 0 unlocks Course 1
# graph[1] = [2]  # Course 1 unlocks Course 2
# graph[2] = [0]  # Course 2 unlocks Course 0

# # Calculate in-degrees (how many prerequisites each course has)
# in_degree[0] = 1  # Course 0 needs Course 2
# in_degree[1] = 1  # Course 1 needs Course 0
# in_degree[2] = 1  # Course 2 needs Course 1

# # Initialize queue with courses that have no prerequisites
# queue = []  # EMPTY! Every course has in_degree = 1
# The Problem is Immediately Visible:
# # Queue is empty because no course has in_degree = 0
# # This means every course is waiting for another course

# course_order = []

# # While loop never executes because queue is empty
# while queue:  # False, queue is empty
#     # This code never runs!
#     pass

# # Final check
# len(course_order) == 0
# numCourses == 3
# 0 != 3  → Return False (cycle detected!)

# Approach : DFS

# There is also a DFS approach that detects cycles directly. We use 3 states: unvisited, visiting, and visited. The key insight is if we encounter a course that is currently being visited in our DFS path, we have found a cycle. We mark courses as 'visiting' when we start exploring them, and 'visited' when done. Same O(V + E) complexity, just a different way to detect cycles - directly through state tracking rather than counting processed nodes.

class Solution:
    def canFinish(self, numCourses, prerequisites):
        """
        Determines if all courses can be completed given prerequisites.
        Uses DFS with state tracking to detect cycles.
        
        Approach: A cycle in the prerequisite graph means courses cannot be completed.
        We use DFS to explore each course and track visiting states to detect cycles.
        
        Key insight: If we're currently exploring a course (state=1) and we encounter 
        it again in the same DFS path, we've found a cycle.
        
        Time: O(V + E) where V = numCourses, E = len(prerequisites)
        Space: O(V + E) for graph + O(V) for recursion stack = O(V + E)
        """
        
        # Build adjacency list representation of the graph
        # graph[i] contains all courses that have course i as a prerequisite
        # Example: if [1,0] exists, graph[0] will contain 1
        graph = [[] for _ in range(numCourses)]
        
        for course, prereq in prerequisites:
            # prereq -> course (must take prereq before course)
            graph[prereq].append(course)
        
        # State tracking for each course (3-color algorithm):
        # 0 = UNVISITED (white) - haven't explored this course yet
        # 1 = VISITING (gray) - currently exploring this course in current DFS path
        # 2 = VISITED (black) - completely finished exploring this course and all its dependencies
        state = [0] * numCourses
        
        def hasCycle(course):
            """
            DFS helper to detect if there's a cycle starting from this course.
            Returns True if cycle detected, False otherwise.
            """
            
            # CYCLE DETECTED: We've encountered a course that's already in our current path
            # This means we've looped back to a course we're still processing
            # Example: 0 -> 1 -> 2 -> 1 (visiting 1 again while still exploring from 1)
            if state[course] == 1:
                return True
            
            # ALREADY PROCESSED: We've fully explored this course before in a different path
            # No need to explore again - we know it's safe (no cycles from here)
            # This optimization prevents redundant work
            if state[course] == 2:
                return False
            
            # Mark this course as currently being visited (part of current DFS path)
            # If we encounter this course again before finishing, it's a cycle
            state[course] = 1
            
            # Explore all courses that depend on this one (all neighbors)
            # Think of it as: "If I take this course, what courses does it unlock?"
            # graph[course] is a list of integers, neighbor is each individual integer
            # Example: if graph[0] = [1, 2], then neighbor will be 1, then 2
            for neighbor in graph[course]:
                # Recursively check if any path from neighbor leads to a cycle
                if hasCycle(neighbor):
                    return True  # Propagate cycle detection up the call stack
            
            # We've finished exploring all paths from this course without finding cycles
            # Mark it as completely visited so we don't redundantly explore it again
            # Any future DFS that reaches this course can safely skip it
            state[course] = 2
            
            return False  # No cycle found from this course
        
        # Check every course as a potential starting point
        # We need to check all courses because the graph might be disconnected
        # (some courses might not be reachable from others)
        for course in range(numCourses):
            # If we find a cycle starting from any course, return False immediately
            if hasCycle(course):
                return False
        
        # We've checked all courses and found no cycles
        # Therefore, all courses can be completed
        return True

# Follow up : Return the ordering of courses you should take to finish all courses. (Leetcode 210. Course Schedule II)

# Topological sort

# class Solution:
#     def findOrder(self, numCourses, prerequisites):
#         """
#         Returns the actual course order if possible, empty list if impossible.
#         This is LeetCode 210 - Course Schedule II
        
#         The key change: instead of just counting, we store the order as we process.
#         """
        
#         # Build adjacency list and in-degree array (same as before)
#         graph = [[] for _ in range(numCourses)]
#         in_degree = [0] * numCourses
        
#         for course, prereq in prerequisites:
#             graph[prereq].append(course)
#             in_degree[course] += 1
        
#         # Initialize queue with courses that have no prerequisites
#         queue = deque()
#         for course in range(numCourses):
#             if in_degree[course] == 0:
#                 queue.append(course)
        
#         # THIS IS THE KEY CHANGE: Store the actual order instead of just counting
#         course_order = []
        
#         while queue:
#             course = queue.popleft()
#             # Add this course to our order as we "complete" it
#             course_order.append(course)
            
#             # Process neighbors (same as before)
#             for neighbor in graph[course]:
#                 in_degree[neighbor] -= 1
#                 if in_degree[neighbor] == 0:
#                     queue.append(neighbor)
        
#         # If we got all courses, return the order; otherwise return empty list
#         # len(course_order) == numCourses means no cycle
#         return course_order if len(course_order) == numCourses else []

# # Approach : DFS

# class Solution:
#     def findOrder(self, numCourses, prerequisites):
#         """
#         Returns the actual course order if possible, empty list if cycle exists.
#         Uses DFS with state tracking and builds order in reverse.
        
#         Key insight: In DFS, we add a course to the order AFTER exploring all
#         its dependencies. This naturally gives us reverse topological order.
        
#         Time: O(V + E) where V = numCourses, E = len(prerequisites)
#         Space: O(V + E) for graph + O(V) for recursion stack
#         """
        
#         # Build adjacency list representation of the graph
#         # graph[prereq] contains all courses that need prereq as a prerequisite
#         graph = [[] for _ in range(numCourses)]
        
#         for course, prereq in prerequisites:
#             graph[prereq].append(course)
        
#         # State tracking for cycle detection:
#         # 0 = UNVISITED (haven't explored yet)
#         # 1 = VISITING (currently in DFS path - used to detect cycles)
#         # 2 = VISITED (fully explored - safe to skip)
#         state = [0] * numCourses
        
#         # Store the course order as we complete DFS on each course
#         # We'll build this in REVERSE topological order
#         course_order = []
        
#         def hasCycle(course):
#             """
#             DFS to explore course and all its dependencies.
#             Returns True if cycle detected, False otherwise.
#             """
            
#             # CYCLE DETECTED: Found a course in our current DFS path
#             if state[course] == 1:
#                 return True
            
#             # ALREADY PROCESSED: This course and all its dependencies are done
#             # We've already added it to course_order, so skip it
#             if state[course] == 2:
#                 return False
            
#             # Mark as currently visiting (part of current DFS path)
#             state[course] = 1
            
#             # Explore all courses that depend on this course
#             # We need to complete all dependencies before we can take this course
#             for neighbor in graph[course]:
#                 if hasCycle(neighbor):
#                     # Cycle detected in neighbor's subtree, propagate success
#                     return True
            
#             # CRITICAL: Add course to order AFTER exploring all its dependencies
#             # This is the key difference from the canFinish version!
#             # We add a course only after all courses that depend on it are added
#             # This gives us REVERSE topological order (post-order traversal)
#             course_order.append(course)
            
#             # Mark as fully visited
#             state[course] = 2
            
#             return False
        
#         # Try DFS from every course (handles disconnected components)
#         for course in range(numCourses):
#             # If any DFS finds a cycle, return empty list immediately
#             if hasCycle(course):
#                 return []
        
#         # IMPORTANT: Reverse the order!
#         # We built the list in reverse topological order (post-order DFS)
#         # Reversing gives us the correct topological order
#         return course_order[::-1]

# Variant : Course Schedule (Adjacency List Form)

# You are given a directed graph representing course dependencies. There are a total of graph.length courses labeled from 0 to graph.length - 1. The graph is represented as an adjacency list, where graph[i] contains a list of courses that depend on the completion of course i.

# In other words, for every course i, each element in graph[i] denotes a course that requires i as a prerequisite.

# Return true if you can finish all courses (i.e., the graph has no cycle). Otherwise, return false.

# Example 1

# Input:
# graph = [[1], []]
# Output: True

# Explanation:
# There are 2 courses in total.
# To take course 1, you must first finish course 0.
# Since this dependency can be satisfied, all courses can be completed.

# Example 2

# Input:
# graph = [[1], [0], []]
# Output: False

# Explanation:
# There are 3 courses in total.
# Course 2 can be finished, but course 0 and 1 form a cycle (each depends on the other),
# so it’s impossible to finish all courses.

# Constraints

# 1 <= graph.length <= 5000

# All directed edges in the graph are unique.

# The number of nodes equals graph.length.

# Approach : Topological Sort

# class Solution:
#     def canFinish(self, graph):
#         """
#         Uses Topological Sort (Kahn's Algorithm) with BFS to detect cycles.
        
#         Time: O(V + E) where V = len(graph), E = total edges
#         Space: O(V) for in_degree array and queue
#         """
        
#         # Number of courses
#         numCourses = len(graph)
        
#         # Calculate in-degrees: count how many prerequisites each course has
#         # in_degree[i] = number of courses that must be completed before course i
#         in_degree = [0] * numCourses
        
#         # For each course i, increment in_degree for all courses that depend on it
#         for i in range(numCourses):
#             for neighbor in graph[i]:
#                 in_degree[neighbor] += 1
        
#         # Initialize queue with all courses that have no prerequisites (in_degree == 0)
#         # These courses can be taken immediately
#         queue = deque()
#         for i in range(numCourses):
#             if in_degree[i] == 0:
#                 queue.append(i)
        
#         # Track how many courses we've successfully completed
#         courses_taken = 0
        
#         # Process courses using BFS
#         while queue:
#             # Take a course (simulate completing it)
#             course = queue.popleft()
#             courses_taken += 1
            
#             # For each course that depends on the current course
#             for neighbor in graph[course]:
#                 # Remove the dependency (decrease in-degree by 1)
#                 in_degree[neighbor] -= 1
                
#                 # If this course now has no more prerequisites, it can be taken
#                 if in_degree[neighbor] == 0:
#                     queue.append(neighbor)
        
#         # If we processed all courses, there's no cycle
#         # If courses_taken < numCourses, some courses are stuck in a cycle
#         return courses_taken == numCourses
        

# # Approach : DFS

# class Solution:
#     def canFinish(self, graph):
#         """
#         Uses DFS with state tracking to detect cycles.
        
#         Time: O(V + E) where V = len(graph), E = total edges
#         Space: O(V) for state array + O(V) for recursion stack = O(V)
#         """
        
#         # Number of courses
#         numCourses = len(graph)
        
#         # State tracking for cycle detection:
#         # 0 = UNVISITED (haven't explored this course yet)
#         # 1 = VISITING (currently exploring this course in current DFS path)
#         # 2 = VISITED (completely finished exploring this course and all dependencies)
#         state = [0] * numCourses
        
#         def hasCycle(course):
#             """
#             DFS helper to detect if there's a cycle starting from this course.
#             Returns True if cycle detected, False otherwise.
#             """
            
#             # CYCLE DETECTED: We've encountered a course in our current DFS path
#             # This means we've looped back to a course we're still processing
#             if state[course] == 1:
#                 return True
            
#             # ALREADY PROCESSED: This course and all its dependencies are fully explored
#             # No need to explore again - we know it's safe (no cycles from here)
#             if state[course] == 2:
#                 return False
            
#             # Mark this course as currently being visited (part of current DFS path)
#             state[course] = 1
            
#             # Explore all courses that depend on this course
#             # graph[course] directly gives us the list of dependent courses
#             for neighbor in graph[course]:
#                 # Recursively check if any path from neighbor leads to a cycle
#                 if hasCycle(neighbor):
#                     return True  # Propagate cycle detection up the call stack
            
#             # We've finished exploring all paths from this course without finding cycles
#             # Mark it as completely visited
#             state[course] = 2
            
#             return False  # No cycle found from this course
        
#         # Check every course as a potential starting point
#         # Need to check all courses because graph might be disconnected
#         for course in range(numCourses):
#             # If we find a cycle starting from any course, return false immediately
#             if hasCycle(course):
#                 return False
        
#         # We've checked all courses and found no cycles
#         # Therefore, all courses can be completed
#         return True