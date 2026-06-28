"""
LeetCode 1209. Remove All Adjacent Duplicates in String II
Difficulty: Medium
URL: https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/
"""

# Brute Force : 

# Approach : Stack

class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        """
        Remove k consecutive duplicate characters using a stack.
        
        Approach:
        - Use stack to store [character, count] pairs
        - When we see same char, increment count
        - When count reaches k, pop (remove all k chars)
        - When we see different char, start new entry
        
        Time Complexity: O(n)
        - Single pass through string: O(n)
        - Each character pushed once: O(n)
        - Each character popped once: O(n)
        - Building result: O(n)
        - Total: O(n)
        
        Space Complexity: O(n)
        - Stack can hold up to n entries in worst case
        - Example: "abcdef" with k=2 → stack has 6 entries

        Note ON CASCADING (no post-pop recheck needed, unlike the
        "remove all runs" variant): here k is fixed, so a pop is
        triggered by the MATCHING char itself reaching count==k --
        it's already consumed by the pop, nothing's left in hand.
        Example: "deeedbbcccbdaa", k=3 -- 'e' hits count 3 -> pop ->
        stack top is now 'd'. The next char in s is 'd', handled
        normally on the next iteration -> merges to ['d',2]. No
        special recheck logic required.
        """
        # Stack stores [character, count] pairs
        stack = []
        
        for char in s:
            # If stack not empty and top character matches current
            if stack and stack[-1][0] == char:
                # Increment count for this character
                stack[-1][1] += 1
                
                # If count reaches k, remove all k occurrences
                if stack[-1][1] == k:
                    stack.pop()
            else:
                # New character, push with count 1
                stack.append([char, 1])

        # No final-cleanup pop needed here (unlike "remove all runs",
        # where a run still in progress at end-of-string never gets
        # popped inside the loop, since its pop is mismatch-triggered).
        # Here, count==k is checked the instant count increments, so a
        # complete run-of-k can never survive to the end of the loop.
        # Example: "aab", k=2 -- count hits 2 on the 2nd 'a' and pops
        # immediately, mid-loop, regardless of what follows. Anything
        # still on the stack when the loop ends has count < k by
        # construction -- a real leftover, not an unfinished run.
        
        # Build result string from stack
        result = []
        for char, count in stack:
            result.append(char * count)  # Repeat char 'count' times
        
        return ''.join(result)

# Approach : Two pointers

class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        """
        Two-pointer in-place approach (simulating stack).
        
        Key Idea:
        - 'write' pointer indicates where to write next character (stack top + 1)
        - When we see k consecutive chars, move write pointer back by k
        - This simulates popping k elements from stack
        
        Time Complexity: O(n)
        Space Complexity: O(n) for chars array + counts array
        """
        # Convert to list for in-place modification
        chars = list(s)
        
        # counts[i] = number of consecutive identical chars ending at position i
        counts = [0] * len(s)
        
        # Write pointer (stack top position)
        write = 0
        
        for read in range(len(s)):
            # Place current character at write position
            chars[write] = chars[read]
            
            # Calculate count for this position
            if write == 0:
                # First position
                counts[write] = 1
            elif chars[write] == chars[write - 1]:
                # Same as previous character
                counts[write] = counts[write - 1] + 1
            else:
                # Different from previous character
                counts[write] = 1
            
            # If we've accumulated k consecutive chars, remove them
            if counts[write] == k:
                write -= k  # Move write pointer back (simulate k pops)
            
            # Move write pointer forward for next character
            write += 1
        
        # Return valid portion of the array
        return ''.join(chars[:write])


# Check Leetcode 723 Candy Crush 


# Candy Crush (1D Variant) (https://leetcode.com/discuss/post/380650/bloomberg-phone-candy-crush-1d-by-suprit-r11f/)

# You are given a string s consisting of lowercase letters, representing a row of candies on a one-dimensional board, where each letter represents a distinct candy type.

# A crush consists of choosing a maximal sequence of 3 or more adjacent candies of the same type and removing them from the board. When a sequence is removed, the candies on the left and right sides of the removed sequence become adjacent to each other, and may now form a new crushable sequence.

# Repeatedly perform crushes, processing from left to right, until no more crushes are possible. Return the final string.

# It is guaranteed that performing crushes greedily from left to right produces a valid final board (though, as explored in the follow-up, it may not be the only possible final result, nor necessarily the shortest).

# Example 1:
# Input: s = "aaabbbc"
# Output: "c"

# Explanation:
# Remove "aaa" (leftmost run of 3+): "aaabbbc" -> "bbbc"
# Remove "bbb": "bbbc" -> "c"
# No more crushes possible.

# Example 2:
# Input: s = "aabbbacd"
# Output: "cd"

# Explanation:
# Remove "bbb": "aabbbacd" -> "aaacd"
# Remove "aaa": "aaacd" -> "cd"
# No more crushes possible.

# Example 3:
# Input: s = "aabbccddeeedcba"
# Output: ""

# Explanation:
# Remove "eee": "aabbccddeeedcba" -> "aabbccdddcba"
# Remove "ddd": "aabbccdddcba" -> "aabbcccba"
# Remove "ccc": "aabbcccba" -> "aabbba"
# Remove "bbb": "aabbba" -> "aaa"
# Remove "aaa": "aaa" -> ""

# Approach : Stack

# def crush_candy(s: str) -> str:
#     """
#     Crush all runs of 3+ identical adjacent candies, greedily left to
#     right, cascading until no more crushes are possible.
    
#     Stack of [char, count] pairs. A pop is triggered by a MISMATCH (the
#     incoming char differs from the top), so after popping we must recheck
#     the new top against the same pending char -- it may now match and
#     need to merge. Example: "aabbbacd" -- popping "bbb" exposes top 'a',
#     and the pending char is also 'a' -> merge to count 3 -> then THAT
#     becomes poppable too. Skipping this recheck would corrupt the stack.
    
#     Time: O(n) -- each char pushed/popped/incremented O(1) times
#     Space: O(n) worst case (no removable runs, e.g. "abcdef")
#     """
#     stack = []  # [char, count]

#     for char in s:
#         if stack and stack[-1][0] == char:
#             stack[-1][1] += 1
#         else:
#             # Previous run is "closed" by this mismatch -- remove if >= 3
#             if stack and stack[-1][1] >= 3:
#                 stack.pop()
#             # Recheck: pending char may now match the newly exposed top
#             if stack and stack[-1][0] == char:
#                 stack[-1][1] += 1
#             else:
#                 stack.append([char, 1])

#     # Trailing run never hit a mismatch to trigger its pop -- catch it here
#     if stack and stack[-1][1] >= 3:
#         stack.pop()

#     return ''.join(char * count for char, count in stack)



# Follow-up: (complicated)

# Removal order can affect the final result when multiple crushable runs exist simultaneously — greedy left-to-right is not guaranteed to produce the shortest possible final string. 

# Given the same input, find the length of the shortest string achievable over all valid orders of crushing.

# Input: s = "aaabbbacd"
# Output: "cd" (length 2)
# Explanation:

# Removing "bbb" first instead of "aaa": "aaabbbacd" -> "aaaacd"
# The 'a' freed up by removing "bbb" merges with the existing run of 3 'a's,
# forming a run of 4 -> remove "aaaa": "aaaacd" -> "cd"
# This is shorter than the greedy left-to-right result, "acd".

# def shortest_after_crush(s: str) -> str:
#     """
#     Follow-up: find the SHORTEST string achievable, over all valid orders
#     of crushing runs of length >= 3 (with cascading).
    
#     Why greedy left-to-right isn't optimal here:
#     Removing a different (non-leftmost) run first can expose a bigger
#     merge later. Example: "aaabbba"
#       - Greedy (remove "aaa" first): "aaabbba" -> "bbba" -> "a"
#         (length 1)
#       - Remove "bbb" first instead: "aaabbba" -> "aaaa"
#         The leftover 'a's on either side of the removed "bbb" merge into
#         a run of 4 -> also removable -> "aaaa" -> "" (length 0, shorter!)
#     So the choice of WHICH run to remove first changes the final result.
#     We can't just always take the leftmost run -- we must explore all
#     choices and keep the best one.
    
#     Approach:
#     At each state (current string), find every maximal run of length
#     >= 3. For each one, try removing it and recurse on what's left.
#     Take whichever branch yields the shortest final string. Memoize on
#     the string itself, since different removal orders can converge on
#     the same intermediate string -- solving it twice would be wasted work.
    
#     Time Complexity (per single call to helper(s), excluding recursion):
#     - Scanning phase: O(n). The i/j run-finding loop visits each
#       character exactly once across the whole scan (i always jumps
#       straight to j, never re-examining a character already classified)
#       -- so this part alone is linear, same as in the basic crush problem.
#     - Rebuilding phase: O(n^2). Every time a removable run is found,
#       remainder = s[:i] + s[j:] costs O(n) (slicing copies characters
#       into a new string). In the worst case there can be up to O(n)
#       separate removable runs in one string (e.g. many short runs each
#       of length exactly 3), and EACH one triggers its own O(n) rebuild
#       -> O(n) runs * O(n) per rebuild = O(n^2).
#     - The rebuild cost dominates the scan cost, so total per-call work
#       (excluding recursive calls) is O(n) + O(n^2) = O(n^2).
#     - Memoization guarantees each distinct intermediate string is fully
#       processed only once. 
      
#       Total time = O(n^2) * (number of distinct
#       reachable states).

#     - The number of distinct reachable states does not have a tight
#       known closed-form bound for this problem; it depends on how many
#       genuinely different intermediate strings are produced by different
#       removal orders, which varies with the structure of the input.
    
#     Space Complexity:
#     - O(n) per memo entry (one string stored per distinct state), so
#       total memo space is O(n * number of distinct reachable states).
#     - Recursion depth is at most O(n), since every removal shrinks the
#       string by at least 3 characters.
#     """
#     memo = {}

#     def helper(s):
#         # Already solved this exact intermediate string via some other
#         # removal order -- reuse it instead of recomputing
#         if s in memo:
#             return memo[s]

#         n = len(s)
#         candidates = []  # results of trying each possible run removal

#         # i = start index of the run currently being examined.
#         # j = first index AFTER that run (i.e. where it ends / breaks).
#         # So at any point, s[i:j] is the maximal run starting at i.
#         i = 0
#         while i < n:
#             j = i
#             # Advance j while it's still in bounds and still matches
#             # the character that started this run (s[i]). When this
#             # inner loop exits, s[i:j] is exactly one full run.
#             while j < n and s[j] == s[i]:
#                 j += 1

#             run_length = j - i
#             if run_length >= 3:
#                 # This run (s[i:j]) is removable. Try removing IT
#                 # specifically (not necessarily the leftmost one we'd
#                 # pick under plain greedy crushing), recurse on what's
#                 # left, and ONLY THEN move on -- this call fully
#                 # completes and returns before we look for the next run.
#                 remainder = s[:i] + s[j:]
#                 candidates.append(helper(remainder))

#             # Jump i to j: the next run starts exactly where this one
#             # ended, so there's no need to re-examine any character
#             # between the old i and j -- they're already classified.
#             i = j

#         # No removable run found -- this string is final, nothing left
#         # to crush
#         if not candidates:
#             result = s
#         else:
#             # Pick whichever removal choice led to the shortest outcome
#             result = min(candidates, key=len)

#         memo[s] = result
#         return result

#     return helper(s)

# Example : s = "aaabbba" Output = ""

# Dry Run:

# 🔵 CALL A: helper("aaabbba"), n=7
# candidates = []
# i=0: j=0 → inner: s[0]='a'==s[0]→j=1; s[1]='a'==s[0]→j=2; s[2]='a'==s[0]→j=3; s[3]='b'≠s[0]→stop. Run s[0:3]="aaa", length 3 → removable.

# remainder = s[:0]+s[3:] = ""+"bbba" = "bbba"

# 📞 call helper("bbba") → (Call B, see below) → returns "a"

# candidates = ["a"]

# i = j = 3
# i=3: j=3 → inner: s[3]='b'==s[3]→j=4; s[4]='b'==s[3]→j=5; s[5]='b'==s[3]→j=6; s[6]='a'≠s[3]→stop. Run s[3:6]="bbb", length 3 → removable.

# remainder = s[:3]+s[6:] = "aaa"+"a" = "aaaa"

# 📞 call helper("aaaa") → (Call C, see below) → returns ""

# candidates = ["a", ""]

# i = j = 6
# i=6: j=6 → inner: s[6]='a'==s[6]→j=7; check j<n→7<7→false→stop. Run s[6:7]="a", length 1 → not removable. Nothing appended.

# i = j = 7
# Check outer loop: 7 < 7 → false → loop ends.
# candidates = ["a", ""] → result = min(["a",""], key=len) = ""

# memo["aaabbba"] = ""

# 🔙 Call A returns "" ✓ matches before

# 🟢 CALL B: helper("bbba"), n=4
# candidates = []
# i=0: j=0 → inner: s[0]='b'==s[0]→j=1; s[1]='b'==s[0]→j=2; s[2]='b'==s[0]→j=3; s[3]='a'≠s[0]→stop. Run s[0:3]="bbb", length 3 → removable.

# remainder = s[:0]+s[3:] = ""+"a" = "a"

# 📞 call helper("a") → (Call D, see below) → returns "a"

# candidates = ["a"]

# i = j = 3
# i=3: j=3 → inner: s[3]='a'==s[3]→j=4; check j<n→4<4→false→stop. Run s[3:4]="a", length 1 → not removable. Nothing appended.

# i = j = 4
# Check outer loop: 4 < 4 → false → loop ends.
# candidates = ["a"] → result = "a"

# memo["bbba"] = "a"

# 🔙 Call B returns "a" ✓ matches the corrected version from last message

# 🟡 CALL D: helper("a"), n=1
# candidates = []
# i=0: j=0 → inner: s[0]='a'==s[0]→j=1; check j<n→1<1→false→stop. Run s[0:1]="a", length 1 → not removable. Nothing appended.

# i = j = 1
# Check outer loop: 1 < 1 → false → loop ends.
# candidates = [] → empty → result = s = "a"

# memo["a"] = "a"

# 🔙 Call D returns "a" ✓ matches

# 🟢 CALL C: helper("aaaa"), n=4
# candidates = []
# i=0: j=0 → inner: s[0]='a'==s[0]→j=1; s[1]='a'==s[0]→j=2; s[2]='a'==s[0]→j=3; s[3]='a'==s[0]→j=4; check j<n→4<4→false→stop. Run s[0:4]="aaaa", length 4 → removable.

# remainder = s[:0]+s[4:] = ""+"" = ""

# 📞 call helper("") → (Call E, see below) → returns ""

# candidates = [""]

# i = j = 4
# Check outer loop: 4 < 4 → false → loop ends.
# candidates = [""] → result = ""

# memo["aaaa"] = ""

# 🔙 Call C returns "" ✓ matches

# 🟡 CALL E: helper(""), n=0
# Check outer loop immediately: 0 < 0 → false → loop body never executes, not even once.
# candidates = [] → empty → result = s = ""

# memo[""] = ""

# 🔙 Call E returns "" ✓ matches

# memo = {"a": "a", "bbba": "a", "": "", "aaaa": "", "aaabbba": ""}

        
        