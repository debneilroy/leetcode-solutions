"""
LeetCode 1. Two Sum
Difficulty: Easy
URL: https://leetcode.com/problems/two-sum/
"""

# Brute Force : Use two nested loops to check every possible pair. The outer loop iterates through each element, and the inner loop checks all subsequent elements. If any pair sums to the target, return their indices. 

# class Solution:
#     """
#     Time: O(n²) - checking all pairs
#     Space: O(1) - no extra data structures
#     """
#     def twoSum(self, nums, target):
#         # Check every possible pair of numbers
#         for i in range(len(nums)):
#             for j in range(i + 1, len(nums)):
#                 if nums[i] + nums[j] == target:
#                     return [i, j]
        
#         return []  # No solution found



class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Find two numbers in the array that sum to the target value.
        
        Time Complexity: O(n)
        - Single pass through the array
        - Hash map lookup and insertion are O(1) operations
        
        Space Complexity: O(n)
        - Hash map stores at most n elements in worst case
        """
        # Dictionary to store number and its index
        seen = {}
        
        for i, num in enumerate(nums):
            # Calculate what number we need to reach the target
            complement = target - num
            
            # If we've seen the complement before, we found our answer
            if complement in seen:
                return [seen[complement], i]
            
            # Store the current number and its index
            seen[num] = i
        
        return []  # No solution found (though problem guarantees one exists)


# Variant 1 : Return True if there exists a pair of numbers that add up to target, else return False.

# class Solution:
#     def twoSum(self, nums, target):
#         """
#         Check if there exists a pair of numbers that sum to the target.
        
#         Time Complexity: O(n)
#         - Single pass through the array
#         - Hash set lookup and insertion are O(1) operations
        
#         Space Complexity: O(n)
#         - Hash set stores at most n elements in worst case
#         """
#         seen = set()
        
#         for num in nums:
#             complement = target - num
            
#             # If we've seen the complement, a valid pair exists
#             if complement in seen:
#                 return True
            
#             # Add current number to the set
#             seen.add(num)
        
#         return False


# Variant 2 : Given an array of domino pairs dominoes where each domino is [a, b], and an integer target, return the number of unique domino pairs [a1, a2] and [b1, b2] where:

# a1 + b1 = target (first elements sum to target)
# a2 + b2 = target (second elements sum to target)
# You cannot use the same domino with itself

# Note: Numbers are limited to digits 0-9.

# Example 1:
# Input: dominoes = [[1,2],[9,8],[3,4],[7,6],[1,2]], target = 10
# Output: 3

# Valid pairs:
# 1. [1,2] and [9,8]: 1+9=10, 2+8=10 ✓
# 2. [3,4] and [7,6]: 3+7=10, 4+6=10 ✓
# 3. [1,2] (index 0) and [9,8]: already counted
# 4. [1,2] (index 4) and [9,8]: 1+9=10, 2+8=10 ✓

# Total: 3 pairs

# Example 2:
# Input: dominoes = [[1,2],[3,4],[5,6]], target = 10
# Output: 0

# Explanation:
# - [1,2] needs [9,8] (not present)
# - [3,4] needs [7,6] (not present)
# - [5,6] needs [5,4] (not present)
# No valid pairs exist.

# Example 3:
# Input: dominoes = [[5,5],[5,5],[5,5]], target = 10
# Output: 3

# Explanation:
# All dominoes are [5,5], and each needs [5,5] as complement.
# Pairs: (0,1), (0,2), (1,2)
# Total: 3 pairs


# Approach : Using defaultdict

# def numEquivDominoPairs(dominoes, target):
#     """
#     Count pairs of dominoes where corresponding elements sum to target.
#     Uses defaultdict for cleaner frequency tracking without manual checking.
    
#     Time Complexity: O(n)
#     - Single pass through the dominoes array: O(n)
#     - defaultdict lookup: O(1) average case
#     - defaultdict insertion/update: O(1) average case
    
#     Space Complexity: O(n)
#     - defaultdict stores at most n unique domino configurations
#     - Each tuple key takes O(1) space
    
#     Args:
#         dominoes: List of domino pairs [a, b] where 0 <= a, b <= 9
#         target: Target sum value
        
#     Returns:
#         Integer - count of valid domino pairs
#     """
#     # defaultdict(int) automatically initializes missing keys to 0
#     domino_to_freq = defaultdict(int)
#     result = 0
    
#     for a1, a2 in dominoes:
#         # Calculate the complement domino needed
#         complement = (target - a1, target - a2)
        
#         # Add frequency of complement (0 if not seen before)
#         # No need to check if key exists - defaultdict handles it
#         result += domino_to_freq[complement]
        
#         # Increment frequency of current domino
#         # If first occurrence, defaultdict returns 0, then we add 1
#         domino_to_freq[(a1, a2)] += 1
    
#     return result

# Find all domino pair indices

# from collections import defaultdict

# def findAllDominoPairIndices(dominoes, target):
#     """
#     Find indices of all pairs of dominoes where corresponding elements sum to target.
    
#     Time Complexity: O(n + p)
#         - n = number of dominoes
#         - p = number of valid pairs found
#         - Outer loop: O(n) - iterate through all dominoes once
#         - Inner loop: O(p) total - across all iterations, we create p pairs
#         - Dictionary operations (lookup, insert): O(1) average case
#         - Total: O(n) + O(p) = O(n + p)
        
#         Best case: O(n) when no pairs exist (p = 0)
#         Worst case: O(n²) when all dominoes pair with each other (p ≈ n²/2)
#         Example: [[5,5], [5,5], [5,5], ...] creates C(n,2) = n(n-1)/2 pairs
    
#     Space Complexity: O(n + p)
#         - domino_to_indices dictionary: O(n)
#           Stores at most n unique domino values, each mapping to indices
#           Total indices stored = n (each index appears exactly once)
#         - pairs list: O(p)
#           Stores p pair results, each pair taking O(1) space
#         - Total: O(n) + O(p) = O(n + p)
        
#         Best case: O(n) when no pairs exist (p = 0)
#         Worst case: O(n²) when all dominoes pair (p ≈ n²/2)
    
#     Args:
#         dominoes: List of domino pairs [a, b]
#         target: Target sum value
        
#     Returns:
#         List of lists [[i, j]] where i < j, representing valid pair indices
        
#     Examples:
#         >>> findAllDominoPairIndices([[1,2], [9,8], [1,2]], 10)
#         [[0, 1], [1, 2]]
        
#         >>> findAllDominoPairIndices([[5,5], [5,5], [5,5]], 10)
#         [[0, 1], [0, 2], [1, 2]]
#     """
#     # Map: domino value -> list of indices where it appears
#     domino_to_indices = defaultdict(list)

#     # Store all valid pairs
#     pairs = []
    
#     for i, (a1, a2) in enumerate(dominoes):
#         # Calculate complement needed
#         complement = (target - a1, target - a2)
        
#         # Check if we've seen the complement before
#         if complement in domino_to_indices:
#             # Pair current index with ALL previous indices that have the complement
#             for j in domino_to_indices[complement]:
#                 pairs.append([j, i])
#                 # We can also add pair as [domino_at_j, domino_at_i]
#                 # pairs.append([dominoes[j], dominoes[i]])
        
#         # Add current index to the list for this domino value. No need to check if key exists - defaultdict handles it
#         domino_to_indices[(a1, a2)].append(i)

#         # If dominoes_to_indices is just a list, must explicitly check if key exists
#         # if (a1, a2) not in domino_to_indices:
#         #     domino_to_indices[(a1, a2)] = []
        
#         # domino_to_indices[(a1, a2)].append(i)
    
#     return pairs

# Approach : Using Integer Key (a1 * 10 + a2)

# Integer encoding (a*10+b) is more memory efficient because:
# Single object (28 bytes) vs tuple + references (48-104 bytes)
# Simpler hash (faster lookups)
# Better cache locality (CPUs love contiguous integers)

# def numEquivDominoPairs(dominoes, target):
#     """
#     Count pairs of dominoes where corresponding elements sum to target.
#     Uses integer encoding instead of tuple for keys (works for single digits 0-9).
    
#     Time Complexity: O(n)
#     - Single pass through the dominoes array: O(n)
#     - Dictionary lookup: O(1) average case
#     - Dictionary insertion/update: O(1) average case
    
#     Space Complexity: O(n)
#     - Dictionary stores at most n unique domino encodings
#     - Integer keys are more memory efficient than tuples
    
#     Args:
#         dominoes: List of domino pairs [a, b] where 0 <= a, b <= 9
#         target: Target sum value
        
#     Returns:
#         Integer - count of valid domino pairs
    
#     Note: 
#     - Encoding: [a, b] becomes a * 10 + b (e.g., [3,7] becomes 37)
#     - Only works for single-digit numbers (0-9)
#     - More memory efficient than tuple keys
#     """
#     domino_to_freq = {}
#     result = 0
    
#     for a1, a2 in dominoes:
#         # Calculate the complement domino [b1, b2]
#         b1 = target - a1
#         b2 = target - a2
        
#         # Encode complement as integer: b1 * 10 + b2
#         # Example: [9, 8] becomes 98
#         complement_key = b1 * 10 + b2
        
#         # If we've seen the complement, add its frequency
#         if complement_key in domino_to_freq:
#             result += domino_to_freq[complement_key]
        
#         # Encode current domino as integer: a1 * 10 + a2
#         # Example: [1, 2] becomes 12
#         current_key = a1 * 10 + a2
#         domino_to_freq[current_key] = domino_to_freq.get(current_key, 0) + 1
    
#     return result

# def findAllDominoPairIndices_IntegerEncoding(dominoes, target):
#     """
#     Find indices of all pairs of dominoes where corresponding elements sum to target.
#     Uses integer encoding instead of tuples for keys (works for single digits 0-9).
    
#     Time Complexity: O(n + p)
#     Space Complexity: O(n + p)
#     """
#     # Map: domino encoding (integer) -> list of indices
#     domino_to_indices = defaultdict(list)
    
#     # Store all valid pairs
#     pairs = []
    
#     for i, (a1, a2) in enumerate(dominoes):
#         # Calculate complement encoding
#         complement_key = (target - a1) * 10 + (target - a2)
        
#         # Check if complement exists and pair with all previous occurrences
#         if complement_key in domino_to_indices:
#             for j in domino_to_indices[complement_key]:
#                 pairs.append([j, i])
        
#         # Encode and store current domino
#         current_key = a1 * 10 + a2
#         domino_to_indices[current_key].append(i)
    
#     return pairs


# Dominoes Variant 1 : Numbers in dominoes can be any integer

# def numEquivDominoPairs(dominoes, target):
#     """
#     Works for ANY integer values (positive, negative, large).
    
#     Time Complexity: O(n)
#     Space Complexity: O(n)
#     """    
#     domino_to_freq = defaultdict(int)
#     result = 0
    
#     for a1, a2 in dominoes:
#         # Tuple handles any values - no collisions possible
#         complement = (target - a1, target - a2)
#         result += domino_to_freq[complement]
#         domino_to_freq[(a1, a2)] += 1
    
#     return result

# Dominoes Variant 2 : Given an array of domino pairs, return the number of unique domino value combinations [a1, a2] and [b1, b2] where a1 + b1 = target and a2 + b2 = target.

# Example 1:
# dominoes = [[1,2], [9,8], [1,2], [9,8]]
# target = 10

# Unique values: {[1,2], [9,8]}
# Value combination: [1,2] pairs with [9,8]
#   1 + 9 = 10 ✓
#   2 + 8 = 10 ✓

# Answer: 1 unique value combination

# Example 2:
# dominoes = [[5,5], [5,5]]
# target = 10

# Unique values: {[5,5]}
# Can [5,5] pair with [5,5]? 
#   5 + 5 = 10 ✓
#   5 + 5 = 10 ✓
# Yes! This is a valid value combination.

# Answer: 1 unique value combination

# Example 3:
# dominoes = [[5,5]]
# target = 10

# Unique values: {[5,5]}
# Can [5,5] pair with [5,5]?
# Yes, the VALUE combination is valid.
# But do we have enough dominoes to form this pair?

# This is the ambiguity: Does the problem require
# at least 2 physical dominoes to form a pair?

# def numEquivDominoPairs_MathematicalCombos(dominoes, target):
#     """
#     INTERPRETATION A: Count unique VALUE COMBINATIONS (pure mathematical approach)
    
#     A "unique domino value combination" is a pair of VALUES [a1,a2] and [b1,b2]
#     that mathematically satisfy the constraint, regardless of how many times
#     they physically appear in the input.
    
#     Philosophy: We're counting DISTINCT MATHEMATICAL COMBINATIONS, not physical pairs.
    
#     Time Complexity: O(n)
#     Space Complexity: O(n)
    
#     Examples:
#         [[5,5]] → 1
#             Unique values: {[5,5]}
#             Combination: [5,5] + [5,5] = target ✓
#             Count: 1 unique combination exists
        
#         [[5,5], [5,5], [5,5]] → 1
#             Unique values: {[5,5]}
#             Combination: [5,5] + [5,5] = target ✓
#             Count: Still 1 unique combination (same as above)
        
#         [[1,2], [9,8], [1,2], [9,8]] → 1
#             Unique values: {[1,2], [9,8]}
#             Combination: [1,2] + [9,8] = target ✓
#             Count: 1 unique combination
        
#         [[1,2], [3,4], [7,6], [9,8]] → 2
#             Unique values: {[1,2], [3,4], [7,6], [9,8]}
#             Combinations: 
#                 [1,2] + [9,8] = target ✓
#                 [3,4] + [7,6] = target ✓
#             Count: 2 unique combinations
#     """
#     # Step 1: Extract unique domino VALUES from input
#     # We only care about which distinct values exist, not how many times
#     # Example: [[5,5], [5,5], [5,5]] → {(5,5)}
#     unique_dominoes = set(tuple(d) for d in dominoes)
    
#     # Step 2: Store unique value combinations we find
#     # We use a set to automatically handle deduplication
#     pairs = set()
    
#     for domino in unique_dominoes:
#         a1, a2 = domino
        
#         complement = (target - a1, target - a2)
        
#         # Check if this complement value exists (anywhere in the input)
#         if complement in unique_dominoes:
#             # ================================================================
#             # CANONICAL REPRESENTATION!
#             # ================================================================
#             # Example: dominoes = [[1,2], [9,8]], target = 10
#             #
#             # WITHOUT canonical (just storing (domino, complement)):
#             #   Iteration 1: domino=(1,2), complement=(9,8)
#             #     → Add ((1,2), (9,8)) to set
#             #   Iteration 2: domino=(9,8), complement=(1,2)
#             #     → Add ((9,8), (1,2)) to set
#             #   Result: {((1,2), (9,8)), ((9,8), (1,2))} 
#             #   Length: 2 ❌ WRONG! These are the SAME logical pair!
#             #
#             # WITH canonical (using min/max):
#             #   Iteration 1: domino=(1,2), complement=(9,8)
#             #     → pair = (min((1,2), (9,8)), max((1,2), (9,8)))
#             #     → pair = ((1,2), (9,8))  [since (1,2) < (9,8)]
#             #     → Add ((1,2), (9,8)) to set
#             #   Iteration 2: domino=(9,8), complement=(1,2)
#             #     → pair = (min((9,8), (1,2)), max((9,8), (1,2)))
#             #     → pair = ((1,2), (9,8))  [same canonical form!]
#             #     → Try to add ((1,2), (9,8)) but set already has it
#             #   Result: {((1,2), (9,8))}
#             #   Length: 1 ✓ CORRECT!
#             #
#             # Why min/max works:
#             #   Python compares tuples lexicographically (left to right)
#             #   (1,2) < (9,8) because 1 < 9
#             #   So regardless of which domino we process first,
#             #   we ALWAYS get the same canonical form: smaller tuple first
#             # ================================================================
#             pair = (min(domino, complement), max(domino, complement))
#             pairs.add(pair)
            
#             # Note: If domino == complement (self-pairing like [5,5] + [5,5]),
#             # we still add it because it's a mathematically valid combination

#     return len(pairs)

# def numEquivDominoPairs_PhysicalPairs(dominoes, target):
#     """
#     INTERPRETATION B: Count unique VALUE COMBINATIONS (with physical constraint)
    
#     A "unique domino value combination" requires that we have enough physical
#     dominoes to form the pair. For self-pairing combinations, we need at least
#     2 physical dominoes with that value.
    
#     Philosophy: We're counting combinations that can be PHYSICALLY FORMED.
    
#     Time Complexity: O(n)
#     Space Complexity: O(n)
    
#     Examples:
#         [[5,5]] → 0
#             Unique values: {[5,5]: count=1}
#             Combination: [5,5] + [5,5] is valid mathematically
#             BUT: We only have 1 physical domino, can't form a pair
#             Count: 0
        
#         [[5,5], [5,5]] → 1
#             Unique values: {[5,5]: count=2}
#             Combination: [5,5] + [5,5] is valid
#             AND: We have 2 physical dominoes, CAN form a pair
#             Count: 1
        
#         [[5,5], [5,5], [5,5]] → 1
#             Unique values: {[5,5]: count=3}
#             Combination: [5,5] + [5,5] is valid
#             AND: We have 3 physical dominoes (≥2), CAN form a pair
#             Count: 1 (still just one unique combination)
        
#         [[1,2], [9,8]] → 1
#             Unique values: {[1,2]: count=1, [9,8]: count=1}
#             Combination: [1,2] + [9,8] is valid
#             AND: Different values, so 1 of each is enough
#             Count: 1
        
#         [[5,5], [3,4]] → 0
#             Unique values: {[5,5]: count=1, [3,4]: count=1}
#             [5,5] needs [5,5] but count=1 (not enough) ✗
#             [3,4] needs [7,6] which doesn't exist ✗
#             Count: 0
#     """
#     from collections import Counter
    
#     # Step 1: Count frequency of each unique domino VALUE
#     # We need to know HOW MANY times each value appears
#     # Example: [[5,5], [5,5], [3,4]] → {(5,5): 2, (3,4): 1}
#     domino_counts = Counter(tuple(d) for d in dominoes)

#     # Without Counter
#     # domino_counts = {}
#     # for d in dominoes:
#     #     key = tuple(d)
#     #     if key in domino_counts:
#     #         domino_counts[key] += 1
#     #     else:
#     #         domino_counts[key] = 1
    
#     # Step 2: Store unique value combinations we can physically form
#     pairs = set()
    
#     # Step 3: For each unique value and its count, check constraints
#     for domino, count in domino_counts.items():
#         a1, a2 = domino
        
#         # Calculate complement value needed
#         complement = (target - a1, target - a2)
        
#         # Check if complement value exists in our input
#         if complement in domino_counts:
            
#             # CRITICAL DISTINCTION: Check if domino pairs with itself
#             if domino == complement:
#                 # SELF-PAIRING case (e.g., [5,5] needs [5,5])
#                 # We need at least 2 physical dominoes to form a pair
#                 # Example: [[5,5]] has count=1, NOT ENOUGH
#                 #          [[5,5], [5,5]] has count=2, ENOUGH
#                 if count >= 2:
#                     # We have enough physical dominoes!
#                     pairs.add((domino, complement))
#                 # else: Not enough physical dominoes, skip this combination
                
#             else:
#                 # DIFFERENT VALUES case (e.g., [1,2] needs [9,8])
#                 # We only need 1 of each value
#                 # Since both exist in domino_counts, we can form the pair
#                 pair = (min(domino, complement), max(domino, complement))
#                 pairs.add(pair)
    
#     # Step 4: Return count of unique combinations we can physically form
#     return len(pairs)







