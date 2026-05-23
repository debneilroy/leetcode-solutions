"""
LeetCode 1570. Dot Product of Two Sparse Vectors
Difficulty: Medium
URL: https://leetcode.com/problems/dot-product-of-two-sparse-vectors/
"""

# Approach : Hashmap

class SparseVector:
    """
    A space-efficient representation of sparse vectors (vectors with mostly zeros).
    Only stores non-zero elements to optimize memory usage and computation.
    """
    
    def __init__(self, nums):
        """
        Initialize the sparse vector by storing only non-zero elements.
        
        Args:
            nums: List[int] - Input vector that may contain many zeros
        
        Time Complexity: O(n) where n is the length of nums
            - We iterate through all elements once to identify non-zeros
        
        Space Complexity: O(L) where L is the number of non-zero elements
            - We only store non-zero values in the hashmap
            - Best case: O(1) if all elements are zero
            - Worst case: O(n) if all elements are non-zero
        """
        # Store original length for validation in dotProduct
        # if lengths always equal, remove this
        self.length = len(nums)
        
        # Dictionary to store only non-zero elements
        # Key: index in original array
        # Value: the non-zero value at that index
        self.nonzeros = {}
        
        # Iterate through input array and store non-zero elements
        for i, num in enumerate(nums):
            if num != 0:
                self.nonzeros[i] = num
    
    def dotProduct(self, vec):
        """
        Compute the dot product between this vector and another sparse vector.
        
        Args:
            vec: SparseVector - Another sparse vector to compute dot product with
        
        Returns:
            int - The dot product result (sum of products of corresponding elements)
        
        Time Complexity: O(min(L1, L2)) where L1 and L2 are the numbers of
                        non-zero elements in each vector
            - We iterate through the smaller set of non-zero elements
            - Hashmap lookup is O(1) on average
            - Best case: O(1) if one vector has no non-zero elements
            - Worst case: O(n) if both vectors are fully dense (L1 = L2 = n)
        
        Space Complexity: O(1)
            - Only using a constant amount of extra space for the result
            - No additional data structures created

        Edge Cases:
            - Both vectors all zeros: nonzeros dicts are empty, loop never runs, returns 0
            - One vector all zeros: smaller set is empty, loop never runs, returns 0
            - Both vectors fully dense: degrades to O(n), iterates all n elements
            - Single element vectors: handles correctly, returns 0 or v1[0]*v2[0]
        """
        # Base checks
        if not isinstance(vec, SparseVector):
            raise TypeError("Expected a SparseVector instance")

        # Length check before zero exit: zero vectors of different lengths should raise,
        # not silently return 0 — correctness before optimization.
        # If reversed, dotProduct([0,0], [0,0,0]) would silently return 0 instead of raising
        # if lengths always equal: remove this check — guaranteed by problem constraints
        if self.length != vec.length:
            raise ValueError(f"Vector length mismatch: {self.length} vs {vec.length}")

        # Early exit: if either vector is all zeros, dot product is 0
        if not self.nonzeros or not vec.nonzeros:
            return 0

        result = 0

        if len(self.nonzeros) <= len(vec.nonzeros):
            smaller, larger = self.nonzeros, vec.nonzeros
        else:
            smaller, larger = vec.nonzeros, self.nonzeros

        # Iterate through the smaller one
        for i, val in smaller.items():  # O(min(L1, L2))
            if i in larger:              # O(1)
                result += val * larger[i]

        return result

# Example 

# Say we have:

# v1 = SparseVector([1, 0, 0, 2, 0])
# v2 = SparseVector([0, 0, 3, 2, 0])

# After __init__:
# v1.length   = 5
# v1.nonzeros = {0: 1, 3: 2}      # only indices with non-zero values

# v2.length   = 5
# v2.nonzeros = {2: 3, 3: 2}      # only indices with non-zero values

# During dotProduct:
# isinstance check  → pass
# length check      → 5 == 5, pass
# zero check        → both have nonzeros, pass

# len(v1.nonzeros) = 2
# len(v2.nonzeros) = 2
# 2 <= 2 → smaller = v1.nonzeros, larger = v2.nonzeros

# Iterate smaller:
#   i=0, val=1 → 0 not in larger → skip
#   i=3, val=2 → 3 in larger    → result += 2 * 2 = 4

# return 4
# Verify manually:
# [1, 0, 0, 2, 0]
# [0, 0, 3, 2, 0]
# = (1*0) + (0*0) + (0*3) + (2*2) + (0*0) = 4 


# Approach : Index-Value Pairs (Preferred approach for Meta)

class SparseVector:
    """
    A space-efficient representation of sparse vectors using sorted list of tuples.
    Stores only non-zero elements as (index, value) pairs in sorted order by index.
    """
    
    def __init__(self, nums):
        """
        Initialize the sparse vector by storing non-zero elements as sorted tuples.
        
        Args:
            nums: List[int] - Input vector that may contain many zeros
        
        Time Complexity: O(n) where n is the length of nums
            - We iterate through all elements once to identify non-zeros
            - Pairs are naturally sorted since we iterate indices in order (0 to n-1)
        
        Space Complexity: O(L) where L is the number of non-zero elements
            - We store L tuples, each containing (index, value)
            - Best case: O(1) if all elements are zero (empty list)
            - Worst case: O(n) if all elements are non-zero
        """
        # Store original length for validation in dotProduct
         # if lengths always equal, remove this
        self.length = len(nums)

        # Store non-zero elements as list of (index, value) tuples
        # Tuples over lists: immutable (pairs should never change after creation),
        # slightly less memory, and signals fixed records rather than mutable sequences
        self.pairs = []
        for i, num in enumerate(nums):
            if num != 0:
                self.pairs.append((i, num))  # tuple: index and value are a fixed record
        
    def dotProduct(self, vec):
        """
        Compute dot product using two-pointer technique on sorted lists.
        
        Args:
            vec: SparseVector - Another sparse vector to compute dot product with
        
        Returns:
            int - The dot product result (sum of products of corresponding elements)
        
        Time Complexity: O(L1 + L2) where L1 and L2 are the numbers of
                        non-zero elements in each vector
            - We traverse both lists simultaneously using two pointers
            - Each element in both lists is visited at most once
            - Worst case: O(L1 + L2) when lists have no overlapping indices (all skips)
            - Best case: O(min(L1, L2)) when one list is exhausted early
        
        Space Complexity: O(1)
            - Only using constant extra space (result, i, j variables)
            - No additional data structures created
        """
        # Base checks
        if not isinstance(vec, SparseVector):
            raise TypeError("Expected a SparseVector instance")

        # Length check before zero exit: zero vectors of different lengths should raise,
        # not silently return 0 — correctness before optimization.
        # If reversed, dotProduct([0,0], [0,0,0]) would silently return 0 instead of raising
        # if lengths always equal: remove this check — guaranteed by problem constraints
        if self.length != vec.length:
            raise ValueError(f"Vector length mismatch: {self.length} vs {vec.length}")

        # Early exit: if either vector is all zeros, dot product is 0
        if not self.pairs or not vec.pairs:
            return 0

        result = 0
        
        # Two pointers starting at the beginning of each pairs list
        i = 0  # pointer for self.pairs
        j = 0  # pointer for vec.pairs
        
        # Advance both pointers until one list is exhausted
        while i < len(self.pairs) and j < len(vec.pairs):
            idx1, val1 = self.pairs[i]
            idx2, val2 = vec.pairs[j]
            
            if idx1 == idx2:
                # Matching indices: contribute to dot product, advance both
                result += val1 * val2
                i += 1 # advance pointer, not idx1 — idx1 is a read-only local, i controls position in list
                j += 1
            
            elif idx1 < idx2:
                # self is behind: advance i to catch up to vec's index
                i += 1  
            
            else:
                # vec is behind: advance j to catch up to self's index
                j += 1  
        
        return result

# Example: 

# Say we have:
# v1 = SparseVector([1, 0, 0, 2, 0])
# v2 = SparseVector([0, 0, 3, 2, 0])

# After __init__:
# v1.length = 5
# v1.pairs  = [(0, 1), (3, 2)]     # only non-zero elements as (index, value) tuples

# v2.length = 5
# v2.pairs  = [(2, 3), (3, 2)]     # only non-zero elements as (index, value) tuples

# During dotProduct:
# isinstance check  → pass
# length check      → 5 == 5, pass
# zero check        → both have pairs, pass

# i=0, j=0  → idx1=0, idx2=2  → 0 < 2 → self is behind, advance i
# i=1, j=0  → idx1=3, idx2=2  → 3 > 2 → vec is behind,  advance j
# i=1, j=1  → idx1=3, idx2=3  → match → result += 2 * 2 = 4, advance both
# i=2 → i exhausted, exit loop

# return 4

# When Index-Value pairs is better

# 1. When both vectors have similar sparsity (L₁ ≈ L₂)

# O(L₁ + L₂) ≈ O(2L₁) vs O(L₁) - not much difference


# 2. Memory-constrained environments

# List of tuples has less overhead than hash map


# 3. Cache-friendly performance needed

# Sequential access is more cache-friendly than hash lookups


# 4. Guaranteed worst-case performance

# O(L₁ + L₂) guaranteed vs O(L₁ × L₂) with hash collisions (theoretical)


# Variant : What if one vector is sparse and the other one is dense (or length of both vectors differ)?
# Use binary search on the dense vector (or longer vector)

class SparseVector:
    def __init__(self, nums):
        """
        Store non-zero elements as sorted list of (index, value) tuples.

        Time Complexity: O(n) where n is the length of nums
            - We iterate through all elements once to identify non-zeros
            - Pairs are naturally sorted since we iterate indices in order (0 to n-1)
        
        Space Complexity: O(L) where L is the number of non-zero elements
            - We store L tuples, each containing (index, value)
            - Best case: O(1) if all elements are zero (empty list)
            - Worst case: O(n) if all elements are non-zero
        """

        self.length = len(nums)

        self.pairs = []
        for i, num in enumerate(nums):
            if num != 0:
                self.pairs.append((i, num))  

    def dotProduct(self, vec):
        """
        Compute dot product using binary search.

        Strategy: iterate through the smaller vector and binary search
        for matching indices in the larger vector.

        Time Complexity: O(min(L1, L2) * log(max(L1, L2)))
            - Iterate through smaller vector: O(min(L1, L2))
            - Binary search in larger vector: O(log(max(L1, L2)))
            - Best case: O(log n) when smaller vector has only one non-zero element
            - Worst case: O(n log n) when both vectors are fully dense (L1 = L2 = n),
            worse than two-pointer's O(n) — prefer two-pointer when L1 ≈ L2
            - Useful when one vector is much sparser than the other:
              e.g. k non-zeros vs n non-zeros gives O(k log n),
              faster than two-pointer's O(n) in this case

        Space Complexity: O(1)
            - Only constant extra space (result, pointers)
            - No additional data structures created

        When to Use:
            - One vector is much sparser than the other (k << n):
              binary search gives O(k log n) vs two-pointer's O(n)
            - Vectors are pre-sorted and stored as pairs (no extra preprocessing)
            - Prefer over hashmap when memory is tight (no dict overhead)
            - Prefer over two-pointer when L1 and L2 are highly unbalanced

            Avoid when:
            - Both vectors have similar sparsity: two-pointer's O(L1 + L2)
              beats O(min * log(max)) when L1 ≈ L2
            - Vectors are not sorted: sorting costs O(n log n) upfront
        """

        # Base checks
        if not isinstance(vec, SparseVector):
            raise TypeError("Expected a SparseVector instance")

        if self.length != vec.length:
            raise ValueError(f"Vector length mismatch: {self.length} vs {vec.length}")

        if not self.pairs or not vec.pairs:
            return 0

        result = 0

        # Iterate smaller vector, binary search in larger — minimizes total searches
        if len(self.pairs) <= len(vec.pairs):
            smaller, larger = self.pairs, vec.pairs
        else:
            smaller, larger = vec.pairs, self.pairs

        # For each non-zero in smaller, search for matching index in larger
        for idx, val in smaller:
            pos = self._binary_search(larger, idx)
            if pos != -1:  # matching index found, contribute to dot product
                result += val * larger[pos][1]

        return result

    def _binary_search(self, pairs, target_idx):
        """
        Binary search for target_idx in sorted pairs list.

        Args:
            pairs: list of (index, value) tuples sorted by index
            target_idx: the index we're searching for

        Returns:
            position in pairs if found, -1 otherwise

        Time Complexity: O(log L) where L is len(pairs)
        Space Complexity: O(1)
        """
        left, right = 0, len(pairs) - 1

        while left <= right: # not left < right: would miss target when left == right (single element)
            mid = (left + right) // 2
            mid_idx = pairs[mid][0]  # extract index from (index, value) tuple

            if mid_idx == target_idx:
                return mid          # found matching index
            elif mid_idx < target_idx:
                left = mid + 1      # target is in right half
            else:
                right = mid - 1     # target is in left half

        return -1  # index not present in larger vector


# Example :

# v1 = SparseVector([1, 0, 0, 0, 0])       # sparse: only 1 non-zero
# v2 = SparseVector([1, 2, 3, 4, 5])       # dense: all non-zero

# After __init__:
# v1.length = 5
# v1.pairs  = [(0, 1)]                      # L1 = 1

# v2.length = 5
# v2.pairs  = [(0,1),(1,2),(2,3),(3,4),(4,5)]  # L2 = 5

# During dotProduct:
# isinstance check  → pass
# length check      → 5 == 5, pass
# zero check        → both have pairs, pass

# len(v1.pairs) = 1
# len(v2.pairs) = 5
# 1 <= 5 → smaller = v1.pairs, larger = v2.pairs

# Iteration 1: idx=0, val=1
#   binary search for 0 in [(0,1),(1,2),(2,3),(3,4),(4,5)]
#   mid=2 → 2 > 0 → go left
#   mid=0 → 0 == 0 → found at pos=0
#   result += 1 * 1 = 1

# no more elements in smaller, exit loop
# return 1

# TC breakdown:
# 1 iteration × log(5) ≈ 1 × 2 = 2 operations    → O(k log n) = O(1 * log 5)
# two-pointer would take 1 + 5 = 6 steps          → O(n)

# Binary search wins significantly when k << n


# Variant : (precursor to LC 1868)

# Given two sorted integer arrays nums1 and nums2 of the same length that may contain many duplicate values, design a data structure that compresses them efficiently and supports computing their dot product.
# Implement class CompressedVector:

# CompressedVector(nums) — initializes the object with the sorted array nums
# dotProduct(vec) — returns the dot product of this vector and vec

# Example:

# Input:
# nums1 = [1, 1, 1, 1, 3, 3, 5, 5, 5, 5, 5, 8]
# nums2 = [1, 1, 3, 3, 3, 5, 7, 7, 7, 8, 8, 8]

# Output: 281

# Explanation:
# Dot product multiplies corresponding elements and sums them up:

# pos:   0  1  2  3  4  5  6  7  8  9  10  11
# nums1: 1  1  1  1  3  3  5  5  5  5   5   8
# nums2: 1  1  3  3  3  5  7  7  7  8   8   8
#        ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓   ↓   ↓
# prod:  1  1  3  3  9 15 35 35 35 40  40  64

# (1×1) + (1×1) + (1×3) + (1×3) + (3×3) + (3×5) +
# (5×7) + (5×7) + (5×7) + (5×8) + (5×8) + (8×8)
# = 1 + 1 + 3 + 3 + 9 + 15 + 35 + 35 + 35 + 40 + 40 + 64
# = 281

# Constraints:

# 1. 1 <= nums.length <= 10^5
# 2. nums1.length == nums2.length
# 3. -100 <= nums[i] <= 100
# 4. nums is sorted in non-decreasing order
# 5. At most 10^4 calls to dotProduct


class CompressedVector:
    """
    Efficient representation of sorted vectors with duplicates using
    Run-Length Encoding (RLE).

    Stores (value, start, end) tuples where end is exclusive,
    avoiding recomputation of end positions in dotProduct.
    Assumes input vector is sorted.
    """

    def __init__(self, nums):
        """
        Compress sorted vector with duplicates using run-length encoding.

        Args:
            nums: List[int] - Sorted vector (may contain duplicates)

        Time Complexity: O(n) where n is the length of nums
            - Single pass through the array to identify runs

        Space Complexity: O(R) where R is the number of distinct runs
            - Best case: O(1) if all elements are the same
            - Worst case: O(n) if all elements are unique
            - Typical case: O(R) where R << n with many duplicates

        Example:
            nums = [1, 1, 1, 3, 3, 5, 5, 5, 5]
            runs = [(1, 0, 3), (3, 3, 5), (5, 5, 9)]
                    val s  e   val s  e   val s  e
                    (end is exclusive)

        Why exclusive end:
            - matches Python conventions (range, slicing)
            - overlap_count = overlap_end - overlap_start (no +1 needed)
            - overlap check is simply overlap_start < overlap_end (no +1 needed)
            - using inclusive end requires +1 in two places, making code harder to read
        """
        self.length = len(nums)
        self.runs = []  # list of (value, start, end) tuples, end is exclusive

        if not nums:
            return

        current_val = nums[0]
        start_idx = 0

        for i in range(1, self.length):
            if nums[i] != current_val:
                # End current run at i (exclusive) and save it
                # if using inclusive end: append (current_val, start_idx, i - 1)
                self.runs.append((current_val, start_idx, i)) 
                current_val = nums[i]
                start_idx = i

        # Flush last run — end is self.length since end is exclusive
        # if using inclusive end: append (current_val, start_idx, self.length - 1)
        self.runs.append((current_val, start_idx, self.length))

    def dotProduct(self, vec):
        """
        Compute dot product between two compressed vectors.

        Args:
            vec: CompressedVector - Another compressed vector

        Returns:
            int - The dot product result

        Time Complexity: O(R1 + R2) where R1 and R2 are the numbers of runs
            - Two pointers traverse both run lists simultaneously
            - Each run is processed at most once
            - Worst case: O(n1 + n2) when all elements are unique (R1=n1, R2=n2),
              no compression benefit, degrades to element-wise traversal
            - Much better than O(n1 + n2) for vectors with many duplicates:
              duplicates collapse into single runs, so R << n
              e.g. [1,1,1,1,1] → 1 run instead of 5 elements → O(1) instead of O(5)

        Space Complexity: O(1)
            - Only constant extra space (result, pointers, overlap vars)


        Algorithm:
            1. Use two pointers on the run lists
            2. For each pair of runs, find overlapping positions
            3. Compute contribution: value1 * value2 * overlap_count
            4. Advance pointer whose run ends first; advance both if tied
        """
        if not isinstance(vec, CompressedVector):
            raise TypeError("Expected a CompressedVector instance")

        if self.length != vec.length:
            raise ValueError(f"Vector length mismatch: {self.length} vs {vec.length}")

        # Early exit: if either vector is empty
        if not self.runs or not vec.runs:
            return 0

        result = 0
        i = 0  # pointer for self.runs
        j = 0  # pointer for vec.runs

        while i < len(self.runs) and j < len(vec.runs):
            val1, start1, end1 = self.runs[i]   # end is exclusive, no recomputation needed
            val2, start2, end2 = vec.runs[j]    # end is exclusive, no recomputation needed

            overlap_start = max(start1, start2)
            overlap_end   = min(end1, end2)

            # if using inclusive end:
            #   if overlap_start <= overlap_end:                     # <= instead of <: single
            #       overlap_count = overlap_end - overlap_start + 1  # element overlap (start==end)
            #                                                         # is valid, < would miss it
            if overlap_start < overlap_end:
                # Each overlapping position contributes val1 * val2
                overlap_count = overlap_end - overlap_start
                result += val1 * val2 * overlap_count

            # Advance pointer whose run ends first
            # If tied (end1 == end2), advancing both is a performance optimization —
            # skips a redundant iteration since overlap check would yield count=0 anyway
            if end1 < end2:
                i += 1      # run1 ends first, move to next run in self
            elif end2 < end1:
                j += 1      # run2 ends first, move to next run in vec
            else:
                i += 1      # both runs end at same position,
                j += 1      # advance both to skip redundant iteration

        return result

# Example dry run:

# nums1 = [1, 1, 3, 3, 3]
# nums2 = [1, 2, 2, 3, 3]

# After __init__:
# v1.runs = [(1,0,2), (3,2,5)]        # R1 = 2
# v2.runs = [(1,0,1), (2,1,3), (3,3,5)]  # R2 = 3

# During dotProduct:
# isinstance check  → pass
# length check      → 5 == 5, pass
# zero check        → both have runs, pass

# i=0, j=0 → run1=(1,0,2), run2=(1,0,1)
#   overlap_start = max(0,0) = 0
#   overlap_end   = min(2,1) = 1
#   0 < 1 → count=1 → result += 1*1*1 = 1
#   end1=2 > end2=1 → advance j

# i=0, j=1 → run1=(1,0,2), run2=(2,1,3)
#   overlap_start = max(0,1) = 1
#   overlap_end   = min(2,3) = 2
#   1 < 2 → count=1 → result += 1*2*1 = 3
#   end1=2 < end2=3 → advance i

# i=1, j=1 → run1=(3,2,5), run2=(2,1,3)
#   overlap_start = max(2,1) = 2
#   overlap_end   = min(5,3) = 3
#   2 < 3 → count=1 → result += 3*2*1 = 9
#   end1=5 > end2=3 → advance j

# i=1, j=2 → run1=(3,2,5), run2=(3,3,5)
#   overlap_start = max(2,3) = 3
#   overlap_end   = min(5,5) = 5
#   3 < 5 → count=2 → result += 3*3*2 = 27
#   end1=5 == end2=5 → advance both

# i=2, j=3 → both exhausted, exit loop

# Output : 27


# Another approach : Use (value, count, start_index) 

class CompressedVector:
    """
    Efficient representation of sorted vectors with duplicates using
    Run-Length Encoding (RLE).

    Stores (value, count, start_index) tuples.
    Assumes input vector is sorted.
    """

    def __init__(self, nums):

        self.length = len(nums)
        self.runs = []  # list of (value, count, start_index) tuples

        if not nums:
            return

        current_val = nums[0]
        current_count = 1
        start_idx = 0

        for i in range(1, self.length):
            if nums[i] != current_val:
                self.runs.append((current_val, current_count, start_idx))
                current_val = nums[i]
                current_count = 1    # reset count for new run
                start_idx = i
            else:
                current_count += 1   # continue current run

        # Flush last run
        self.runs.append((current_val, current_count, start_idx))

    def dotProduct(self, vec):
 
        if not isinstance(vec, CompressedVector):
            raise TypeError("Expected a CompressedVector instance")

        if self.length != vec.length:
            raise ValueError(f"Vector length mismatch: {self.length} vs {vec.length}")

        if not self.runs or not vec.runs:
            return 0

        result = 0
        i = 0  
        j = 0  

        while i < len(self.runs) and j < len(vec.runs):
            val1, count1, start1 = self.runs[i]
            val2, count2, start2 = vec.runs[j]

            end1 = start1 + count1
            end2 = start2 + count2

            overlap_start = max(start1, start2)
            overlap_end   = min(end1, end2)

            if overlap_start < overlap_end:
                overlap_count = overlap_end - overlap_start
                result += val1 * val2 * overlap_count

            if end1 < end2:
                i += 1      
            elif end2 < end1:
                j += 1      
            else:
                i += 1      
                j += 1      

        return result


# Follow up : Arrays are of unequal length

class CompressedVector:
    def __init__(self, nums):

        self.length = len(nums)
        self.runs = []  # list of (value, start, end) tuples, end is exclusive

        if not nums:
            return

        current_val = nums[0]
        start_idx = 0

        for i in range(1, self.length):
            if nums[i] != current_val:
                self.runs.append((current_val, start_idx, i))  
                current_val = nums[i]
                start_idx = i

        self.runs.append((current_val, start_idx, self.length))

    def dotProduct(self, vec):

        if not isinstance(vec, CompressedVector):
            raise TypeError("Expected a CompressedVector instance")

        if not self.runs or not vec.runs:
            return 0

        # Compute up to shorter vector's length — extra elements treated as 0
        effective_length = min(self.length, vec.length)

        result = 0
        i = 0  # pointer for self.runs
        j = 0  # pointer for vec.runs

        while i < len(self.runs) and j < len(vec.runs):
            val1, start1, end1 = self.runs[i]
            val2, start2, end2 = vec.runs[j]

            # Clip runs to effective length — ignore positions beyond shorter vector
            end1 = min(end1, effective_length)
            end2 = min(end2, effective_length)

            # If run starts at or beyond effective length, no more valid positions
            if start1 >= effective_length or start2 >= effective_length:
                break

            overlap_start = max(start1, start2)
            overlap_end   = min(end1, end2)

            if overlap_start < overlap_end:
                overlap_count = overlap_end - overlap_start
                result += val1 * val2 * overlap_count

            if end1 < end2:
                i += 1     
            elif end2 < end1:
                j += 1      
            else:
                i += 1      
                j += 1      

        return result
