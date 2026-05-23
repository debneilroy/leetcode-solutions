"""
LeetCode 88. Merge Sorted Array
Difficulty: Easy
URL: https://leetcode.com/problems/merge-sorted-array/
"""

# Brute Force Approach : Concatenate, then sort

# class Solution:
#     def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
#         """
#         Brute force: Copy nums2 into nums1, then sort the entire array.
        
#         TC: Best O(m + n) - Timsort detects already sorted runs
#             Worst O((m + n) log(m + n)) - general sorting case
#         SC: Best O(log(m + n)) - recursion depth for small merges
#             Worst O(m + n) - Timsort's auxiliary space for merging
        
#         Args:
#             nums1: First sorted array with extra space at end
#             m: Number of valid elements in nums1
#             nums2: Second sorted array
#             n: Number of elements in nums2
#         """
#         # Copy all elements from nums2 into the end of nums1
#         # nums1[m:m+n] = nums2 is slice assignment (in-place)
#         for i in range(n):
#             nums1[m + i] = nums2[i]
        
#         # Sort the entire array of size m + n in-place
#         # This destroys the fact that nums1 and nums2 were already sorted
#         # Timsort can detect the two sorted runs and merge efficiently
#         # Best case: O(m + n) if runs are already ordered
#         # Example: nums1=[1,2,3], nums2=[4,5,6] → already sorted after copy
#         # Worst case: O((m + n) log(m + n)) for general case
#         # Example: nums1=[4,5,6], nums2=[1,2,3] → needs full sort
#         nums1.sort()

# Optimal approach : Three Pointers (Start From the End)

class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Merge nums2 into nums1 in-place.
        
        TC: O(m + n) - single pass, each element processed once
        SC: O(1) - only three pointers used
        
        Args:
            nums1: First sorted array with extra space at end
            m: Number of valid elements in nums1
            nums2: Second sorted array
            n: Number of elements in nums2
        """
        # Edge case: nums2 is empty, nums1 already sorted
        if n == 0:
            return
        
        # Edge case: nums1 has no valid elements, copy all of nums2
        # Note: not strictly required since main loop handles it
        # (p1 = -1, so p1 >= 0 is always false, we copy all nums2)
        # nums1[:] = nums2 is slice assignment (in-place), NOT a copy
        # Equivalent to: for i in range(n): nums1[i] = nums2[i]
        # Space complexity remains O(1)
        if m == 0:
            nums1[:] = nums2
            return
        
        # Start from end of valid elements in both arrays
        p1, p2 = m - 1, n - 1
        # Start from end of nums1's total capacity
        p = m + n - 1
        
        # Continue while nums2 has elements to merge
        while p2 >= 0:
            # If nums1 still has elements AND nums1's element is larger
            if p1 >= 0 and nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                # Either nums1 exhausted OR nums2's element is larger/equal
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1
        
        # No need to copy remaining nums1 elements - already in place

# Approach : Three Pointers (Start From the Beginning)

class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Merge nums2 into nums1 using forward-fill with extra space.
        
        TC: O(m + n) - single pass through both arrays
        SC: O(m) - temporary copy of nums1's valid elements
        
        Args:
            nums1: First sorted array with extra space at end
            m: Number of valid elements in nums1
            nums2: Second sorted array
            n: Number of elements in nums2
        """
        # Edge case: nums2 is empty
        if n == 0:
            return
        
        # Edge case: nums1 has no valid elements
        if m == 0:
            nums1[:] = nums2
            return
        
        # Copy valid elements from nums1 to avoid overwriting
        # WHY: Forward-fill writes at position p starting from 0
        # Without copy: nums1=[1,2,3,0,0,0], nums2=[2,5,6]
        # At p=2, we write nums2[0]=2, overwriting nums1[2]=3 before reading it
        # With copy: we read from nums1_copy (immutable), write to nums1 (safe)
        # This is why forward-fill requires O(m) extra space
        nums1_copy = nums1[:m]
        
        # Start from beginning of both arrays
        p1, p2 = 0, 0
        # Start from beginning of nums1
        p = 0
        
        # Merge while both arrays have elements
        while p1 < m and p2 < n:
            # Compare elements from nums1_copy and nums2
            if nums1_copy[p1] <= nums2[p2]:
                nums1[p] = nums1_copy[p1]
                p1 += 1
            else:
                nums1[p] = nums2[p2]
                p2 += 1
            p += 1
        
        # Copy remaining elements from nums1_copy (if any)
        # Example: nums1_copy=[4,5,6], nums2=[1,2,3]
        # After main loop: nums1=[1,2,3,?,?,?], p1=0, p2=3, p=3
        # Need to copy nums1_copy[0:3] = [4,5,6] to nums1[3:6]
        while p1 < m:
            nums1[p] = nums1_copy[p1]
            p1 += 1
            p += 1
        
        # Copy remaining elements from nums2 (if any)
        # Example: nums1_copy=[1,2,3], nums2=[4,5,6]
        # After main loop: nums1=[1,2,3,?,?,?], p1=3, p2=0, p=3
        # Need to copy nums2[0:3] = [4,5,6] to nums1[3:6]
        while p2 < n:
            nums1[p] = nums2[p2]
            p2 += 1
            p += 1

# Variant : No m and n given explicitly

# You are given two integer arrays list_a and list_b, sorted in non-decreasing order.
# Merge list_a and list_b into a single array sorted in non-decreasing order.
# The final sorted array should not be returned by the function, but instead be stored inside the array list_a. To accommodate this, list_a is double the length of list_b, where the first half of elements denote the elements that should be merged, and the last half of elements are set to 0 and should be ignored.

# Example 1:
# Input: list_a = [1, 8, 0, 0], list_b = [3, 5]
# Output: [1, 3, 5, 8]
# Explanation: The arrays we are merging are [1, 8] and [3, 5].
# The result of the merge is [1, 3, 5, 8] with the underlined elements coming from list_a.

# Example 2:
# Input: list_a = [1, 0], list_b = [2]
# Output: [1, 2]
# Explanation: The arrays we are merging are [1] and [2].
# The result of the merge is [1, 2].

# class Variant:
#     def mergeSortedArray(self, list_a: list[int], list_b: list[int]) -> None:
#         """
#         Merge two sorted arrays list_a and list_b into list_a in-place.
        
#         TC: O(m + n) - single pass, each element processed once
#             where m = len(list_a) // 2, n = len(list_b)
#         SC: O(1) - only three pointers used
        
#         Args:
#             list_a: First sorted array, length = 2 * len(list_b)
#                    First half contains valid elements, second half is zeros
#             list_b: Second sorted array
#         """
#         # Start from end of valid elements in list_a
#         # list_a has length 2n where first n elements are valid
#         p1 = len(list_a) // 2 - 1
        
#         # Start from end of list_b
#         p2 = len(list_b) - 1
        
#         # Start from end of list_a's total capacity
#         p = len(list_a) - 1
        
#         # Continue while list_b has elements to merge
#         while p2 >= 0:
#             # If list_a still has elements AND list_a's element is larger/equal
#             if p1 >= 0 and list_a[p1] >= list_b[p2]:
#                 list_a[p] = list_a[p1]
#                 p1 -= 1
#             else:
#                 # Either list_a exhausted OR list_b's element is larger
#                 list_a[p] = list_b[p2]
#                 p2 -= 1
#             p -= 1
        
#         # No need to copy remaining list_a elements - already in place


# Variant : Merge three arrays

# You are given three integer arrays list_a, list_b, and list_c, sorted in non-decreasing order. Arrays can contain duplicate elements.
# Merge list_a, list_b, and list_c into a single array sorted in non-decreasing order.
# The final sorted array should be stored inside the array list_a. To accommodate this, list_a has length equal to len(list_a_valid) + len(list_b) + len(list_c), where the first portion contains valid elements from list_a, and the remaining positions are set to 0 and should be ignored.

# Example 1:
# Input: list_a = [1, 5, 9, 0, 0, 0, 0], list_b = [2, 6], list_c = [3, 7]
# Output: [1, 2, 3, 5, 6, 7, 9]
# Explanation: Merging [1, 5, 9], [2, 6], and [3, 7]

# Example 2:
# Input: list_a = [1, 2, 2, 0, 0, 0], list_b = [2, 3], list_c = [4]
# Output: [1, 2, 2, 2, 3, 4]
# Explanation: Merging [1, 2, 2], [2, 3], and [4] with duplicates

# class Variant3Arrays:
#     def mergeSortedArrays(self, list_a: list[int], list_b: list[int], list_c: list[int]) -> None:
#         """
#         Merge three sorted arrays list_a, list_b, and list_c into list_a in-place.
        
#         TC: O(m + n + k) - single pass, each element processed once
#             where m = len(list_a_valid), n = len(list_b), k = len(list_c)
#         SC: O(1) - only four pointers used
        
#         Args:
#             list_a: First sorted array with extra space at end
#             list_b: Second sorted array
#             list_c: Third sorted array
#         """

#         # Check if list_a has enough capacity
#         if len(list_a) < len(list_b) + len(list_c):
#             raise ValueError("list_a doesn't have enough space to merge all arrays")

#         # Calculate number of valid elements in list_a
#         # list_a total length = m + n + k
#         n = len(list_b)
#         k = len(list_c)
#         m = len(list_a) - n - k
        
#         # Edge case: all arrays empty or list_a already contains everything
#         if n == 0 and k == 0:
#             return
        
#         # Start from end of valid elements in each array
#         # Example: list_a = [1, 5, 9, 0, 0, 0, 0], list_b = [2, 6], list_c = [3, 7]
#         # m = 7 - 2 - 2 = 3, valid elements in list_a are [1, 5, 9]
#         # p1 = 3 - 1 = 2 (points to 9)
#         p1 = m - 1
#         p2 = n - 1
#         p3 = k - 1
        
#         # Start from end of list_a's total capacity
#         p = len(list_a) - 1
        
#         # Continue while any array has elements to merge
#         while p1 >= 0 or p2 >= 0 or p3 >= 0:
#             # Get current values from each array (use -infinity if exhausted)
#             val1 = list_a[p1] if p1 >= 0 else float('-inf')
#             val2 = list_b[p2] if p2 >= 0 else float('-inf')
#             val3 = list_c[p3] if p3 >= 0 else float('-inf')
            
#             # Find maximum of the three values
#             # Place the largest at position p and move corresponding pointer
#             if val1 >= val2 and val1 >= val3:
#                 list_a[p] = val1
#                 p1 -= 1
#             elif val2 >= val1 and val2 >= val3:
#                 list_a[p] = val2
#                 p2 -= 1
#             else:
#                 list_a[p] = val3
#                 p3 -= 1
            
#             p -= 1
        
#         # No need to copy remaining list_a elements - already in place
