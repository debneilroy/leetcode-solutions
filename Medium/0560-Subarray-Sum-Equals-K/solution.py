"""
LeetCode 560. Subarray Sum Equals K
Difficulty: Medium
URL: https://leetcode.com/problems/subarray-sum-equals-k/
"""

# Brute Force (TC : O(n^2)  SC : O(1))

# def subarraySum_bruteforce(nums, k):
#     """
#     Brute force approach - check all possible subarrays.
#     Time Complexity: O(n²)
#     Space Complexity: O(1)
#     """
#     count = 0
#     n = len(nums)
    
#     for i in range(n):
#         current_sum = 0
#         for j in range(i, n):
#             current_sum += nums[j]
#             if current_sum == k:
#                 count += 1
    
#     return count

# Hashmap Approach (whenever sums has increased by a value of k, we've found a subarray of sums=k)
# Hashmap has to be initialised with 0 (e.g, nums = [1,2,1,3], k = 3)
# https://leetcode.com/problems/subarray-sum-equals-k/solutions/341399/python-clear-explanation-with-code-and-example/

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Find the total number of continuous subarrays whose sum equals k.
        
        Time Complexity: O(n) - single pass through array
        Space Complexity: O(n) - hash map stores up to n cumulative sums
        
        Args:
            nums: List of integers (can contain positive, negative, and zero)
            k: Target sum (can be any integer: positive, negative, or zero)
        
        Returns:
            int: Count of subarrays whose sum equals k
        
        Constraints:
            - Works for ANY integer values in nums (positive, negative, zero)
            - Works for ANY integer value of k (positive, negative, zero)
            - This is the OPTIMAL solution for mixed/negative numbers
            - For ONLY positive integers: sliding window is O(1) space alternative
            - For ONLY negative integers: sliding window with reverse logic is O(1) space
        """
        # Base case: empty array
        if not nums:
            return 0

        # Hash map to store cumulative sum frequencies
        # Key: cumulative sum, Value: frequency (count of times this sum occurred)
        # Initialize with {0: 1} to handle subarrays starting from index 0
        # 
        # WHY {0: 1}? Example: nums = [3, 2, 1], k = 3
        #   At i=0: cumulative_sum = 3
        #   We check if (3 - 3) = 0 exists in sum_count
        #   Since sum_count[0] = 1, we find 1 valid subarray: [3]
        #   This represents: "There's 1 way to have sum 0" (the empty prefix before index 0)
        #
        # Another example: nums = [1, 2, 3], k = 6
        #   At i=2: cumulative_sum = 6
        #   We check if (6 - 6) = 0 exists in sum_count
        #   Since sum_count[0] = 1, we find the subarray [1, 2, 3] starting from index 0
        #
        # Without {0: 1}, we'd miss all subarrays that start from index 0!
        sum_count = {0: 1}  

        cumulative_sum = 0
        result = 0
        
        for num in nums:
            # Update cumulative sum
            cumulative_sum += num
            
            # Check if (cumulative_sum - k) exists in hash map
            # This means there's a subarray ending at current position with sum k
            if (cumulative_sum - k) in sum_count:
                result += sum_count[cumulative_sum - k]
            
            # Add current cumulative sum to hash map
            sum_count[cumulative_sum] = sum_count.get(cumulative_sum, 0) + 1
            # if cumulative_sum in sum_count:
            #     sum_count[cumulative_sum] += 1
            # else:
            #     sum_count[cumulative_sum] = 1
        
        return result

# Find all subarray indices

# def find_all_subarray_indices(nums, k):
#     """
#     Find ALL subarrays with sum equal to k (returns only start and end indices).

#     ============================================================================
#     COMPLEXITY SUMMARY
#     ============================================================================
    
#     Time Complexity: O(n + m) where n = len(nums), m = number of valid subarrays
#         - Best/Average case: O(n) when few valid subarrays exist
#         - Worst case: O(n²) when m = n(n+1)/2 (example: [0,0,0,0] with k=0)
    
#     Space Complexity: O(n + m)
#         - Hashmap: O(n) always
#         - Result: O(m) tuples, worst case O(n²)
#         - Total worst case: O(n²)
    
#     ============================================================================
#     WHY O(n + m) AND NOT O(n × m)?
#     ============================================================================
    
#     KEY INSIGHT: Inner loop doesn't run m times at EACH iteration.
#     Instead, it runs a TOTAL of m times ACROSS ALL iterations combined.
    
#     The algorithm has two parts:
#         1. Outer loop: runs exactly n times
#         2. Inner loop: total executions across all iterations = m
    
#     Example: nums = [0,0,0,0], k = 0
#         Iteration 0: inner loop runs 1 time  → 1 subarray found
#         Iteration 1: inner loop runs 2 times → 2 more subarrays
#         Iteration 2: inner loop runs 3 times → 3 more subarrays
#         Iteration 3: inner loop runs 4 times → 4 more subarrays
#         Total: 1+2+3+4 = 10 = m (not n×m = 4×10 = 40!)
    
#     Total work = Outer loop work + Inner loop work = O(n) + O(m) = O(n + m)
    
#     If it were O(n × m), the inner loop would run m times at EVERY iteration,
#     but it doesn't - it runs different amounts at each iteration, totaling m.
    
#     ============================================================================
#     WHY WORST CASE IS O(n²)?
#     ============================================================================
    
#     An array of length n has n(n+1)/2 = O(n²) possible subarrays.
#     When ALL are valid (like [0,0,0,0] with k=0), we must output all O(n²) of them.
    
#     Example: n=4 → 10 subarrays
#         Length 1: [0], [0], [0], [0]                    → 4 subarrays
#         Length 2: [0,0], [0,0], [0,0]                   → 3 subarrays
#         Length 3: [0,0,0], [0,0,0]                      → 2 subarrays
#         Length 4: [0,0,0,0]                             → 1 subarray
#         Total: 4+3+2+1 = 10 = n(n+1)/2
    
#     This is called "output-sensitive" time complexity - depends on output size.
    
#     ============================================================================

#     ============================================================================
#     WHY WORST CASE SPACE IS O(n²)?
#     ============================================================================
    
#     We use TWO data structures:
    
#     1. HASHMAP (sum_to_indices): O(n) space
#        - Stores cumulative sums and their positions
#        - Even in worst case (e.g., [0,0,0,0]), stores at most n+1 positions total
#        - Example: {0: [-1, 0, 1, 2, 3]} → 5 integers = O(n)
    
#     2. RESULT LIST: O(m) space, worst case O(n²)
#        - Stores (start_index, end_index) tuples
#        - Each tuple is 2 integers = O(1) space
#        - Number of tuples = m (number of valid subarrays)
       
#        Example: nums = [0,0,0,0], k = 0
#        Result = [(0,0), (0,1), (1,1), (0,2), (1,2), (2,2), (0,3), (1,3), (2,3), (3,3)]
#        → 10 tuples × 2 integers = 20 integers total
       
#        In worst case: m = n(n+1)/2 = O(n²)
#        For n=4: 10 tuples = 4×5/2
#        For n=100: 5,050 tuples = 100×101/2
       
#        Space for result = m tuples × O(1) per tuple = O(m) = O(n²)
    
#     TOTAL SPACE = Hashmap + Result = O(n) + O(n²) = O(n²)
    
#     The O(n²) space comes from storing all the INDEX PAIRS in the result list,
#     not from the hashmap!
    
#     This is called "output-sensitive" space complexity - depends on output size.
    
#     ============================================================================
    
#     Args:
#         nums: List of integers (can be positive, negative, zero)
#         k: Target sum (can be any integer)

#     Returns:
#         List of tuples (start_index, end_index) for all valid subarrays
#     """
    
#     result = []
#     cumulative_sum = 0
    
#     # Maps cumulative_sum → list of indices where this sum occurred, uses defaultdict(list) for    automatic empty list creation
#     # With regular dict: sum_to_indices = {}
#     sum_to_indices = defaultdict(list)
    
#     # Initialize with {0: [-1]} to handle subarrays starting from index 0
#     #
#     # WHY -1 instead of 0 or 1?
#     # 
#     # The -1 represents a CONCEPTUAL POSITION "before the array starts"
#     # (not an actual array index). This is needed because when we find a match,
#     # we calculate the subarray start as: (start_idx + 1)
#     #
#     # Example: nums = [3, 2, 1], k = 3
#     #   At i=0: cumulative_sum = 3
#     #   We look for (3 - 3) = 0 in the map
#     #   Found! sum_to_indices[0] = [-1]
#     #   
#     #   Subarray indices: (start_idx + 1) to i
#     #                   = (-1 + 1) to 0
#     #                   = 0 to 0
#     #   Subarray: nums[0:1] = [3] ✓ Correct!
#     #
#     # If we used 0 instead of -1:
#     #   Subarray indices: (0 + 1) to 0 = 1 to 0
#     #   Subarray: nums[1:1] = [] ✗ Wrong! (empty subarray)
#     #
#     # If we used 1 instead of -1:
#     #   Subarray indices: (1 + 1) to 0 = 2 to 0
#     #   Subarray: nums[2:1] = [] ✗ Wrong! (empty subarray)
#     #
#     # The math works out: To get subarray starting at index 0,
#     # we need start_idx + 1 = 0, therefore start_idx = -1
#     #
#     # Conceptually: -1 means "position before array" with cumulative_sum = 0
#     # With regular dict: sum_to_indices[0] = [-1]  (same initialization)
#     sum_to_indices[0].append(-1)

#     for i, num in enumerate(nums):
#         cumulative_sum += num
        
        
#         if cumulative_sum - k in sum_to_indices: # Note: With defaultdict(list), this check is optional (missing keys return [])
#             # Inner loop: Runs different amounts at each iteration
#             # Total across ALL iterations = m (number of valid subarrays)
#             # NOT m times at each iteration!
#             #
#             # Example: [0,0,0,0], k=0
#             #   i=0: runs 1 time, i=1: runs 2 times, i=2: runs 3 times, i=3: runs 4 times
#             #   Total: 1+2+3+4 = 10 = m (not 4×10!)
#             for start_idx in sum_to_indices[cumulative_sum - k]:
#                 result.append((start_idx + 1, i))

#         # Record current position for this cumulative sum
#         # Note: Works directly with defaultdict(list) - auto-creates empty list if needed
#         sum_to_indices[cumulative_sum].append(i)

#         # With regular dict, need one of these approaches:
#         # Option 1 (explicit check):
#         #   if cumulative_sum not in sum_to_indices:
#         #       sum_to_indices[cumulative_sum] = []
#         #   sum_to_indices[cumulative_sum].append(i)
#         #
#         # Option 2 (setdefault):
#         #   sum_to_indices.setdefault(cumulative_sum, []).append(i)
#         #
#         # Option 3 (get with default):
#         #   sum_to_indices[cumulative_sum] = sum_to_indices.get(cumulative_sum, []) + [i]

#     return result

# # Find all subarrays

# def find_all_subarrays(nums, k):
#     """
#     Find ALL subarrays with sum equal to k (returns actual subarray elements).

#     ============================================================================
#     COMPLEXITY SUMMARY
#     ============================================================================
    
#     Time Complexity: O(n + m·L) where:
#         - n = len(nums)
#         - m = number of valid subarrays
#         - L = average length of valid subarrays
        
#         Best case: O(n) when few/short subarrays exist
#         Worst case: O(n³) when m = O(n²) and L = O(n)
    
#     Space Complexity: O(n + m·L)
#         - Hashmap: O(n)
#         - Result: O(m·L) = total elements across all subarrays
#         - Worst case: O(n³)
    
#     ============================================================================
#     WHY O(n³) AND NOT O(n²)?
#     ============================================================================
    
#     The difference from returning indices:
    
#     RETURNING INDICES:
#         - Each match: append (start, end) tuple → O(1)
#         - m matches × O(1) = O(m)
#         - Worst case: O(n²) when m = n(n+1)/2
    
#     RETURNING SUBARRAYS:
#         - Each match: slice nums[start:end+1] → O(length)
#         - m matches × O(average length) = O(m·L)
#         - Worst case: O(n³) when m = O(n²) and L = O(n)
    
#     Example worst case: nums = [0,0,0,0], k = 0
#         All n(n+1)/2 = 10 subarrays are valid:
#         [0]           length 1   \
#         [0]           length 1    |
#         [0]           length 1    |
#         [0]           length 1    | Total: 10 subarrays
#         [0,0]         length 2    |
#         [0,0]         length 2    |
#         [0,0]         length 2    /
#         [0,0,0]       length 3
#         [0,0,0]       length 3
#         [0,0,0,0]     length 4
        
#         Total elements copied: 1+1+1+1+2+2+2+3+3+4 = 20
#         Formula: n(n+1)(n+2)/6 = 4×5×6/6 = 20
        
#         For general n: n(n+1)(n+2)/6 = O(n³)
    
#     ============================================================================
#     COMPARISON: INDICES vs SUBARRAYS
#     ============================================================================
    
#     Returning INDICES:
#         Time: O(n²) worst case
#         Space: O(n²) worst case
#         Each match: O(1) to store tuple
    
#     Returning SUBARRAYS:
#         Time: O(n³) worst case
#         Space: O(n³) worst case
#         Each match: O(length) to copy elements
    
#     Recommendation: Return indices when possible, construct subarrays only if needed
    
#     ============================================================================
    
#     """
    
#     result = []
#     cumulative_sum = 0
    
#     sum_to_indices = defaultdict(list)
    
#     sum_to_indices[0].append(-1)

#     for i, num in enumerate(nums):
#         cumulative_sum += num

#         if cumulative_sum - k in sum_to_indices:
            
#             # For each previous position where we saw (cumulative_sum - k),
#             # we have a valid subarray from that position+1 to current position i
#             #
#             # TIME COST: This inner loop runs m times TOTAL across all iterations
#             # But each iteration also does slicing, which is O(length)
#             #
#             # Example: nums = [0,0,0,0], k = 0
#             #
#             # At each iteration, we create multiple subarrays:
#             #
#             #   i=0: Create 1 subarray
#             #        [0] (length 1)
#             #        Cost: 1
#             #
#             #   i=1: Create 2 subarrays
#             #        [0,0] (length 2)
#             #        [0] (length 1)
#             #        Cost: 2+1 = 3
#             #
#             #   i=2: Create 3 subarrays
#             #        [0,0,0] (length 3)
#             #        [0,0] (length 2)
#             #        [0] (length 1)
#             #        Cost: 3+2+1 = 6
#             #
#             #   i=3: Create 4 subarrays
#             #        [0,0,0,0] (length 4)
#             #        [0,0,0] (length 3)
#             #        [0,0] (length 2)
#             #        [0] (length 1)
#             #        Cost: 4+3+2+1 = 10
#             #
#             # Total slicing cost: 1 + 3 + 6 + 10 = 20 elements copied
#             #
#             # For general n: Total = n(n+1)(n+2)/6 = O(n³)
#             # - We create O(n²) subarrays
#             # - Average length of subarrays: O(n)
#             # - Total elements: O(n²) × O(n) = O(n³)
#             for start_idx in sum_to_indices[cumulative_sum - k]:
#                 # Calculate actual subarray boundaries
#                 start = start_idx + 1  # Actual starting index in array
#                 end = i + 1            # One past ending index (for slicing)
                
#                 # CRITICAL: Slicing creates a COPY of elements
#                 # 
#                 # TIME: O(end - start) = O(length of subarray)
#                 # SPACE: O(end - start) = O(length of subarray)
#                 #
#                 # This is why returning subarrays is O(n³):
#                 # - We have up to O(n²) subarrays in worst case
#                 # - Each can have length up to O(n)
#                 # - Total elements copied: O(n³)
#                 #
#                 # Compare with returning indices:
#                 #   result.append((start_idx + 1, i))  # O(1)
#                 # vs
#                 #   result.append(nums[start:end])     # O(length)
#                 subarray = nums[start:end]
#                 result.append(subarray)

#         # Record current position for this cumulative sum
#         # Allows future iterations to find subarrays ending at later positions
#         sum_to_indices[cumulative_sum].append(i)

#     return result

# Variant 1 : Return True if there exists at least one continuous subarray whose sum equals k.

# def subarraySum_exists(nums, k):
#     """
#     Check if there exists at least one continuous subarray whose sum equals k.
#     WORKS FOR: Mixed positive/negative/zero integers in nums, any integer k
    
#     Time Complexity: O(n) - worst case, but can terminate early
#     Space Complexity: O(n) - worst case for hash set

#     """
#     # Use a set instead of dict since we only need to check existence
#     # Initialize with 0 to handle subarrays starting from index 0
#     # Example: nums=[3,2,1], k=3
#     # At i=0: cumulative_sum=3, we check if (3-3)=0 exists in set
#     #  Since 0 is in the set, we correctly identify that [3] is a valid subarray
#     # Without the 0 initialization, we'd miss subarrays starting from index 0
#     cumulative_sums = {0} 
    
#     cumulative_sum = 0
    
#     for num in nums:
#         cumulative_sum += num
        
#         # Check if (cumulative_sum - k) exists
#         # This means there's a subarray ending at current position with sum k
#         # This relationship holds for ANY integer values (positive, negative, zero)
#         if (cumulative_sum - k) in cumulative_sums:
#             return True
        
#         # Add current cumulative sum to set
#         cumulative_sums.add(cumulative_sum)
    
#     return False

# def subarraySum_exists_bruteforce(nums, k):
#     """
#     Brute force approach for comparison.
#     Time Complexity: O(n²)
#     Space Complexity: O(1)
#     """
#     n = len(nums)
    
#     for i in range(n):
#         current_sum = 0
#         for j in range(i, n):
#             current_sum += nums[j]
#             if current_sum == k:
#                 return True
    
#     return False

# def find_first_subarray_with_sum(nums, k):
#     """
#     Find the first subarray with sum k (mixed positive/negative/zero numbers).
#     Returns the actual subarray, not just boolean.
    
#     Time Complexity: O(n)
#         - Single pass through array: O(n) worst case
#         - Slicing when match found: O(k) where k = subarray length
#         - KEY: Slicing happens ONLY ONCE, then we return immediately
#         - Total: O(n) + O(k) = O(n) since k ≤ n
        
#         WHY NOT O(n²)?
#         - Unlike "find all", we don't slice multiple times
#         - We slice once and return immediately (early termination)
#         - Example: If match found at i=2 in array of n=1000
#           → Only 3 loop iterations + 1 slice = O(3 + slice_length) = O(n)
    
#     Space Complexity: O(n)
#         - Hashmap stores at most n cumulative sums: O(n)
#         - Result subarray: O(k) where k = subarray length, worst case O(n)
#         - Total: O(n)
    
#     COMPARISON WITH OTHER APPROACHES:
#         Find if exists:  O(n) time, O(n) space - no slicing, just return True
#         Find FIRST:      O(n) time, O(n) space - slice ONCE and return
#         Find ALL:        O(n³) time, O(n³) space - slice m times, m = O(n²) worst case
    
#     Args:
#         nums: List of integers (can be positive, negative, zero)
#         k: Target sum (can be any integer)
    
#     Returns:
#         List containing first subarray with sum k, or None if not found
#     """
    
#     # Base case: empty array has no subarrays
#     # Without this check, loop wouldn't run and we'd return None anyway,
#     # but explicit check makes intent clear and avoids unnecessary setup
#     if not nums:
#         return None
    
#     # Map: cumulative_sum → first index where this sum occurred
#     # 
#     # KEY DIFFERENCE from "find all": 
#     #   - This version: stores single int (first occurrence only)
#     #   - "Find all" version: stores list of ints (all occurrences)
#     #
#     # WHY {0: -1}?
#     # - The -1 represents "position before array starts" (conceptual, not actual index)
#     # - Needed to handle subarrays that start from index 0
#     # - When we find a match, we calculate: start = sum_to_index[target] + 1
#     # - For subarray starting at index 0: start = -1 + 1 = 0 ✓
#     #
#     # Example: nums = [5, 3], k = 5
#     #   At i=0: cumulative_sum=5, look for (5-5)=0, found at position -1
#     #   Subarray: from (-1+1) to 0 = nums[0:1] = [5] ✓
#     #
#     # Without {0: -1}:
#     #   At i=0: cumulative_sum=5, look for 0, NOT FOUND
#     #   We'd miss the subarray [5] completely! ✗
#     sum_to_index = {0: -1}
    
#     cumulative_sum = 0
    
#     for i, num in enumerate(nums):
#         cumulative_sum += num
        
#         if (cumulative_sum - k) in sum_to_index:
#             # Found a match! Calculate subarray boundaries
            
#             # start_index = actual starting position in array
#             # We add 1 because sum_to_index stores the position BEFORE the subarray starts
#             #
#             # Example: If sum_to_index[0] = -1, then start = -1 + 1 = 0 (start of array)
#             # Example: If sum_to_index[3] = 2, then start = 2 + 1 = 3
#             start_index = sum_to_index[cumulative_sum - k] + 1
            
#             # end_index = current position (inclusive)
#             # This is the last element of the subarray
#             end_index = i
            
#             # CRITICAL: Slicing happens here - O(end - start + 1) time
#             # BUT this only executes ONCE because we return immediately after!
#             # This is the KEY DIFFERENCE from "find all" where slicing
#             # happens O(n²) times in worst case (once per valid subarray).
#             #
#             # Time for this slice: O(subarray_length) = O(end - start + 1) ≤ O(n)
#             # Since it happens only once: Total algorithm time still O(n)
    
#             # Space for result: O(end - start + 1) = O(subarray_length) ≤ O(n)
#             return nums[start_index:end_index + 1]
        
#         # Store FIRST occurrence of this cumulative sum only
#         # 
#         # WHY check "if not in" before storing?
#         # - We want to keep the FIRST (leftmost) occurrence
#         # - This ensures we find the subarray that appears earliest in the array
#         # - If we overwrote existing values, we'd find later subarrays instead
#         #
#         # Example of why this matters:
#         #   nums = [1, -1, 2], k = 2
#         #
#         #   Without the check (always overwrite):
#         #     i=0: cumulative_sum=1, store {0:-1, 1:0}
#         #     i=1: cumulative_sum=0, OVERWRITE {0:1, 1:0}  ← overwrites -1 with 1
#         #     i=2: cumulative_sum=2, look for 0, found at position 1
#         #          Return nums[2:3] = [2] ✗ (found later subarray)
#         #
#         #   With the check (keep first):
#         #     i=0: cumulative_sum=1, store {0:-1, 1:0}
#         #     i=1: cumulative_sum=0, already exists, DON'T overwrite {0:-1, 1:0}
#         #     i=2: cumulative_sum=2, look for 0, found at position -1
#         #          Return nums[0:3] = [1,-1,2] ✓ (found earlier subarray)
#         #
#         # KEY DIFFERENCE from "find all":
#         #   - "Find all" ALWAYS appends: sum_to_index[cumulative_sum].append(i)
#         #   - "Find first" checks before storing to keep only first occurrence
#         #
#         # TIME: O(1) hash lookup and insert
#         if cumulative_sum not in sum_to_index:
#             sum_to_index[cumulative_sum] = i
    
#     # No valid subarray found after checking entire array
#     return None

# # Variant 2 : There are only positive integers in the array

# # Approach : Two Pointer (sliding window)

# # With only positive integers, the cumulative sum is monotonically increasing. This means:

# # If current_sum > k → we must shrink the window from the left
# # If current_sum < k → we must expand the window to the right
# # If current_sum = k → we found our answer!

# def subarraySum_positive_count(nums, k):
#     """
#     Count number of subarrays with sum k (positive integers only).
#     Uses sliding window technique for optimal space complexity.
    
#     IMPORTANT: Only works for arrays with POSITIVE integers.
#     For mixed positive/negative/zero, must use hash map approach.
     
#     Why sliding window works:
#         Because all numbers are positive:
#             - Expanding the window (right++) strictly increases the sum
#             - Shrinking the window (left++) strictly decreases the sum

#         Therefore
#         - If sum > k → must shrink from left
#         - If sum < k → must expand to right
#         - If sum = k → found valid subarray
    
#     Time Complexity: O(n)
#         - Outer loop: n iterations
#         - Inner while loop: each element removed at most once total
#         - Total: O(2n) = O(n)
    
#     Space Complexity: O(1)
#         - Only uses pointers and counters
#         - No hash map needed
    
#     Args:
#         nums: List of POSITIVE integers only
#         k: Target sum (positive)
    
#     Returns:
#         Count of subarrays with sum equal to k
    
#     Example:
#         nums = [1, 1, 1], k = 2
#         Valid subarrays: [1,1] at (0,1) and [1,1] at (1,2)
#         Returns: 2
#     """
    
#     # Edge cases:
#     # - Empty array: no subarrays possible
#     # - k <= 0: impossible with positive integers
#     if not nums or k <= 0:
#         return 0
    
#     # Sliding window pointers
#     # Window represents contiguous subarray nums[left:right+1]
#     left = 0
    
#     # Sum of current window elements
#     # INVARIANT: current_sum == sum(nums[left:right+1])
#     # This invariant must be maintained at ALL times!
#     current_sum = 0
    
#     # Count of valid subarrays found
#     count = 0
    
#     for right in range(len(nums)):
#         # Expand: Add current element to window
#         # Window is now nums[left:right+1]
#         current_sum += nums[right]
        
#         # Shrink: Remove elements from left while sum exceeds k
#         # 
#         # Q: Can we use 'if' instead of 'while'?
#         # A: Using 'while' is necessary for correctness and clarity:
#         #
#         # 1. CORRECTNESS: We need to shrink UNTIL sum <= k
#         #    - 'if' only shrinks once, may leave sum > k
#         #    - Example: nums=[10, 1, 2], k=3
#         #      right=0: sum=10, 'if' shrinks once → sum still > k (might be 0 or positive)
#         #      'while' keeps shrinking until sum <= k
#         #
#         # 2. SEMANTIC CLARITY: 'while' expresses "keep shrinking until condition met"
#         #    - More readable and follows standard sliding window pattern
#         #
#         # 3. GUARANTEES: After 'while' loop, we know for certain sum <= k
#         #    - With 'if', no such guarantee
#         #
#         # Note: 'if' might technically work due to how we add elements in next iteration,
#         # but 'while' is the correct, clear, and robust choice.

#         # If all integers are negative, just do while current_sum < k, rest of the code is the same.
#         while current_sum > k:
#             # CRITICAL: Subtract nums[left] BEFORE incrementing left
#             # This maintains the invariant: current_sum == sum(nums[left:right+1])
#             # 
#             # We are about to move left pointer (left += 1)
#             # This removes nums[left] from the window
#             # So we MUST subtract it from current_sum
#             # 
#             # What happens WITHOUT this subtraction?
#             # 
#             # Example: nums = [5, 1, 2], k = 3
#             #   right=0: sum=5, left=0
#             #   while 5 > 3:
#             #     left=1  (WITHOUT subtracting nums[0]=5)
#             #   current_sum is STILL 5!
#             #   But window is now nums[1:1]=[1], which has actual sum=1
#             #   Invariant BROKEN: current_sum=5 but actual window sum=1
#             # 
#             #   right=1: sum=5+1=6 (WRONG! We're adding to corrupted sum)
#             #   Actual window should be [1,2] with sum=3
#             #   But our sum=6 is completely wrong!
#             #   Algorithm fails!
#             # 
#             # Correct behavior WITH subtraction:
#             #   right=0: sum=5
#             #   while 5 > 3:
#             #     sum=5-5=0, left=1
#             #   sum=0 reflects empty window (nothing before left=1)
#             # 
#             #   right=1: sum=0+1=1 (adding nums[1]=1)
#             #   Window=[1] with sum=1 ✓ Correct!
#             # 
#             # Without maintaining this invariant, the entire algorithm collapses!
#             current_sum -= nums[left]  # Maintain invariant
#             left += 1
        
#         # Check if current window has sum exactly equal to k
#         if current_sum == k:
#             # Found a valid subarray at nums[left:right+1]
#             count += 1
            
#             # CRITICAL: Move left pointer to continue searching for more subarrays
#             # 
#             # We must update current_sum to maintain the invariant:
#             #   current_sum == sum(nums[left:right+1])
#             # 
#             # After moving left, the window becomes nums[left+1:right+1]
#             # So we must subtract nums[left] from current_sum
#             # 
#             # Without this subtraction:
#             # - current_sum would still include the old nums[left]
#             # - But the window is now nums[left+1:right+1]
#             # - Invariant BROKEN: current_sum ≠ actual window sum
#             # - Algorithm produces WRONG results!
#             # 
#             # Example of failure without subtraction:
#             #   nums = [1, 2, 1], k = 3
#             #   right=1: sum=3, window=[1,2], MATCH! left→1 but sum still 3
#             #   right=2: sum=3+1=4 (WRONG! window [2,1] should have sum=3, not 4)
#             #   State corrupted, wrong answer!
#             # 
#             # With subtraction:
#             #   nums = [1, 2, 1], k = 3
#             #   right=1: sum=3, MATCH! sum=3-1=2, left=1
#             #   right=2: sum=2+1=3, window=[2,1], correct state maintained ✓
#             current_sum -= nums[left]  # Maintain invariant
#             left += 1
    
#     return count

# def subarraySum_positive_only(nums, k):
#     """
#     Check if there exists a subarray with sum k when all numbers are positive.
    
#     Time Complexity: O(n)
#     Space Complexity: O(1)
#     """
#     if not nums or k <= 0:
#         return False
    
#     left = 0
#     current_sum = 0
    
#     for right in range(len(nums)):
#         # Expand window by adding current element
#         current_sum += nums[right]
        
#         # Shrink window from left while sum is too large
#         while current_sum > k:
#             current_sum -= nums[left]
#             left += 1
        
#         # Check if we found the target sum
#         if current_sum == k:
#             return True
    
#     return False

# def get_subarray_with_sum(nums, k):
#     """
#     Return the actual subarray with sum k (if it exists).

#     Time Complexity: O(n)
#         - Single pass through array
#         - Each element added once, removed at most once
    
#     Space Complexity: O(1) + O(m) where m = length of returned subarray
#         Algorithm space: O(1)
#             - Only uses: left pointer, right pointer, current_sum
#             - No additional data structures (no hash map, no array)
        
#         Output space: O(m) where m = length of subarray found
#             - When we find a match, we create a copy: nums[left:right+1]
#             - This subarray has length m = (right - left + 1)
#             - In worst case: m = n (entire array is the answer)
#             - Example: nums=[1,2,3], k=6 → returns [1,2,3] which is O(3)=O(n)
        
#         Total: O(1) + O(m) = O(m)
        
#     Note: We don't count input array nums in space complexity (standard practice)
#     """
#     if not nums or k <= 0:
#         return None
    
#     left = 0
#     current_sum = 0
    
#     for right in range(len(nums)):
#         current_sum += nums[right]
        
#         while current_sum > k:
#             current_sum -= nums[left]
#             left += 1
        
#         if current_sum == k:
#             return nums[left:right+1]  # Return the subarray
    
#     return None


# def get_all_subarrays_with_sum(nums, k):
#     """
#     Return ALL subarrays with sum k (positive integers only).
#     Uses sliding window technique.
    
#     IMPORTANT: Only works for arrays with POSITIVE integers.
#     For mixed positive/negative/zero, must use hash map approach.
    
#     ============================================================================
#     TIME COMPLEXITY: O(n²) worst case
#     ============================================================================
    
#     Analysis:
#         - Sliding window traversal: O(n)
#         - Number of matches (m): up to O(n) 
#         - Slicing cost per match: O(length of subarray)
#         - Total slicing: O(m × average_length)
    
#     Best case: O(n) when k is small constant
#         Example: nums = [1,1,1,1,1,1,1,1], k = 2
#         - Matches: 7
#         - Each slice length: 2
#         - Total: 7 × 2 = 14 = O(n)
    
#     Worst case: O(n²) when k ≈ n/2
#         Example: nums = [1,1,1,1,1,1,1,1], k = 4
#         - Matches: 5 (approximately n - k + 1)
#         - Each slice length: 4 (which is O(n))
#         - Total: 5 × 4 = 20 = O(n²)
        
#         General formula when k = Θ(n):
#         - Matches: O(n)
#         - Each slice: O(n)
#         - Total: O(n) × O(n) = O(n²)
    
#     ============================================================================
#     SPACE COMPLEXITY: O(n²) worst case
#     ============================================================================
    
#     Algorithm space: O(1) - just pointers
    
#     Output space: O(m × average_length)
#         - Store m subarrays
#         - Each subarray is a copy of elements
        
#         Best case: O(n) when k is small
#         Worst case: O(n²) when k ≈ n/2
        
#         Example: nums = [1,1,1,1,1,1,1,1], k = 4
#         - 5 subarrays, each length 4
#         - Total elements: 5 × 4 = 20 = O(n²)
    
#     """
    
#     # Edge cases: empty array or impossible k
#     if not nums or k <= 0:
#         return []
    
#     result = []  # Store all valid subarrays
#     left = 0     # Left pointer of sliding window
#     current_sum = 0  # Sum of current window
    
#     # INVARIANT: current_sum == sum(nums[left:right+1])
    
#     for right in range(len(nums)):
#         # Expand window: add current element
#         current_sum += nums[right]
        
#         while current_sum > k:
#             current_sum -= nums[left]  # Maintain invariant
#             left += 1
        
#         if current_sum == k:
#             # Found a valid subarray at nums[left:right+1]
#             # Create a copy and add to result
#             # SLICING COST: O(right - left + 1) = O(length of subarray)
#             result.append(nums[left:right+1])
            
#             # Move left pointer to continue searching for more subarrays
#             # Must maintain invariant: current_sum == sum(nums[left:right+1])
#             current_sum -= nums[left]  # Maintain invariant
#             left += 1
    
#     return result


# def get_all_subarray_indices_with_sum(nums, k):
#     """
#     Return indices of ALL subarrays with sum k (positive integers only).
#     Uses sliding window technique.
    
#     IMPORTANT: Only works for arrays with POSITIVE integers.
#     For mixed positive/negative/zero, must use hash map approach.
    
#     ============================================================================
#     TIME COMPLEXITY: O(n) always
#     ============================================================================
    
#     Analysis:
#         - Sliding window traversal: O(n)
#         - Number of matches (m): up to O(n)
#         - Storing each match: O(1) per match (just 2 integers)
#         - Total: O(n) + O(m) × O(1) = O(n)
    
#     KEY DIFFERENCE from returning actual subarrays:
#         - No slicing cost! Just store (start, end) tuples
#         - Each tuple is O(1) to create and store
#         - Much faster than creating subarray copies
    
#     Example: nums = [1,1,1,1,1,1,1,1], k = 4
#         - Matches: 5
#         - Each stores 2 integers: (start, end)
#         - Total: 5 × O(1) = O(5) = O(n)
        
#     Compare with returning subarrays:
#         - Same 5 matches
#         - Each creates copy of 4 elements
#         - Total: 5 × 4 = 20 = O(n²) when k ≈ n/2
    
#     ============================================================================
#     SPACE COMPLEXITY: O(n) worst case
#     ============================================================================
    
#     Algorithm space: O(1) - just pointers
    
#     Output space: O(m) where m = number of matches
#         - Store m tuples (start_index, end_index)
#         - Each tuple is O(1) space (just 2 integers)
#         - Maximum m = O(n) matches
#         - Total: O(n) in worst case
        
#     """
#     if not nums or k <= 0:
#         return []
    
#     result = []  
#     left = 0     
#     current_sum = 0  
    
#     for right in range(len(nums)):
#         current_sum += nums[right]
        
#         while current_sum > k:
#             current_sum -= nums[left]  
#             left += 1
        
#         if current_sum == k:
#             # Found a valid subarray at indices [left, right]
#             # Store just the indices - O(1) operation!
#             # No slicing cost, no copying elements
#             result.append((left, right))
            
#             current_sum -= nums[left]  
#             left += 1
    
#     return result