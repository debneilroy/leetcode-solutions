"""
LeetCode 26. Remove Duplicates from Sorted Array
Difficulty: Easy
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
"""

class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        """
        Two-pointer: 'slow' marks the last position of a confirmed-unique
        element. 'fast' scans ahead looking for the next new value.

        Time Complexity:  O(n) - single pass through nums
        Space Complexity: O(1) - modifies nums in place, no extra structures
        """
        if not nums:
            return 0

        # slow = index of the last unique element written so far.
        # Before the loop: nums[0] is trivially unique (it's the only
        # element seen), so slow starts at 0.
        slow = 0

        # fast scans from index 1 to the end, checking every candidate.
        for fast in range(1, len(nums)):
            # Compare candidate against the LAST CONFIRMED unique value,
            # not the previous index. Since nums is sorted, all duplicates
            # of nums[slow] are guaranteed to be contiguous — so this
            # single comparison is enough to catch them all.
            #
            # Example: nums = [0,0,1,1,1,2,2,3]
            #                   s f
            # nums[fast]=0 == nums[slow]=0 -> duplicate, skip (fast++, slow stays)
            if nums[fast] != nums[slow]:
                # Found a genuinely new value. Advance slow first (opens
                # up the next writable slot), THEN place nums[fast] there.
                #
                # Before: nums = [0,0,1,1,1,2,2,3], slow=0, fast=2 (nums[fast]=1)
                # After:  nums = [0,1,1,1,1,2,2,3], slow=1
                slow += 1
                nums[slow] = nums[fast]

        # slow is the index of the last unique element, so count = slow+1.
        return slow + 1
        