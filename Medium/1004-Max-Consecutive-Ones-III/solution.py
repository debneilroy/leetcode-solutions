"""
LeetCode 1004. Max Consecutive Ones III
Difficulty: Medium
URL: https://leetcode.com/problems/max-consecutive-ones-iii/
"""

# Approach : Sliding Window

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        """
        Sliding window with an explicit zero counter.

        Expand the window rightward freely. When the number of zeros inside
        the window exceeds k, shrink from the left until we're back within
        budget. Track the largest valid window seen.

        Example (shrink never triggers — k is never exceeded):
            nums = [1, 1, 0, 0, 1, 1, 1], k = 2
            indices: 0  1  2  3  4  5  6

            right=0: nums[0]=1, zeros=0, window=[1],             left=0, size=1, ans=1
            right=1: nums[1]=1, zeros=0, window=[1,1],           left=0, size=2, ans=2
            right=2: nums[2]=0, zeros=1, window=[1,1,0],         left=0, size=3, ans=3
            right=3: nums[3]=0, zeros=2, window=[1,1,0,0],       left=0, size=4, ans=4
                       zeros==k=2, still valid — no shrink needed
            right=4: nums[4]=1, zeros=2, window=[1,1,0,0,1],     left=0, size=5, ans=5
            right=5: nums[5]=1, zeros=2, window=[1,1,0,0,1,1],   left=0, size=6, ans=6
            right=6: nums[6]=1, zeros=2, window=[1,1,0,0,1,1,1], left=0, size=7, ans=7
            => 7

        Example (shrink triggers):
            nums = [1, 1, 0, 0, 0, 1, 1], k = 1
            indices: 0  1  2  3  4  5  6

            right=0: nums[0]=1, zeros=0, window=[1],      left=0, size=1, ans=1
            right=1: nums[1]=1, zeros=0, window=[1,1],    left=0, size=2, ans=2
            right=2: nums[2]=0, zeros=1, window=[1,1,0],  left=0, size=3, ans=3
                       zeros==k=1, still valid
            right=3: nums[3]=0, zeros=2 > k=1 — SHRINK:
                       nums[left=0]=1, not a zero, left->1
                       nums[left=1]=1, not a zero, left->2
                       nums[left=2]=0, zero! zeros->1,  left->3
                     window=[0],                         left=3, size=1, ans=3
            right=4: nums[4]=0, zeros=2 > k=1 — SHRINK:
                       nums[left=3]=0, zero! zeros->1,  left->4
                     window=[0],                         left=4, size=1, ans=3
            right=5: nums[5]=1, zeros=1, window=[0,1],   left=4, size=2, ans=3
            right=6: nums[6]=1, zeros=1, window=[0,1,1], left=4, size=3, ans=3
            => 3

        TC: O(n) — each element is added and removed from the window at most once.
        SC: O(1) — only a handful of integer variables.
        """
        left = 0   # left boundary of the window; everything to the left has been discarded
        zeros = 0  # number of zeros currently inside window [left, right]
        ans = 0    # best window size seen so far

        for right in range(len(nums)):
            # expand window to include nums[right]
            if nums[right] == 0:
                zeros += 1

            # window has too many zeros — shrink from the left until valid again (zeros <= k)
            # we use while (not if) because we may need to move left
            # past several 1s before hitting the zero that fixes the count.
            # in this problem the while body fires at most once per step (O(1)),
            # but while is correct in general and makes the intent clear.
            while zeros > k:
                if nums[left] == 0:
                    zeros -= 1  # evicting a zero frees up one unit of budget
                left += 1 # discard nums[left] from the window

            # window [left, right] is valid; record its size
            ans = max(ans, right - left + 1)

        return ans

# Another version using k itself

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        """
        Sliding window where k itself serves as the remaining zero budget.

        Core idea:
            - right expands the window by 1 every iteration
            - when a zero is encountered, k decreases by 1
            - when k goes negative (budget exceeded), shrink from the left
              until budget is restored
            - when a zero is evicted from the left, k is restored by 1
            - since while shrinks the window fully, we must track ans explicitly
              to remember the best window seen so far

        Window size behavior with while:
            k >= 0 (valid):    right+1, left stays  => size grows by 1
            k <  0 (exceeded): right+1, left moves until k>=0 => size may shrink

        Example:
            nums = [1,1,0,0,0,1,1], k=1
            indices: 0 1 2 3 4 5 6

            with while:                               with if:
            right=3: left moves 0->1->2->3, size=1    right=3: left moves 0->1, size=3
            right=4: left moves 3->4,       size=1    right=4: left moves 1->2, size=3
            right=5: left moves 4->4,       size=2    right=5: left moves 2->3, size=3
            right=6: left stays,            size=3    right=6: left moves 3->4, size=3
            ans tracked explicitly = 3 ✓              len(nums) - left = 7-4 = 3 ✓

        TC: O(n) — right moves n steps, left moves at most n steps.
        SC: O(1) — only two pointers and k.
        """
        left = 0
        ans = 0

        for right in range(len(nums)):
            # expand window: consume budget if nums[right] is a zero
            if nums[right] == 0:
                k -= 1

            # --- WHILE VERSION (used here) ---
            # shrinks window fully until budget is restored
            # left moves as many times as needed in a single iteration
            # window CAN shrink, so ans must be tracked explicitly
            while k < 0:
                if nums[left] == 0:
                    k += 1
                left += 1

            # --- IF VERSION (alternative) ---
            # if k < 0:
            #     if nums[left] == 0:
            #         k += 1
            #     left += 1
            #
            # difference vs while:
            #   while: left moves until k >= 0  — window shrinks to smallest valid size
            #   if:    left moves exactly once  — window stays same size or grows
            #
            # consequence:
            #   while: window can shrink, so ans = max(ans, ...) is required
            #   if:    window never shrinks, so ans is optional — len(nums)-left works

            # required with while since window can shrink
            # optional with if — could just return len(nums) - left
            ans = max(ans, right - left + 1)

        return ans  # if version: can return len(nums) - left instead


# Variant 1 : Longest Vacation

# Given an array of characters days where days[i] is either 'W' (workday) or 'H' (holiday), return the longest consecutive vacation you can take. You may use at most PTO paid time off days to convert workdays into vacation days.

# Example 1:
# Input:  days = ['W','H','H','W','W','H','W'], PTO = 2
# Output: 5
# Explanation: ['W',H,H,W,W,H,'W']
#              Convert days[3] and days[4] from W to H.
#              Longest vacation is days[1..5] = [H,H,H,H,H], length 5.

# Example 2:
# Input:  days = ['W','W','W','H','H','W'], PTO = 0
# Output: 2
# Explanation: No days can be converted.
#              Longest existing vacation is days[3..4] = [H,H], length 2.

# Constraints:
# 1. 1 <= days.length <= 10^5
# 2. days[i] is either 'W' or 'H'
# 3. 0 <= PTO <= days.length

# class Solution:
#     def longestVacation_v1(self, days: List[str], PTO: int) -> int:
#         """
#         Approach 1 : Sliding window with explicit workday counter.

#         Direct translation of LC 1004 v1 — only change is:
#             nums[i] == 0  =>  days[i] == 'W'  (workday costs PTO)
#             nums[i] == 1  =>  days[i] == 'H'  (holiday is free)
#             k             =>  PTO

#         Example (shrink never triggers):
#             days = [H,H,W,W,H,H,H], PTO=2
#             indices: 0 1 2 3 4 5 6

#             right=0: days[0]=H, work=0, window=[H],           left=0, size=1, max_vacation=1
#             right=1: days[1]=H, work=0, window=[H,H],         left=0, size=2, max_vacation=2
#             right=2: days[2]=W, work=1, window=[H,H,W],       left=0, size=3, max_vacation=3
#             right=3: days[3]=W, work=2, window=[H,H,W,W],     left=0, size=4, max_vacation=4
#                        work==PTO=2, still valid — no shrink needed
#             right=4: days[4]=H, work=2, window=[H,H,W,W,H],   left=0, size=5, max_vacation=5
#             right=5: days[5]=H, work=2, window=[H,H,W,W,H,H], left=0, size=6, max_vacation=6
#             right=6: days[6]=H, work=2, window=[H,H,W,W,H,H,H],left=0,size=7, max_vacation=7
#             => 7

#         Example (shrink triggers):
#             days = [W,H,H,W,W,H,W], PTO=2
#             indices: 0 1 2 3 4 5 6

#             right=0: days[0]=W, work=1, window=[W],         left=0, size=1, max_vacation=1
#             right=1: days[1]=H, work=1, window=[W,H],       left=0, size=2, max_vacation=2
#             right=2: days[2]=H, work=1, window=[W,H,H],     left=0, size=3, max_vacation=3
#             right=3: days[3]=W, work=2, window=[W,H,H,W],   left=0, size=4, max_vacation=4
#                        work==PTO=2, still valid — no shrink needed
#             right=4: days[4]=W, work=3 > PTO=2 — SHRINK:
#                        days[left=0]=W, work->2, left->1
#                      window=[H,H,W,W],           left=1, size=4, max_vacation=4
#             right=5: days[5]=H, work=2, window=[H,H,W,W,H], left=1, size=5, max_vacation=5
#             right=6: days[6]=W, work=3 > PTO=2 — SHRINK:
#                        days[left=1]=H, not W, left->2
#                        days[left=2]=H, not W, left->3
#                        days[left=3]=W, work->2, left->4
#                      window=[W,H,W],              left=4, size=3, max_vacation=5
#             => 5

#         TC: O(n) — each element is added and removed from the window at most once.
#         SC: O(1) — only a handful of integer variables.
#         """

#         left = 0          # left boundary of window; moves forward when PTO is exceeded
#         work = 0          # number of workdays currently inside window [left, right]
#         max_vacation = 0  # longest consecutive vacation found so far

#         for right in range(len(days)):
#             # expand window: consume PTO if we just included a workday
#             # CHANGE from LC 1004: nums[right] == 0  =>  days[right] == 'W'
#             if days[right] == 'W':
#                 work += 1

#             # shrink from left until workdays in window <= PTO
#             # we use while (not if) because we may need to skip past
#             # several holidays before hitting the workday that fixes the count
#             # in this problem the while body fires at most once per step,
#             # but while is correct in general and makes the intent clear
#             while work > PTO:
#                 if days[left] == 'W':  # CHANGE from LC 1004: nums[left] == 0  =>  days[left] == 'W'
#                     work -= 1          # evicting a workday restores one PTO unit
#                 left += 1              # discard days[left] from the window

#             max_vacation = max(max_vacation, right - left + 1)

#         return max_vacation

# class Solution:
#     def longestVacation_v2(self, days: List[str], PTO: int) -> int:
#         """
#         Approach 2 : Sliding window where PTO itself serves as the remaining budget.

#         Direct translation of LC 1004 v2 — only change is:
#             nums[i] == 0  =>  days[i] == 'W'  (workday costs PTO)
#             nums[i] == 1  =>  days[i] == 'H'  (holiday is free)
#             k             =>  PTO

#         Window size behavior with while:
#             PTO >= 0 (valid):    right+1, left stays             => size grows by 1
#             PTO <  0 (exceeded): right+1, left moves until PTO>=0 => size may shrink

#         Example (shrink never triggers):
#             days = [H,H,W,W,H,H,H], PTO=2
#             indices: 0 1 2 3 4 5 6

#             right=0: days[0]=H, PTO=2,       left=0, size=1
#             right=1: days[1]=H, PTO=2,       left=0, size=2
#             right=2: days[2]=W, PTO=1,       left=0, size=3
#             right=3: days[3]=W, PTO=0,       left=0, size=4
#             right=4: days[4]=H, PTO=0,       left=0, size=5
#             right=5: days[5]=H, PTO=0,       left=0, size=6
#             right=6: days[6]=H, PTO=0,       left=0, size=7
#             => len(days) - left = 7 - 0 = 7

#         Example (shrink triggers):
#             days = [W,H,H,W,W,H,W], PTO=2
#             indices: 0 1 2 3 4 5 6

#             with while:                                        with if:
#             right=4: left moves 0->1, PTO->0,    size=4       right=4: left moves 0->1, PTO->0,  size=4
#             right=6: left moves 2->3->4, PTO->0, size=3       right=6: left moves 2->3, PTO stays-1, size=5
#             max_vacation tracked explicitly = 5 ✓             len(days) - left = 7-2 = 5 ✓

#         TC: O(n) — right moves n steps, left moves at most n steps.
#         SC: O(1) — only two pointers and PTO.
#         """

#         left = 0          # left boundary of window; moves forward when PTO is exceeded
#         max_vacation = 0  # longest consecutive vacation found so far
#                           # required with while since window can shrink
#                           # optional with if — len(days)-left works too

#         for right in range(len(days)):
#             # expand window: consume PTO if we just included a workday
#             # CHANGE from LC 1004: nums[right] == 0  =>  days[right] == 'W'
#             if days[right] == 'W':
#                 PTO -= 1

#             # --- WHILE VERSION (used here) ---
#             # shrinks window fully until PTO budget is restored
#             # left moves as many times as needed in a single iteration
#             # window CAN shrink, so max_vacation must be tracked explicitly
#             while PTO < 0:
#                 if days[left] == 'W':  # CHANGE from LC 1004: nums[left] == 0  =>  days[left] == 'W'
#                     PTO += 1           # evicting a workday restores one PTO unit
#                 left += 1             # discard days[left] from the window

#             # --- IF VERSION (alternative) ---
#             # if PTO < 0:
#             #     if days[left] == 'W':
#             #         PTO += 1
#             #     left += 1
#             #
#             # difference vs while:
#             #   while: left moves until PTO >= 0  — window shrinks to smallest valid size
#             #   if:    left moves exactly once    — window stays same size or grows
#             #
#             # consequence:
#             #   while: window can shrink, so max_vacation = max(...) is required
#             #   if:    window never shrinks, so max_vacation is optional — len(days)-left works

#             # required with while since window can shrink
#             # optional with if — could just return len(days) - left
#             max_vacation = max(max_vacation, right - left + 1)

#         return max_vacation  # if version: can return len(days) - left instead


# Variant 2 

# Given an array of booleans year where False represents a workday and True represents a paid holiday, return the longest consecutive vacation you can take. You may use at most PTO days off to convert workdays into vacation days.

# Example 1:
# Input:  year = [F,T,T,F,F,T,F], PTO = 2
# Output: 5
# Explanation: [F,T,T,F,F,T,F]
#              Convert year[3] and year[4] from F to T.
#              Longest vacation is year[1..5] = [T,T,T,T,T], length 5.

# Example 2:
# Input:  year = [F,F,F,T,T,F], PTO = 0
# Output: 2
# Explanation: No days can be converted.
#              Longest existing vacation is year[3..4] = [T,T], length 2.

# Constraints:
# 1. 1 <= year.length <= 10^5
# 2. year[i] is either False or True
# 3. 0 <= PTO <= year.length

# class Solution:
#     def longestVacation_v1(self, year: List[bool], PTO: int) -> int:
#         """
#         Sliding window with explicit workday counter.
#         Direct translation of LC 1004 v1 — only change is:
#             nums[i] == 0  =>  not year[i]  (False = workday, costs PTO)
#             nums[i] == 1  =>  year[i]      (True  = holiday, free)
#             k             =>  PTO

#         Example (shrink never triggers):
#             year = [T,T,F,F,T,T,T], PTO=2
#             indices: 0 1 2 3 4 5 6

#             right=0: year[0]=T, work=0, window=[T],           left=0, size=1, max_vacation=1
#             right=1: year[1]=T, work=0, window=[T,T],         left=0, size=2, max_vacation=2
#             right=2: year[2]=F, work=1, window=[T,T,F],       left=0, size=3, max_vacation=3
#             right=3: year[3]=F, work=2, window=[T,T,F,F],     left=0, size=4, max_vacation=4
#                        work==PTO=2, still valid — no shrink needed
#             right=4: year[4]=T, work=2, window=[T,T,F,F,T],   left=0, size=5, max_vacation=5
#             right=5: year[5]=T, work=2, window=[T,T,F,F,T,T], left=0, size=6, max_vacation=6
#             right=6: year[6]=T, work=2, window=[T,T,F,F,T,T,T],left=0,size=7, max_vacation=7
#             => 7

#         Example (shrink triggers):
#             year = [F,T,T,F,F,T,F], PTO=2
#             indices: 0 1 2 3 4 5 6

#             right=0: year[0]=F, work=1, window=[F],         left=0, size=1, max_vacation=1
#             right=1: year[1]=T, work=1, window=[F,T],       left=0, size=2, max_vacation=2
#             right=2: year[2]=T, work=1, window=[F,T,T],     left=0, size=3, max_vacation=3
#             right=3: year[3]=F, work=2, window=[F,T,T,F],   left=0, size=4, max_vacation=4
#                        work==PTO=2, still valid — no shrink needed
#             right=4: year[4]=F, work=3 > PTO=2 — SHRINK:
#                        not year[left=0]=True, work->2, left->1
#                      window=[T,T,F,F],           left=1, size=4, max_vacation=4
#             right=5: year[5]=T, work=2, window=[T,T,F,F,T], left=1, size=5, max_vacation=5
#             right=6: year[6]=F, work=3 > PTO=2 — SHRINK:
#                        not year[left=1]=False, not a workday, left->2
#                        not year[left=2]=False, not a workday, left->3
#                        not year[left=3]=True,  work->2, left->4
#                      window=[F,T,F],              left=4, size=3, max_vacation=5
#             => 5

#         TC: O(n) — each element is added and removed from the window at most once.
#         SC: O(1) — only a handful of integer variables.
#         """

#         left = 0          # left boundary of window; moves forward when PTO is exceeded
#         work = 0          # number of workdays currently inside window [left, right]
#         max_vacation = 0  # longest consecutive vacation found so far

#         for right in range(len(year)):
#             # expand window: consume PTO if we just included a workday
#             # CHANGE from LC 1004: nums[right] == 0  =>  not year[right]
#             if not year[right]:
#                 work += 1

#             # shrink from left until workdays in window <= PTO
#             # we use while (not if) because we may need to skip past
#             # several holidays before hitting the workday that fixes the count
#             # in this problem the while body fires at most once per step,
#             # but while is correct in general and makes the intent clear
#             while work > PTO:
#                 if not year[left]:  # CHANGE from LC 1004: nums[left] == 0  =>  not year[left]
#                     work -= 1       # evicting a workday restores one PTO unit
#                 left += 1          # discard year[left] from the window

#             max_vacation = max(max_vacation, right - left + 1)

#         return max_vacation

#     def longestVacation_v2(self, year: List[bool], PTO: int) -> int:
#         """
#         Sliding window where PTO itself serves as the remaining budget.
#         Direct translation of LC 1004 v2 — only change is:
#             nums[i] == 0  =>  not year[i]  (False = workday, costs PTO)
#             nums[i] == 1  =>  year[i]      (True  = holiday, free)
#             k             =>  PTO

#         Window size behavior with while:
#             PTO >= 0 (valid):    right+1, left stays             => size grows by 1
#             PTO <  0 (exceeded): right+1, left moves until PTO>=0 => size may shrink

#         Example (shrink never triggers):
#             year = [T,T,F,F,T,T,T], PTO=2
#             indices: 0 1 2 3 4 5 6

#             right=0: year[0]=T, PTO=2,       left=0, size=1
#             right=1: year[1]=T, PTO=2,       left=0, size=2
#             right=2: year[2]=F, PTO=1,       left=0, size=3
#             right=3: year[3]=F, PTO=0,       left=0, size=4
#             right=4: year[4]=T, PTO=0,       left=0, size=5
#             right=5: year[5]=T, PTO=0,       left=0, size=6
#             right=6: year[6]=T, PTO=0,       left=0, size=7
#             => len(year) - left = 7 - 0 = 7

#         Example (shrink triggers):
#             year = [F,T,T,F,F,T,F], PTO=2
#             indices: 0 1 2 3 4 5 6

#             with while:                                          with if:
#             right=4: left moves 0->1, PTO->0,    size=4         right=4: left moves 0->1, PTO->0,    size=4
#             right=6: left moves 2->3->4, PTO->0, size=3         right=6: left moves 2->3, PTO stays -1, size=5
#             max_vacation tracked explicitly = 5 ✓               len(year) - left = 7-2 = 5 ✓

#         TC: O(n) — right moves n steps, left moves at most n steps.
#         SC: O(1) — only two pointers and PTO.
#         """

#         left = 0          # left boundary of window; moves forward when PTO is exceeded
#         max_vacation = 0  # longest consecutive vacation found so far
#                           # required with while since window can shrink
#                           # optional with if — len(year)-left works too

#         for right in range(len(year)):
#             # expand window: consume PTO if we just included a workday
#             # CHANGE from LC 1004: nums[right] == 0  =>  not year[right]
#             if not year[right]:
#                 PTO -= 1

#             # --- WHILE VERSION (used here) ---
#             # shrinks window fully until PTO budget is restored
#             # left moves as many times as needed in a single iteration
#             # window CAN shrink, so max_vacation must be tracked explicitly
#             while PTO < 0:
#                 if not year[left]:  # CHANGE from LC 1004: nums[left] == 0  =>  not year[left]
#                     PTO += 1        # evicting a workday restores one PTO unit
#                 left += 1          # discard year[left] from the window

#             # --- IF VERSION (alternative) ---
#             # if PTO < 0:
#             #     if not year[left]:
#             #         PTO += 1
#             #     left += 1
#             #
#             # difference vs while:
#             #   while: left moves until PTO >= 0  — window shrinks to smallest valid size
#             #   if:    left moves exactly once    — window stays same size or grows
#             #
#             # consequence:
#             #   while: window can shrink, so max_vacation = max(...) is required
#             #   if:    window never shrinks, so max_vacation is optional — len(year)-left works

#             # required with while since window can shrink
#             # optional with if — could just return len(year) - left
#             max_vacation = max(max_vacation, right - left + 1)

#         return max_vacation  # if version: can return len(year) - left instead







        