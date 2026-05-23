"""
LeetCode 56. Merge Intervals
Difficulty: Medium
URL: https://leetcode.com/problems/merge-intervals/
"""

# Check another variant LC 57

# Approach : Brute Force

# class Solution:
#     def merge(self, intervals: List[List[int]]) -> List[List[int]]:
#         """
#         Brute Force: Multiple passes until no more merges possible.
        
#         Algorithm:
#         1. Start with first interval in result
#         2. For each remaining interval:
#            - Check against ALL intervals in result
#            - If overlaps with any: merge them
#            - If no overlap with any: add as new interval
#         3. Repeat the entire process until no merges happen in a full pass
        
#         TC: O(n²) worst case, but may need multiple passes in practice
#         SC: O(n)
#         """
#         if not intervals:
#             return []
        
#         result = [intervals[0]]
        
#         # Process all intervals once
#         for i in range(1, len(intervals)):
#             curr = intervals[i]
#             merged = False
            
#             for j in range(len(result)):
#                 # Check overlap
#                 if curr[0] <= result[j][1] and curr[1] >= result[j][0]:
#                     # Merge
#                     result[j][0] = min(result[j][0], curr[0])
#                     result[j][1] = max(result[j][1], curr[1])
#                     merged = True
#                     break
            
#             if not merged:
#                 result.append(curr[:])
        
#         # Multiple passes until stable
#         changed = True
#         while changed:
#             changed = False
#             new_result = [result[0]]
            
#             # Try to merge intervals within result
#             for i in range(1, len(result)):
#                 curr = result[i]
#                 merged = False
                
#                 for j in range(len(new_result)):
#                     if curr[0] <= new_result[j][1] and curr[1] >= new_result[j][0]:
#                         new_result[j][0] = min(new_result[j][0], curr[0])
#                         new_result[j][1] = max(new_result[j][1], curr[1])
#                         merged = True
#                         changed = True
#                         break
                
#                 if not merged:
#                     new_result.append(curr[:])
            
#             result = new_result
        
#         return result

# Optimized Approach : Sorting

class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Merge all overlapping intervals.
        
        Algorithm:
        1. Sort intervals by start time
        2. Iterate through sorted intervals, merging when they overlap
        3. Two intervals [a, b] and [c, d] overlap if c <= b (since c >= a after sorting)
        
        TC: O(n log n) - dominated by sorting, where n = len(intervals)

        SC: O(n) - Python's Timsort requires O(n) auxiliary space for merge operations
            Breakdown:
            - Timsort worst-case: O(n) temporary arrays during merging
            - Output array: doesn't count (required by problem, not auxiliary space)
            Note: If using in-place sort like Heapsort, auxiliary space would be O(1)
                (Heapsort works in-place with iterative heap operations, no recursion stack)
                However, Python uses Timsort, so SC = O(n)
        """
        if not intervals:
            return []
        
        # Sort by start time
        # Why sort by start time?
        # - Without sorting, we'd need to compare each interval with ALL others -> O(n²)
        # - After sorting by start, if interval i overlaps with j, then i also overlaps 
        # with all intervals between i and j
        # - This allows greedy merging: we only need to check if current interval 
        # overlaps with the LAST merged interval (one comparison per interval)
        # - Example: [[1,3], [8,10], [2,6], [15,18]]
        # * Unsorted: would need to check [1,3] against all others, then [8,10] against all, etc.
        # * Sorted: [[1,3], [2,6], [8,10], [15,18]] - just extend [1,3] to [1,6] when we see [2,6]

        intervals.sort(key=lambda x: x[0])
        # Alternative: intervals = sorted(intervals, key=lambda x: x[0])
        # Both work; .sort() is slightly more efficient (no extra list creation)
        
        merged = [intervals[0]]
        
        for start, end in intervals[1:]:
            # Check if current interval overlaps with the last merged interval
            if start <= merged[-1][1]:
                # Merge by extending the end of the last interval
                merged[-1][1] = max(merged[-1][1], end)
            else:
                # No overlap, add as new interval
                merged.append([start, end])
        
        return merged


# Variant : Merge Two Sorted Interval Lists (mostly asked instead of the original one)

# Given two array intervals A and B where intervals in A have no overlap in A
# and intervals in B have no overlap in B. Furthermore, A[i], B[i] = [start_i, end_i],
# merge all overlapping intervals between the two interval lists, and return an array
# of the non-overlapping intervals that cover all the intervals in the input.
 
# Note: Both A and B are sorted by start in ascending order.
 
# Example 1:
# Input: A = [[3,11],[14,15],[18,22],[23,24],[25,26]]
#        B = [[2,8],[13,20]]
# Output: [[2,11],[13,22],[23,24],[25,26]]
 
# Example 2:
# Input: A = [], B = [[0,4],[10,13]]
# Output: [[0,4],[10,13]]

# class Solution:
#     def intervalIntersection_bruteforce(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
#         """
#         Brute force approach: Combine + Sort + Merge.
        
#         Algorithm:
#         1. Combine both lists into one
#         2. Sort the combined list by start time (ignores that A and B are already sorted!)
#         3. Merge overlapping intervals (same logic as LC 56)
        
#         TC: O((m+n) log(m+n)) where m = len(A), n = len(B)
#             - Combining: O(m+n)
#             - Sorting: O((m+n) log(m+n)) - dominates
#             - Merging: O(m+n)
#             - Total: O((m+n) log(m+n))
        
#         SC: O(m+n) auxiliary space
#             - Combined array: O(m+n)
#             - Timsort temporary space: O(m+n)
#             - Total: O(m+n)
        
#         Why is this suboptimal?
#         - We're sorting data that's already sorted!
#         - Like taking two sorted decks of cards, mixing them, then re-sorting
#         - Two-pointer approach is much better: O(m+n) time, O(1) space
#         """
#         # Base case: handle empty lists
#         if not A and not B:
#             return []
        
#         # Step 1: Combine both lists
#         intervals = A + B
        
#         # Step 2: Sort by start time (even though A and B are already sorted!)
#         # This is the inefficiency - we're re-sorting already sorted data
#         intervals.sort(key=lambda x: x[0])
        
#         # Step 3: Merge overlapping intervals (same as LC 56)
#         merged = [intervals[0]]
#         for start, end in intervals[1:]:
#             # Check if current interval overlaps with last merged interval
#             if start <= merged[-1][1]:
#                 # Overlap - merge by extending the end
#                 merged[-1][1] = max(merged[-1][1], end)
#             else:
#                 # No overlap - add as new interval
#                 merged.append([start, end])
        
#         return merged


# Optimized Approach : Two Pointer

# class Solution:
#     def intervalIntersection(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
#         """
#         Merge overlapping intervals from two sorted interval lists using two-pointer approach.
        
#         Algorithm (Two phases):
#         Phase 1: Merge from both lists while both are active (like merge sort)
#         Phase 2: Process remaining items from whichever list isn't exhausted
        
#         Why two-pointer approach?
#         - Both A and B are already sorted by start time
#         - No need to sort again (unlike LC 56)
#         - Process intervals in order, merging as we go
#         - TC: O(m + n) vs O((m+n) log(m+n)) for sort-then-merge
        
#         TC: O(m + n) where m = len(A), n = len(B)
#             - Single pass through both arrays with two pointers
#         SC: O(1) auxiliary space (output array doesn't count)
#         """
#         # Base case 1: Both empty
#         if not A and not B:
#             return []
        
#         # Base case 2: A empty - return B directly (no copying needed)
#         # This is O(1) optimization vs processing through merge logic
#         if not A:
#             return B
        
#         # Base case 3: B empty - return A directly (no copying needed)
#         if not B:
#             return A
        
#         result = []
#         i, j = 0, 0  # Two pointers for A and B
        
#         # ====================================================================
#         # PHASE 1: Process while BOTH lists have items
#         # ====================================================================
#         # Loop condition: "and" means both must be active
#         # This is simpler than "or" which would mix Phase 1 and Phase 2 logic
#         while i < len(A) and j < len(B):
#             # Pick the interval with smaller start time (like merge in merge sort)
#             if A[i][0] <= B[j][0]:
#                 curr_interval = A[i]
#                 i += 1
#             else:
#                 curr_interval = B[j]
#                 j += 1
            
#             # Try to merge curr_interval with result using helper method
#             self._try_merge(result, curr_interval)
        
#         # ====================================================================
#         # PHASE 2: Process remaining items from whichever list isn't exhausted
#         # ====================================================================
#         # At this point, exactly ONE of the following is true:
#         # - i < len(A) and j == len(B)  -> A has remaining items
#         # - i == len(A) and j < len(B)  -> B has remaining items
#         # - i == len(A) and j == len(B) -> Both exhausted (won't enter either loop)
        
#         # Process remaining items from A (if any)
#         while i < len(A):
#             self._try_merge(result, A[i])
#             i += 1
        
#         # Process remaining items from B (if any)
#         while j < len(B):
#             self._try_merge(result, B[j])
#             j += 1
        
#         return result
    
#     def _try_merge(self, result: List[List[int]], curr_interval: List[int]) -> None:
#         """
#         Helper method to merge curr_interval with the result list.
        
#         Logic:
#         - If curr_interval overlaps with last interval: merge them
#         - Otherwise: add curr_interval as a new interval
        
#         Overlap condition: curr_interval[0] <= result[-1][1]
#         - curr_interval starts before or at the end of last interval
#         - Example: result[-1] = [1,5], curr = [3,7] -> overlap (3 <= 5)
#         - Example: result[-1] = [1,5], curr = [6,8] -> no overlap (6 > 5)
        
#         Why max()?
#         - Handles cases where curr_interval is fully contained in last interval
#         - Example: result[-1] = [1,10], curr = [2,5] -> keep end as 10
        
#         TC: O(1) - constant time operations
#         SC: O(1) - no extra space
#         """
#         # Check if curr_interval overlaps with the last interval
#         if result and curr_interval[0] <= result[-1][1]:
#             # Overlap detected - merge by extending the end
#             # Use max() because curr might be fully contained in last interval
#             result[-1][1] = max(result[-1][1], curr_interval[1])
#         else:
#             # No overlap (or result is empty) - add as new interval
#             result.append(curr_interval)

# Variant : Merge three sorted intervals

# class Solution:
#     def mergeThreeLists(self, A: List[List[int]], B: List[List[int]], C: List[List[int]]) -> List[List[int]]:
#         """
#         Optimal for exactly 3 lists: Three-pointer approach (extension of two-pointer).
        
#         Algorithm:
#         1. Use three pointers i, j, k for A, B, C
#         2. At each step, pick interval with smallest start time among A[i], B[j], C[k]
#         3. Merge with result
#         4. Advance corresponding pointer
#         5. Process remaining intervals from whichever lists aren't exhausted
        
#         TC: O(n1 + n2 + n3) where n1, n2, n3 are lengths of A, B, C
#             - Single pass through all three lists
#             - Each interval processed exactly once
        
#         SC: O(1) auxiliary space (output doesn't count)
        
#         Why this is optimal for K=3:
#         - No heap overhead (heap is overkill for just 3 lists)
#         - Simple comparison of 3 values
#         - Clean, easy to understand
#         - Same O(N) time as heap but with less overhead
#         """
#         # Base cases
#         if not A and not B and not C:
#             return []
#         if not A and not B:
#             return C
#         if not A and not C:
#             return B
#         if not B and not C:
#             return A
        
#         result = []
#         i, j, k = 0, 0, 0  # Three pointers
        
#         # Phase 1: While ALL three lists have items
#         while i < len(A) and j < len(B) and k < len(C):
#             # Pick interval with smallest start time
#             if A[i][0] <= B[j][0] and A[i][0] <= C[k][0]:
#                 curr = A[i]
#                 i += 1
#             elif B[j][0] <= A[i][0] and B[j][0] <= C[k][0]:
#                 curr = B[j]
#                 j += 1
#             else:
#                 curr = C[k]
#                 k += 1
            
#             self._try_merge(result, curr)
        
#         # Phase 2: Two lists remaining - use two-pointer logic
#         # At this point, at least one list is exhausted
        
#         # Case 1: A and B remain (C exhausted)
#         while i < len(A) and j < len(B):
#             if A[i][0] <= B[j][0]:
#                 curr = A[i]
#                 i += 1
#             else:
#                 curr = B[j]
#                 j += 1
#             self._try_merge(result, curr)
        
#         # Case 2: A and C remain (B exhausted)
#         while i < len(A) and k < len(C):
#             if A[i][0] <= C[k][0]:
#                 curr = A[i]
#                 i += 1
#             else:
#                 curr = C[k]
#                 k += 1
#             self._try_merge(result, curr)
        
#         # Case 3: B and C remain (A exhausted)
#         while j < len(B) and k < len(C):
#             if B[j][0] <= C[k][0]:
#                 curr = B[j]
#                 j += 1
#             else:
#                 curr = C[k]
#                 k += 1
#             self._try_merge(result, curr)
        
#         # Phase 3: One list remaining
#         while i < len(A):
#             self._try_merge(result, A[i])
#             i += 1
        
#         while j < len(B):
#             self._try_merge(result, B[j])
#             j += 1
        
#         while k < len(C):
#             self._try_merge(result, C[k])
#             k += 1
        
#         return result

#     def _try_merge(self, result: List[List[int]], curr: List[int]) -> None:
#         """Helper: Try to merge interval with result"""
#         if result and curr[0] <= result[-1][1]:
#             result[-1][1] = max(result[-1][1], curr[1])
#         else:
#             result.append(curr[:])


# Variant : Merge k sorted intervals

# class Solution:
#     def mergeKIntervalLists_bruteforce(self, lists: List[List[List[int]]]) -> List[List[int]]:
#         """
#         Brute Force: Combine all lists, sort, then merge.
        
#         Algorithm:
#         1. Combine all K lists into one big list
#         2. Sort by start time
#         3. Merge overlapping intervals (LC 56 logic)
        
#         TC: O(N log N) where N = total number of intervals across all K lists, N = len(list[0]) + len(list[1]) + ... + len(list[K-1])
#             - Combining: O(N)
#             - Sorting: O(N log N) - dominates
#             - Merging: O(N)
        
#         SC: O(N) - combined array + Timsort space
        
#         Why is this suboptimal?
#         - Each individual list is ALREADY sorted!
#         - We're re-sorting data that's already sorted
#         - Like taking K sorted decks, mixing them, then re-sorting
#         """
#         if not lists:
#             return []
        
#         # Step 1: Combine all lists
#         all_intervals = []
#         for lst in lists:
#             all_intervals.extend(lst)
        
#         if not all_intervals:
#             return []
        
#         # Step 2: Sort by start time (even though each list is already sorted!)
#         all_intervals.sort(key=lambda x: x[0])
        
#         # Step 3: Merge overlapping intervals (LC 56)
#         merged = [all_intervals[0]]
#         for start, end in all_intervals[1:]:
#             if start <= merged[-1][1]:
#                 merged[-1][1] = max(merged[-1][1], end)
#             else:
#                 merged.append([start, end])
        
#         return merged
    
#     def mergeKIntervalLists_heap(self, lists: List[List[List[int]]]) -> List[List[int]]:
#         """
#         Optimal: K-way merge using min-heap (like merge K sorted arrays).
        
#         Algorithm:
#         1. Use min-heap to track next interval from each list
#         2. Extract minimum interval (by start time)
#         3. Try to merge with result
#         4. Add next interval from same list to heap
#         5. Repeat until heap is empty
        
#         TC: O(N log K) where N = total intervals, K = number of lists
#             - Each interval: extract from heap O(log K) + insert to heap O(log K)
#             - Total: N intervals × O(log K) = O(N log K)
#             - Much better than O(N log N) for brute force when K << N!
        
#         SC: O(K) - heap size is at most K (one interval per list)
        
#         Why is this better?
#         - Leverages the fact that each list is already sorted
#         - Only need to track K items in heap (not all N intervals)
#         - Similar to merge step in merge sort, but for K lists instead of 2
#         """
#         if not lists:
#             return []
        
#         # Min-heap: (start_time, end_time, list_index, interval_index)
#         heap = []
        
#         # Initialize heap with first interval from each list
#         for i, lst in enumerate(lists):
#             if lst:  # Check list is not empty
#                 # Push: (start, end, which list, which interval in that list)
#                 heapq.heappush(heap, (lst[0][0], lst[0][1], i, 0))
        
#         result = []
        
#         # Process intervals in sorted order
#         while heap:
#             # Extract interval with minimum start time
#             start, end, list_idx, interval_idx = heapq.heappop(heap)
#             curr_interval = [start, end]
            
#             # Try to merge with last result interval
#             if result and curr_interval[0] <= result[-1][1]:
#                 # Overlap - merge
#                 result[-1][1] = max(result[-1][1], curr_interval[1])
#             else:
#                 # No overlap - add new interval
#                 result.append(curr_interval)
            
#             # Add next interval from the same list to heap
#             next_idx = interval_idx + 1
#             if next_idx < len(lists[list_idx]):
#                 next_interval = lists[list_idx][next_idx]
#                 heapq.heappush(heap, (next_interval[0], next_interval[1], list_idx, next_idx))
        
#         return result
    
#     def mergeKIntervalLists_sequential(self, lists: List[List[List[int]]]) -> List[List[int]]:
#         """
#         Alternative: Sequential merging (merge lists one by one).
        
#         Algorithm:
#         1. Start with first list as result
#         2. Merge result with list 2 (using two-pointer from earlier)
#         3. Merge result with list 3
#         4. Continue until all K lists merged

#         Time Complexity: O(NK)
#         - N = total number of intervals across all lists
#         - K = number of lists
#         - Each merge step reprocesses all previously merged intervals
#         - In the worst case (no overlaps), intervals persist and get reprocessed up to K times

#         Space Complexity: O(N)
#         - Result list can contain up to N intervals
#         - Output space is required and not considered extra
        
#         When to use?
#         - K is very small (2-3 lists)
#         - Simpler to implement than heap
#         - Reuses two-pointer merge logic
#         """
#         if not lists:
#             return []
        
#         # Filter out empty lists
#         non_empty = [lst for lst in lists if lst]
#         if not non_empty:
#             return []
        
#         # Start with first list
#         result = non_empty[0]
        
#         # Sequentially merge with each remaining list
#         for i in range(1, len(non_empty)):
#             result = self._merge_two_lists(result, non_empty[i])
        
#         return result
    
#     def _merge_two_lists(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
#         """Helper: Merge two sorted interval lists (from earlier problem)"""
#         if not A:
#             return B
#         if not B:
#             return A
        
#         result = []
#         i, j = 0, 0
        
#         # Phase 1: Both active
#         while i < len(A) and j < len(B):
#             if A[i][0] <= B[j][0]:
#                 curr = A[i]
#                 i += 1
#             else:
#                 curr = B[j]
#                 j += 1
            
#             self._try_merge(result, curr)
        
#         # Phase 2: Remaining
#         while i < len(A):
#             self._try_merge(result, A[i])
#             i += 1
        
#         while j < len(B):
#             self._try_merge(result, B[j])
#             j += 1
        
#         return result
    
#     def _try_merge(self, result: List[List[int]], curr: List[int]) -> None:
#         """Helper: Try to merge interval with result"""
#         if result and curr[0] <= result[-1][1]:
#             result[-1][1] = max(result[-1][1], curr[1])
#         else:
#             result.append(curr[:])
 



        