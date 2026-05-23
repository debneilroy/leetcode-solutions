"""
LeetCode 1216. Valid Palindrome III
Difficulty: Hard
URL: https://leetcode.com/problems/valid-palindrome-iii/
"""

# Approach : Recursion

class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        """
        Determines if string s can become a palindrome by removing at most k characters.
        Uses naive recursion (no memoization) — add @lru_cache on (left, right, k) for O(n^2 * k).

        TC: O(2^min(k,n)), Work per node → O(1)
            At each mismatch, two branches are explored (delete left or delete right),
            and branching depth is bounded by k (each branch decrements k by 1).
            Worst case when k >= n: every step mismatches and k never runs out,
            producing a full binary tree of depth n.

            Example — s = "abcde", k = 5 (all chars distinct, k >= n):
                (0,4,5): 'a'≠'e' → branches into (1,4,4) and (0,3,4)
                (1,4,4): 'b'≠'e' → branches into (2,4,3) and (1,3,3)
                (0,3,4): 'a'≠'d' → branches into (1,3,3) and (0,2,3)  ← (1,3,3) recomputed
                ...
            Total calls ≈ 2^5 = 32.

        SC: O(n)
            Each recursive call advances left or right by at least 1, so
            max recursion depth is n regardless of k.
        """

        # empty or single char is always a palindrome
        if len(s) <= 1:
            return True

        # k covers entire string, always possible
        if k >= len(s) - 1:
            return True

        def check_palindrome(s, left, right, k):
            # base case: left crossed right, valid palindrome
            if left >= right:
                return True

            # match: move inward without consuming k
            if s[left] == s[right]:
                return check_palindrome(s, left + 1, right - 1, k)

            # mismatch: k==0 check is here (not as standalone early return) because
            # matching chars must still proceed inward even when k==0.
            # e.g. s="aba", k=0 → 'a'=='a' → check(1,1,0) → True (correct)
            #      s="abc", k=0 → 'a'!='c', k==0 → False (correct)
            if k == 0:
                return False

            # try deleting left or right character
            return check_palindrome(s, left + 1, right, k - 1) or check_palindrome(s, left, right - 1, k - 1)

        return check_palindrome(s, 0, len(s) - 1, k)


# Approach : Top down recursion with memoization (preferred approach)

class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        """
        Return True if s can be made a palindrome by deleting at most k chars.
        
        Time Complexity: O(n²) where n = len(s)
            WHY IT'S O(n²):
            
            1. Number of Unique States:
               - Each state is defined by (i, j) where i <= j
               - For string of length n:
                 * i can be [0, n-1]
                 * j can be [i, n-1]
               - Total states = sum of (n-i) for i in [0, n-1]
                              = n + (n-1) + (n-2) + ... + 1
                              = n(n+1)/2
                              = O(n²)
            
            2. Work Per State:
               - Each state does O(1) work:
                 * Compare s[i] and s[j]: O(1)
                 * Make recursive calls: O(1) (already cached)
                 * Store in memo: O(1)
            
            3. Total Time = States × Work = O(n²) × O(1) = O(n²)
            
            WHY k DOESN'T MATTER:
            - k is only used in the final check: min_del <= k
            - The recursion explores ALL (i,j) pairs regardless of k
            - Even if k=0, we still compute min_deletions for all substrings
            - Even if k=1000, we still compute the same substrings
            
            Example: s = "abcd", k = 1 vs k = 100
            Both cases compute the SAME states:
            (0,0) (0,1) (0,2) (0,3)
                  (1,1) (1,2) (1,3)
                        (2,2) (2,3)
                              (3,3)
            k only affects the return value, not the computation!
        
        Space Complexity: O(n²)
            WHY IT'S O(n²):
            
            1. Memoization Dictionary:
               - Stores up to n(n+1)/2 = O(n²) entries
               - Each entry: ((i,j), min_deletions_value)
               - Dictionary overhead: O(n²)
            
            2. Recursion Call Stack:
               - Maximum depth occurs in worst case
               - Worst case: all characters different, always recurse deeper
               - Stack frames: (0,n-1) → (1,n-1) → (2,n-1) → ... → (n-1,n-1)
               - Or: (0,n-1) → (0,n-2) → (0,n-3) → ... → (0,0)
               - Maximum depth: O(n)
            
            3. Total Space = Memo + Stack = O(n²) + O(n) = O(n²)
            
            WHY k DOESN'T MATTER:
            - k doesn't affect how many states we store
            - k doesn't affect recursion depth
            - Memo size depends only on (i,j) pairs, not on k
        
        Memoization Cache Hits Example:
            Input: s = "abcabc", k = 2,  Output : False
            
            When we compute min_deletions(1, 4) for substring "bcab" in one branch,
            and later need the same substring in another branch, we get a cache hit
            and return the stored result immediately instead of recomputing.
            
            Note: States where i >= j (single character or empty) never cause cache
            hits because they return immediately via the base case before checking memo.
        
        Args:
            s: Input string to check
            k: Maximum number of deletions allowed
            
        Returns:
            True if s can become a palindrome with at most k deletions
        """
        
        def min_deletions(i: int, j: int) -> int:
            """
            Calculate minimum deletions needed to make s[i..j] a palindrome.
            
            Args:
                i: Left boundary index (inclusive)
                j: Right boundary index (inclusive)
                
            Returns:
                Minimum number of character deletions needed
            """
            # Base case 1: Empty string or single character is already a palindrome
            # 
            # i == j: Single character remains (ODD-length substring)
            #   Example: s = "aba", after matching outer 'a's, we reach middle 'b'
            #   min_deletions(1, 1) → single char 'b' → return 0
            #
            # i > j: Pointers have crossed (EVEN-length substring fully processed)
            #   Example: s = "abba", after matching 'a's and 'b's, pointers cross
            #   min_deletions(2, 1) → empty substring → return 0
            #
            # Both cases mean no more characters to check → 0 deletions needed
            if i >= j:
                return 0
            
            # Base case 2: Already computed this subproblem
            # Check if we've solved this (i, j) pair before
            if (i, j) in memo:
                return memo[(i, j)]  # Return cached result (avoids recomputation)
            
            # Case 1: Characters at boundaries match
            if s[i] == s[j]:
                # No deletion needed for these characters
                # Just solve for the inner substring s[i+1..j-1]
                res = min_deletions(i + 1, j - 1)
            else:
                # Case 2: Characters at boundaries don't match
                # We must delete one of them - try both options and take minimum
                
                # Option 1: Delete left character s[i]
                # Then solve for s[i+1..j]
                left = min_deletions(i + 1, j)
                
                # Option 2: Delete right character s[j]
                # Then solve for s[i..j-1]
                right = min_deletions(i, j - 1)
                
                # Add 1 for the deletion we just made, take minimum of both options
                res = 1 + min(left, right)
            
            # Cache the result for this subproblem before returning
            # This ensures if we encounter (i, j) again, we return immediately
            memo[(i, j)] = res
            return res


        # OPTIMIZATION: Early return when k is large enough
        # If we can delete n-1 characters, we're left with ≤1 character
        # Any string with ≤1 character is always a palindrome
        #
        # This check covers:
        # ✅ Empty strings (len=0): k >= -1 (always true)
        # ✅ Single characters (len=1): k >= 0 (true for valid k)
        # ✅ Large k cases: k >= n-1 guarantees palindrome possible
        #
        # Main code EXECUTES when: k < len(s) - 1
        # - Most common test cases: k=0,1,2,... with reasonable string lengths
        # - When we need to actually compute minimum deletions
        #
        # Main code NEVER EXECUTES when: k >= len(s) - 1
        # - Single characters with any valid k
        # - Empty strings
        # - Cases where k is large enough to delete almost everything
        if k >= len(s) - 1:
            return True

        n = len(s)
        
        # Memoization dictionary (cache) to avoid recomputing subproblems
        # Key: (i, j) tuple representing substring boundaries
        # Value: minimum deletions needed to make s[i..j] a palindrome
        memo = {}
        
        # Compute minimum deletions for entire string
        min_del = min_deletions(0, n - 1)
        
        # Check if we can achieve palindrome within k deletions
        return min_del <= k


# Without class

# def is_valid_palindrome(s: str, k: int) -> bool:
#     # Optimization: can always reduce to ≤1 char
#     if k >= len(s) - 1:
#         return True

#     memo = {}

#     def min_deletions(i: int, j: int) -> int:
#         if i >= j:
#             return 0
        
#         if (i, j) in memo:
#             return memo[(i, j)]
        
#         if s[i] == s[j]:
#             res = min_deletions(i + 1, j - 1)
#         else:
#             res = 1 + min(
#                 min_deletions(i + 1, j),
#                 min_deletions(i, j - 1)
#             )
        
#         memo[(i, j)] = res
#         return res

#     return min_deletions(0, len(s) - 1) <= k

# Using lru_cache

from functools import lru_cache

class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        """
        Return True if s can be made a palindrome by deleting at most k chars.

        TC: O(n²)
            - Unique states: (i, j) pairs where i <= j → n(n+1)/2 = O(n²)
            - Work per state: O(1) — compare chars, recursive calls hit cache
            - Total: O(n²) × O(1) = O(n²)
            - k doesn't affect state space — recursion explores all (i,j) pairs
              regardless of k; k only affects the final comparison min_del <= k

        SC: O(n²)
            - lru_cache stores up to O(n²) (i,j) entries
            - Recursion stack depth: O(n)
            - Total: O(n²) + O(n) = O(n²)

        lru_cache (Least Recently Used Cache):
            - Python decorator from functools that memoizes function results
            - Stores return value for each unique set of arguments as a key-value pair:
                key   : function arguments as a tuple, e.g. (i=1, j=3) → (1, 3)
                value : return value, e.g. min_deletions(1, 3) = 2
            - On repeated calls with same args, returns cached value in O(1)
            - maxsize=None: unlimited cache size (no eviction)
            - Requires arguments to be hashable — tuples/ints work, lists don't
            - Equivalent to manually maintaining a memo dict, but cleaner:
                manual : if (i,j) in memo: return memo[(i,j)]
                         memo[(i,j)] = result; return result
                lru     : @lru_cache(maxsize=None) handles this automatically
        """
        if k >= len(s) - 1:
            return True

        @lru_cache(maxsize=None)
        def min_deletions(i: int, j: int) -> int:
            # base case: single char or crossed pointers → already a palindrome
            if i >= j:
                return 0

            # match: no deletion needed, solve inner substring
            if s[i] == s[j]:
                return min_deletions(i + 1, j - 1)

            # mismatch: delete left or right, take minimum
            return 1 + min(min_deletions(i + 1, j), min_deletions(i, j - 1))

        return min_deletions(0, len(s) - 1) <= k


# k aware solution 

class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        """
        Return True if s can be made a palindrome by deleting at most k chars.
        K-aware approach: threads deletions_left through recursion for early pruning.

        TC: O(n² × k)
            - Unique states: (i, j, deletions_left) → O(n²) × O(k) = O(n²k)
            - Work per state: O(1)
            - Same (i,j) reachable with different deletions_left values via
              different deletion paths, so k is part of the state space.
            - Best case O(n²): small k, heavy early pruning via deletions_left == 0

        SC: O(n² × k)
            - memo stores up to O(n²k) (i, j, deletions_left) entries
            - Recursion stack depth: O(n)
            - Total: O(n²k) + O(n) = O(n²k)

        Comparison with k-unaware min_deletions approach:
            k-unaware : TC O(n²),   SC O(n²)  — better when k ≈ n
            k-aware   : TC O(n²k),  SC O(n²k) — better when k << n (early pruning)
        """
        if k >= len(s) - 1:
            return True

        memo = {}

        def can_palindrome(i: int, j: int, deletions_left: int) -> bool:
            # base case: single char or crossed pointers → already a palindrome
            if i >= j:
                return True

            if (i, j, deletions_left) in memo:
                return memo[(i, j, deletions_left)]

            # match: move inward without consuming deletions_left
            if s[i] == s[j]:
                result = can_palindrome(i + 1, j - 1, deletions_left)

            else:
                # mismatch: deletions_left==0 check here (not as standalone early return)
                # because matching chars must still proceed inward even when deletions_left==0.
                # e.g. s="aba", k=0 → 'a'=='a' → can_palindrome(1,1,0) → True
                #      s="ab",  k=0 → 'a'!='b', deletions_left==0 → False
                if deletions_left == 0:
                    memo[(i, j, deletions_left)] = False # not required, can skip
                    return False

                # try deleting left or right character
                result = can_palindrome(i + 1, j, deletions_left - 1) or \
                         can_palindrome(i, j - 1, deletions_left - 1)

            memo[(i, j, deletions_left)] = result
            return result

        return can_palindrome(0, len(s) - 1, k)


from functools import lru_cache

class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        """
        Return True if s can be made a palindrome by deleting at most k chars.
        K-aware approach: threads deletions_left through recursion for early pruning.

        TC: O(n² × k)
            - Unique states: (i, j, deletions_left) → O(n²) × O(k) = O(n²k)
            - Work per state: O(1)
            - Same (i,j) reachable with different deletions_left values via
              different deletion paths, so k is part of the state space.
            - Best case O(n²): small k, heavy early pruning via deletions_left == 0

        SC: O(n² × k)
            - lru_cache stores up to O(n²k) (i, j, deletions_left) entries
            - Recursion stack depth: O(n)
            - Total: O(n²k) + O(n) = O(n²k)

        Comparison with k-unaware min_deletions approach:
            k-unaware : TC O(n²),   SC O(n²)  — better when k ≈ n
            k-aware   : TC O(n²k),  SC O(n²k) — better when k << n (early pruning)
        """
        if k >= len(s) - 1:
            return True

        @lru_cache(maxsize=None)
        def can_palindrome(i: int, j: int, deletions_left: int) -> bool:
            # base case: single char or crossed pointers → already a palindrome
            if i >= j:
                return True

            # match: move inward without consuming deletions_left
            if s[i] == s[j]:
                return can_palindrome(i + 1, j - 1, deletions_left)

            # mismatch: k==0 check here (not as standalone early return) because
            # matching chars must still proceed inward even when deletions_left==0.
            # e.g. s="aba", k=0 → 'a'=='a' → can_palindrome(1,1,0) → True
            #      s="ab",  k=0 → 'a'!='b', deletions_left==0 → False
            if deletions_left == 0:
                return False

            # try deleting left or right character
            return can_palindrome(i + 1, j, deletions_left - 1) or \
                   can_palindrome(i, j - 1, deletions_left - 1)

        return can_palindrome(0, len(s) - 1, k)


# Approach : Top-Down DP (2D)

class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        """
        Return True if s can be made a palindrome by deleting at most k chars.
        
        2D DP bottom-up approach: Build table iteratively from smaller subproblems.
        
        Approach:
            dp[i][j] = minimum deletions needed to make s[i..j] a palindrome
            Uses CLOSED interval notation [i, j] — both endpoints inclusive.
            Conversion to Python slice: s[i..j] ←→ s[i : j+1]
            
            Base cases:
            - dp[i][i] = 0: closed interval [i,i] = single char s[i] → already palindrome
            - i > j    = 0: closed interval crossed → empty substring → already palindrome
            
            Recurrence:
            - If s[i] == s[j]: dp[i][j] = dp[i+1][j-1]
              Rationale: Matching chars already satisfy palindrome property.
                         Keep both (no deletion). Problem reduces to inner substring.
            
            - If s[i] != s[j]: dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])
              Rationale: Chars don't match, must delete one.
                         Try both options, take minimum, add 1 for deletion.
            
            Answer: dp[0][n-1] <= k
        
        Time Complexity: O(n²) where n = len(s)
            - Total cells: n(n+1)/2 = O(n²) — upper triangle where i <= j
            - Work per cell: O(1) — compare chars, lookup dp values, store result
            - Total: O(n²) × O(1) = O(n²)
            - k doesn't affect state space — only used in final comparison dp[0][n-1] <= k
        
        Space Complexity: O(n²)
            - DP table: n × n = O(n²)
            - No recursion stack (iterative)
        
        Comparison with Other Approaches:
            Top-Down (Recursion + Memo): Time O(n²), Space O(n²) + O(n) stack
            2D DP (This solution):       Time O(n²), Space O(n²)
            1D DP (Space optimized):     Time O(n²), Space O(n)
        """
        n = len(s)

        # early return: if k >= n-1, we can delete all but one char
        # leaving a single char (or empty string) which is always a palindrome
        # covers:
        #   n=0: k >= -1 → always True (empty string)
        #   n=1: k >= 0  → always True (single char)
        #   large k: k >= n-1 → can reduce to single char
        if k >= n - 1:
            return True

        # dp[i][j] = minimum deletions to make s[i..j] a palindrome
        # closed interval [i,j]: dp[i][j] ←→ s[i : j+1] in Python
        #   dp[0][0] → s[0..0] = "a"    ←→  s[0:1]  (Python needs j+1)
        #   dp[0][1] → s[0..1] = "ab"   ←→  s[0:2]
        #   dp[0][3] → s[0..3] = "abcd" ←→  s[0:4]
        #
        # Initialize with 0s — base cases automatically handled:
        #   diagonal (i==j): single char [i,i] → 0 deletions ✓
        #   lower triangle (i>j): empty interval → 0 deletions ✓
        #
        # Table structure (n=4, s="abcd"):
        #       j=0  j=1  j=2  j=3
        #     ┌─────────────────────
        # i=0 │  0    ?    ?    ?     ← upper triangle: we compute these
        # i=1 │  0    0    ?    ?     ← diagonal: [i,i] = single char
        # i=2 │  0    0    0    ?     ← lower triangle: unused (stays 0)
        # i=3 │  0    0    0    0
        dp = [[0] * n for _ in range(n)]

        # Fill by increasing substring length (length = j - i + 1 from closed interval)
        #
        # WHY THIS ORDER?
        # dp[i][j] depends on dp[i+1][j-1], dp[i+1][j], dp[i][j-1] — all shorter.
        # So we fill from shortest (length 2) to longest (length n).
        #
        # Fill order (n=4):
        #   length 2: [0,1] [1,2] [2,3]   → use length-1 results
        #   length 3: [0,2] [1,3]         → use length 1 & 2 results
        #   length 4: [0,3]               → use length 2 & 3 results
        for length in range(2, n + 1):
            # i range: 0 to n-length
            # ensures j = i + length - 1 <= n-1 (derived from closed interval: j = i + length - 1)
            #
            # Example: n=4, length=3, s="abcd"
            #   i=0 → j = 0+3-1 = 2 → closed interval [0,2] = "abc"  ←→ s[0:3]
            #   i=1 → j = 1+3-1 = 3 → closed interval [1,3] = "bcd"  ←→ s[1:4]
            for i in range(n - length + 1):
                # j derived from closed interval formula: length = j - i + 1 → j = i + length - 1
                j = i + length - 1

                if s[i] == s[j]:
                    # match: inner substring [i+1, j-1], no deletion needed
                    # empty inner (i+1 > j-1): hits lower triangle → 0 ✓
                    dp[i][j] = dp[i + 1][j - 1]
                else:
                    # mismatch: delete s[i] → solve [i+1, j]
                    #           delete s[j] → solve [i, j-1]
                    #           add 1 for the deletion made
                    dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j - 1])

        # dp[0][n-1] = minimum deletions for entire string s[0..n-1]
        return dp[0][n - 1] <= k

# Dry run Example 

# s = "abca", k = 1

# indices: 0 1 2 3
# chars:   a b c a

# n = 4

# Question: Can we make "abca" a palindrome with at most 1 deletion?

# ### DP Table Structure

# dp[i][j] = minimum deletions to make s[i..j] a palindrome

#       j=0  j=1  j=2  j=3
#        a    b    c    a
#     ┌────────────────────
# i=0│a│  ?    ?    ?    ?
# i=1│b│       ?    ?    ?
# i=2│c│            ?    ?
# i=3│a│                 ?


# ### Initial State (Base Cases)

# Diagonal = 0 (single characters are palindromes)

#       j=0  j=1  j=2  j=3
#        a    b    c    a
#     ┌────────────────────
# i=0│a│  0    ?    ?    ?    ← s[0..0] = "a"
# i=1│b│       0    ?    ?    ← s[1..1] = "b"
# i=2│c│            0    ?    ← s[2..2] = "c"
# i=3│a│                 0    ← s[3..3] = "a"

# ### Fill Order: Length = 2

# Process all 2-character substrings:

# #### Cell (0,1): s[0..1] = "ab"

# i=0, j=1
# s[0]='a' vs s[1]='b'
# 'a' != 'b' ✗ Mismatch!

# Options:
# - Delete 'a': dp[1][1] = 0 → need 1 deletion total
# - Delete 'b': dp[0][0] = 0 → need 1 deletion total

# dp[0][1] = 1 + min(0, 0) = 1

# #### Cell (1,2): s[1..2] = "bc"
# i=1, j=2
# s[1]='b' vs s[2]='c'
# 'b' != 'c' ✗ Mismatch!

# Options:
# - Delete 'b': dp[2][2] = 0 → need 1 deletion total
# - Delete 'c': dp[1][1] = 0 → need 1 deletion total

# dp[1][2] = 1 + min(0, 0) = 1

# #### Cell (2,3): s[2..3] = "ca"

# i=2, j=3
# s[2]='c' vs s[3]='a'
# 'c' != 'a' ✗ Mismatch!

# Options:
# - Delete 'c': dp[3][3] = 0 → need 1 deletion total
# - Delete 'a': dp[2][2] = 0 → need 1 deletion total

# dp[2][3] = 1 + min(0, 0) = 1

# **Table after Length 2:**
#       j=0  j=1  j=2  j=3
#        a    b    c    a
#     ┌────────────────────
# i=0│a│  0    1    ?    ?    ← s[0..1] = "ab" needs 1 deletion
# i=1│b│       0    1    ?    ← s[1..2] = "bc" needs 1 deletion
# i=2│c│            0    1    ← s[2..3] = "ca" needs 1 deletion
# i=3│a│                 0

# ### Fill Order: Length = 3

# Process all 3-character substrings:

# #### Cell (0,2): s[0..2] = "abc"
# i=0, j=2
# s[0]='a' vs s[2]='c'
# 'a' != 'c' ✗ Mismatch!

# Options:
# - Delete 'a': dp[1][2] = 1 → need 1+1 = 2 deletions total
# - Delete 'c': dp[0][1] = 1 → need 1+1 = 2 deletions total

# dp[0][2] = 1 + min(1, 1) = 2

# #### Cell (1,3): s[1..3] = "bca"

# i=1, j=3
# s[1]='b' vs s[3]='a'
# 'b' != 'a' ✗ Mismatch!

# Options:
# - Delete 'b': dp[2][3] = 1 → need 1+1 = 2 deletions total
# - Delete 'a': dp[1][2] = 1 → need 1+1 = 2 deletions total

# dp[1][3] = 1 + min(1, 1) = 2

# **Table after Length 3:**
#       j=0  j=1  j=2  j=3
#        a    b    c    a
#     ┌────────────────────
# i=0│a│  0    1    2    ?    ← s[0..2] = "abc" needs 2 deletions
# i=1│b│       0    1    2    ← s[1..3] = "bca" needs 2 deletions
# i=2│c│            0    1
# i=3│a│                 0

# ### Fill Order: Length = 4

# Process the full string:

# #### Cell (0,3): s[0..3] = "abca"
# ```
# i=0, j=3
# s[0]='a' vs s[3]='a'
# 'a' == 'a' ✓ MATCH!

# Matching chars satisfy palindrome property!
# Keep both (no deletion needed)
# Problem reduces to inner substring s[1..2] = "bc"

# dp[0][3] = dp[1][2] = 1

# **Final Table:**

#       j=0  j=1  j=2  j=3
#        a    b    c    a
#     ┌────────────────────────────────
# i=0│a│  0    1    2    1    ← s[0..3] = "abca" needs 1 deletion ✓
# i=1│b│       0    1    2
# i=2│c│            0    1
# i=3│a│                 0

# ### Answer

# min_deletions_needed = dp[0][3] = 1
# k = 1

# Check: 1 <= 1 → True ✓

# Result: YES, we can make "abca" a palindrome with 1 deletion!

# How? Delete 'b' → "aca" (palindrome)
#   OR Delete 'c' → "aba" (palindrome)

# Approach : Bottom-Up DP (1D) (complicated)

class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        """
        Determine if a string can become a palindrome by removing at most k characters.
        
        Approach:
        ---------
        1. Find the Longest Palindromic Subsequence (LPS) of the string
        2. Calculate how many characters need to be removed: removals = len(s) - LPS
        3. Check if removals <= k
        
        Example:
        --------
        s = "abcdeca", k = 2
        - LPS = "acdca" (length 5) or "abdba" (length 5)
        - Removals needed = 7 - 5 = 2
        - Since 2 <= 2, return True
        
        Time Complexity:  O(n²) where n = len(s)
        -----------------
        - Outer loop runs n times (i from n-1 to 0)
        - Inner loop runs on average n/2 times per outer iteration
        - Total operations: O(n²)
        
        Space Complexity: O(n) where n = len(s)
        ------------------
        - We use a single dp array of size n
        - Plus a few constant variables (diagonal, temp)
        - This is space-optimized from O(n²) 2D table
        """
        n = len(s)

        # early return: if k >= n-1, we can delete all but one char
        # leaving a single char (or empty string) which is always a palindrome
        # covers:
        #   n=0: k >= -1 → always True (empty string)
        #   n=1: k >= 0  → always True (single char)
        #   large k: k >= n-1 → can reduce to single char
        if k >= n - 1:
            return True
        
        # dp[j] stores the length of longest palindromic subsequence
        # for substring s[i...j] as we iterate through different values of i
        dp = [0] * n
        
        # Process each starting position from right to left
        # We go backwards because we need values from positions to the right
        for i in range(n - 1, -1, -1):
            
            # Set the current position to 1 (single character)
            dp[i] = 1
            
            # diagonal represents dp[i+1][j-1] (LPS of middle substring between i and j)
            #
            # WHY dp[i+1][j-1] IS THE MIDDLE SUBSTRING:
            #   dp[i][j] = LPS of closed interval s[i..j]
            #   when s[i] == s[j], both outer chars match → include both (+2)
            #   and solve the middle part (everything between i and j):
            #
            #   s[i]  s[i+1] ... s[j-1]  s[j]
            #    ↑                         ↑
            #   outer                    outer  → matched, contribute +2
            #          ↑           ↑
            #          └───middle──┘           → dp[i+1][j-1]
            #
            #   dp[i][j]     = s[i..j]       = "abcde"  (full substring)
            #   dp[i+1][j-1] = s[i+1..j-1]  = "bcd"    (middle, both ends stripped)
            #   → dp[i][j] = dp[i+1][j-1] + 2
            #
            # WHY INITIALIZE TO 0:
            #   first use of diagonal is when j = i+1 (adjacent chars):
            #   middle = s[i+1..j-1] = s[i+1..i] → left > right → empty → LPS = 0
            #
            #   j = i+1 (adjacent):  s[i]  s[j]        no chars between → empty
            #   j = i+2 (one apart): s[i]  s[?]  s[j]  one char between → LPS = 1
            #
            # WHY NOT diagonal = 1?
            #   diagonal = 0 → dp[j] = 0 + 2 = 2 ✓  e.g. s="aa": LPS = 2
            #   diagonal = 1 → dp[j] = 1 + 2 = 3 ✗  impossible, string only has 2 chars
            diagonal = 0
            
            # Process all ending positions to the right of i
            # We're computing LPS for substring s[i...j]

            # why process all j to the right of i?
            #   i starts from n-1 and goes left → when i=n-1, range(i+1, n) = range(n, n)
            #   is empty (no iterations). as i decreases, j covers all positions to the right.
            #
            #   i=n-1: j=[]            → fills nothing, sets dp[n-1]=1
            #   i=n-2: j=[n-1]         → fills dp[n-2][n-1]
            #   i=n-3: j=[n-2, n-1]    → fills dp[n-3][n-2], dp[n-3][n-1]
            #   i=0:   j=[1, ..., n-1] → fills entire top row
            #
            # why j starts at i+1 (not i)?
            #   j=i   → substring s[i..i] = single char → already handled by dp[i]=1 above
            #   j=i+1 → substring s[i..i+1] = 2 chars  → first case needing recurrence
            #   starting at j=i would overwrite dp[i] with match/mismatch recurrence
            #   which is only valid for substrings of length >= 2
            #
            # dependency direction ensures correctness:
            #   to compute dp[i][j], we need:
            #     dp[i+1][j-1] ← row below, col to left  (diagonal)
            #     dp[i+1][j]   ← row below, same col     (temp)
            #     dp[i][j-1]   ← same row, col to left   (dp[j-1])
            #   all dependencies are in row i+1 or earlier
            #   → already computed since i goes right to left
            for j in range(i + 1, n):
                
                # Save the current dp[j] value before we overwrite it
                # We need this value because it becomes the diagonal
                # for the next iteration (when j moves one step right)
                temp = dp[j]
                
                # Check if characters at positions i and j match
                if s[i] == s[j]:
                    # MATCH: Both boundary characters are the SAME
                    # ============================================
                    # Example: substring "a...a" (both ends are 'a')
                    #
                    # We can include BOTH characters in our palindrome!
                    #
                    # The LPS of s[i...j] = LPS of middle part + 2
                    # The middle part s[i+1...j-1] has LPS stored in 'diagonal'
                    #
                    # Visual: "a" + [middle LPS] + "a"
                    #          ↑                   ↑
                    #         +1                  +1 = +2 total
                    #
                    # Why diagonal? It holds the value from s[i+1...j-1]
                    # which is one position down and one position left in 2D table
                    dp[j] = diagonal + 2
                    
                else:
                    # NO MATCH: Boundary characters are DIFFERENT
                    # ==========================================
                    # Example: substring "a...b" (different ends)
                    #
                    # We CANNOT include both boundaries in same palindrome
                    # We must choose to exclude one of them:
                    #
                    # Option 1: Exclude left character s[i]
                    #          → Take LPS from s[i+1...j]
                    #          → This value is stored in 'temp'
                    #          Visual: [skip 'a'] "...b"
                    #
                    # Option 2: Exclude right character s[j]
                    #          → Take LPS from s[i...j-1]
                    #          → This value is in dp[j-1]
                    #          Visual: "a..." [skip 'b']
                    #
                    # We take MAXIMUM because we want the longest palindrome
                    dp[j] = max(temp, dp[j - 1])
                
                # Update diagonal for the next iteration
                # When we move to j+1, the current dp[j] becomes the diagonal
                # This is because diagonal represents the value one step back
                # in both dimensions (one position left and one position down)
                diagonal = temp
        
        # After processing all positions, dp[n-1] contains the answer
        # This is the length of longest palindromic subsequence
        # for the entire string s[0...n-1]
        lps = dp[n - 1]
        
        # Calculate how many characters we must remove
        # Any character NOT part of the LPS must be removed
        removals = n - lps
        
        # Check if we can achieve palindrome with at most k removals
        return removals <= k

# Dry Run: s = "aba", k = 1

## Initial Setup

# s = "aba"
# k = 1
# n = 3

# Indices:  0   1   2
# String:   a   b   a

# Initial: dp = [0, 0, 0]

# ## Iteration i = 2 (Last character 'a')

# i = 2
# dp[2] = 1           # Single char 'a' is palindrome of length 1
# diagonal = 0        # Empty substring has LPS = 0

# Inner loop: range(3, 3) → No iterations (empty range)

# Result: dp = [0, 0, 1]

# **What dp means now:**
# - dp[2] = LPS of "a" = 1

# ## Iteration i = 1 (Middle character 'b')

# i = 1
# dp[1] = 1           # Single char 'b' is palindrome of length 1
# diagonal = 0        # Empty substring has LPS = 0

# Inner loop: range(2, 3) → j = 2

# ### j = 2: Substring "ba"

# temp = dp[2] = 1    # Save current dp[2]

# Compare: s[1] = 'b' vs s[2] = 'a'
# Match? NO ('b' != 'a')

# dp[2] = max(temp, dp[1])
#       = max(1, 1) 
#       = 1

# diagonal = temp = 1  # Update diagonal for next iteration

# Result: dp = [0, 1, 1]

# What dp means now:
# - dp[1] = LPS of "b" = 1
# - dp[2] = LPS of "ba" = 1 (either 'b' or 'a')

# ## Iteration i = 0 (First character 'a')

# i = 0
# dp[0] = 1           # Single char 'a' is palindrome of length 1
# diagonal = 0        # Empty substring has LPS = 0

# Inner loop: range(1, 3) → j = 1, 2

# ### j = 1: Substring "ab"

# temp = dp[1] = 1    # Save current dp[1]

# Compare: s[0] = 'a' vs s[1] = 'b'
# Match? NO ('a' != 'b')

# dp[1] = max(temp, dp[0])
#       = max(1, 1)
#       = 1

# diagonal = temp = 1  # Update diagonal for next iteration

# Current: dp = [1, 1, 1]

# What dp means now:
# - dp[0] = LPS of "a" = 1
# - dp[1] = LPS of "ab" = 1

# ### j = 2: Substring "aba" (Full string!)

# temp = dp[2] = 1    # Save current dp[2]

# Compare: s[0] = 'a' vs s[2] = 'a'
# Match? YES! ✓

# dp[2] = diagonal + 2
#       = 1 + 2
#       = 3

# Explanation:
#   "aba" → Both ends are 'a' (match!)
#   Middle is "b" (from position 1 to 1)
#   LPS of middle = diagonal = 1 (which came from temp in previous iteration)
#   So LPS of "aba" = 1 + 2 = 3
#   The palindrome is "aba" itself!

# diagonal = temp = 1  # Update diagonal (not needed anymore, loop ends)

# Result: dp = [1, 1, 3]
#                     ↑
#                  Answer!

# What dp means now:
# - dp[0] = LPS of "a" = 1
# - dp[1] = LPS of "ab" = 1  
# - dp[2] = LPS of "aba" = 3

# ## Final Calculation

# lps = dp[n - 1] = dp[2] = 3

# removals = n - lps 
#          = 3 - 3 
#          = 0

# return removals <= k
# Result: True




        