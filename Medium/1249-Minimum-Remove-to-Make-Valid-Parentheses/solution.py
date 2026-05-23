"""
LeetCode 1249. Minimum Remove to Make Valid Parentheses
Difficulty: Medium
URL: https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/
"""

# Brute Force Approach:

# In the brute-force approach, we generate all possible strings by removing any subset of parentheses, then check each one for validity using a balance counter to ensure the parentheses are properly matched. Among all valid strings, we select the longest one, which corresponds to the minimum number of removals needed. For example, for the input "a)b(c)d", the brute-force method would try all combinations like "a)b(c)d", "ab(c)d", "a)bc)d", etc., and identify "ab(c)d" as the longest valid string. This approach has O(n × 2ⁿ) time and O(n) space complexity.


# Check discord comments for other minor follow ups (what if the string is very long, etc)

# Approach : Two pass

class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        """ 
        Approach: Two-pass with counter
        - Pass 1 (L->R): Remove unmatched ')' and count unmatched '('
        - Pass 2 (R->L): Remove unmatched '(' based on count from pass 1
        
        Time Complexity: O(n)
            - Pass 1: O(n) to iterate through string
            - Pass 2: O(n) to iterate through first_pass
            - Reverse: O(n) to reverse result
            - Join: O(n) to create final string
            - Total: O(n) + O(n) + O(n) + O(n) = O(n)
        
        Space Complexity: O(n)
            - first_pass list: O(n) in worst case (all valid chars)
            - result list: O(n) in worst case
            - open_count: O(1)
            - Total: O(n)

        """

        # Edge case: empty string
        if not s:
            return ""
        
        # ========== PASS 1: Remove unmatched closing parentheses ==========
        # Going left-to-right, we can identify ')' that don't have matching '('
        
        first_pass = []  # Will store valid characters after removing unmatched ')'
        open_count = 0   # Tracks number of unmatched '(' seen so far
        
        for char in s:
            if char == '(':
                # Found opening parenthesis
                # Increment counter (this '(' needs a matching ')')
                open_count += 1
                first_pass.append(char)
                
            elif char == ')':
                # Found closing parenthesis
                # Check if there's an unmatched '(' to pair with
                if open_count > 0:
                    # Valid ')' - has a matching '(' before it
                    open_count -= 1  # Match this ')' with previous '('
                    first_pass.append(char)
                # else: Invalid ')' - no matching '(' found, so skip it; we can use continue but its redundant
                
            else:
                # Regular character (letter, digit, etc.)
                # Always keep non-parenthesis characters
                first_pass.append(char)
        
        # After pass 1:
        # - All unmatched ')' are removed
        # - open_count = number of unmatched '(' remaining
        # - first_pass contains: valid ')', all '(', and all letters

        # print(first_pass)
        # print(open_count)

        if open_count == 0:
            return ''.join(first_pass)
        
        # ========== PASS 2: Remove unmatched opening parentheses ==========
        # Going right-to-left, remove 'open_count' number of '('
        # WHY RIGHT-TO-LEFT instead of LEFT-TO-RIGHT?
        # 
        # Example: "(a(b(c)d)" 
        # After pass 1: first_pass = ['(', 'a', '(', 'b', '(', 'c', ')', 'd', ')']
        #               open_count = 1
        # 
        # R->L (CORRECT): Scan backwards, skip rightmost unmatched '('
        # → result before reverse = [')', 'd', ')', 'c', 'b', '(', 'a', '(']
        # → After reverse: "(a(bcd))" ✓
        # 
        # L->R (WRONG): Scan forwards, skip leftmost unmatched '('
        # → result before reverse = ['a', '(', 'b', '(', 'c', ')', 'd', ')']
        # → After reverse: ")d)c(b(a" ✗ COMPLETELY BROKEN
        # 
        # Key: We build result while scanning, then reverse at end. R->L naturally
        # gives us reversed valid string. L->R gives forward string that becomes
        # garbage after reversal.
        
        result = []  # Will store final valid characters
        
        # Iterate through first_pass in reverse order
        for i in range(len(first_pass)-1, -1, -1):
            char = first_pass[i]
            
            if char == '(' and open_count > 0:
                # This is an unmatched '(' that needs to be removed
                open_count -= 1  # Decrement count of '(' to remove
                # Don't append to result (effectively removing it)
                
            else:
                # Either:
                # 1. It's a ')' (always valid after pass 1)
                # 2. It's a '(' that has a matching ')' (open_count is 0)
                # 3. It's a regular character
                result.append(char)

        # print(result)
        
        # After pass 2:
        # - result contains all valid characters but in REVERSE order
        # - Need to reverse it back to get correct order
        
        
        # ========== REVERSE AND BUILD FINAL STRING ==========
        # Reverse the result list to restore original order
        # WHY DO WE NEED TO REVERSE?
        # 
        # Because we scanned R->L in pass 2, we built result in reverse order.
        # result = [')', 'd', ')', 'c', 'b', '(', 'a', '(']
        # 
        # If we DON'T reverse and just join:
        # ''.join(result) = ")d)cb(a(" ✗ INVALID - parentheses backwards!
        # 
        # After reversing:
        # result = ['(', 'a', '(', 'b', 'c', ')', 'd', ')']
        # ''.join(result) = "(a(bc)d)" ✓ VALID
        # 
        # The reversal is ESSENTIAL - it converts the backwards scan result
        # into the correct forward-reading string.

        l, r = 0, len(result) - 1

        while l < r:
            result[l], result[r] = result[r], result[l]
            l, r = l + 1, r - 1
        
        # # Join all characters into final string
        return ''.join(result)


# Approach : Shortened two pass

class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        """        
        Time Complexity: O(n) - two passes through string
        Space Complexity: O(n) - for intermediate and result lists
        
        Approach:
        - Pass 1 (L->R): Remove unmatched ')' and count all '('
        - Pass 2 (L->R): Keep only valid '(' (first 'keep' number of them)
        """
        
        # Edge case: empty string
        if not s:
            return ""

        # ========== PASS 1: Remove all invalid ')' ==========
        # Build a list with valid ')' and ALL '(' (both matched and unmatched)
        
        temp = []  # Temporary result after removing invalid ')'
        
        # extra_opens: Tracks number of unmatched '(' at current position
        # Acts as a "balance" counter:
        #   - Increases when we see '(' (one more waiting for ')')
        #   - Decreases when we see ')' (matched with a '(')
        #   - If 0 when we see ')', that ')' is invalid
        extra_opens = 0
        
        # total_opens: Total count of ALL '(' encountered in the string
        # We need this to calculate how many '(' are actually valid later
        total_opens = 0
        
        for char in s:
            
            if char == "(":
                # Found opening parenthesis
                total_opens += 1   # Increment total '(' counter
                extra_opens += 1   # One more unmatched '(' (waiting for ')')
                
            if char == ")":
                # Found closing parenthesis
                if extra_opens == 0:
                    # No unmatched '(' available to pair with
                    # This ')' is INVALID, skip it (don't add to temp)
                    continue
                # This ')' is VALID - has a matching '(' before it
                extra_opens -= 1  # Match this ')' with previous '('
            
            # Add character to temporary result
            # Includes: ALL '(', VALID ')', and ALL letters
            temp.append(char)
        
        # After Pass 1:
        # - temp contains: ALL '(' (valid + invalid), VALID ')', ALL letters
        # - extra_opens = number of '(' that are unmatched (invalid)
        # - total_opens = total number of '(' in temp
        
        
        # ========== PASS 2: Remove rightmost invalid '(' ==========
        # Strategy: Keep only the FIRST 'keep' number of '(' (left-to-right)
        # The remaining '(' at the end are the unmatched ones we need to remove
        
        result = []  # Final result list
        
        # keep: Number of '(' to KEEP (these are the valid ones)
        # Formula: valid '(' = total '(' - unmatched '('
        # In other words: keep = total_opens - extra_opens
        keep = total_opens - extra_opens
        
        # Iterate through temp and keep only first 'keep' opening parentheses
        for char in temp:
            
            if char == "(":
                # Found an opening parenthesis
                # Check if we've already kept enough valid '('
                
                if keep == 0:
                    # Already kept all valid '('
                    # This '(' is unmatched (invalid), skip it
                    continue
                
                # This '(' is valid, we should keep it
                keep -= 1  # Decrement counter (one less '(' to keep)
                # Character will be added to result below
            
            # Add character to final result
            # Includes: VALID '(', ALL ')', and ALL letters
            result.append(char)
        
        # Join list into final string and return
        return "".join(result)

# Example : s = ")())m(s)("      Output : "()m(s)"

# temp = ['(', ')', 'm', '(', 's', ')', '(']

# total_opens = 3  (we saw 3 opening parentheses total)
# extra_opens = 1  (1 opening parenthesis is unmatched)

# Characters removed in Pass 1:
#   - Index 0: ')' (no matching '(')
#   - Index 3: ')' (no matching '(')

# keep = total_opens - extra_opens
# keep = 3 - 1
# keep = 2

# Meaning: Keep the FIRST 2 opening parentheses
#          Skip the LAST 1 opening parenthesis

# Approach : Using stacks

class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        """
        Stack approach using list to mark characters for removal.
        
        Approach:
        - Convert string to list for easy in-place marking
        - Use stack to track indices of unmatched '('
        - Mark invalid characters as empty string ''
        - Join non-empty characters for final result
        
        Time Complexity: O(n)
            - Convert to list: O(n)
            - Single pass through string: O(n)
            - Mark unmatched '(' from stack: O(k) where k = unmatched '('
            - Join operation: O(n)
            - Total: O(n)
        
        Space Complexity: O(n)
            - chars list: O(n) (copy of input string)
            - stack: O(k) where k = number of '(' (worst case O(n))
            - Total: O(n)
        """
        
        # ========== STEP 1: Convert string to list ==========
        # Strings are immutable in Python, so we convert to list
        # This allows us to mark characters for removal by setting them to ''
        chars = list(s)
        
        # Stack stores INDICES of unmatched '('
        # When we find a ')', we pop from stack (matching found)
        # Remaining indices in stack at the end are unmatched '('
        stack = []
        
        
        # ========== STEP 2: Single pass - identify and mark invalid ')' ==========
        
        for i, char in enumerate(chars):
            
            if char == '(':
                # Found an opening parenthesis
                # Push its index onto stack (waiting for matching ')')
                stack.append(i)
                # Note: We don't mark it yet, as it might get matched later
                
            elif char == ')':
                # Found a closing parenthesis
                
                if stack:
                    # There's at least one unmatched '(' in the stack
                    # This ')' matches with the most recent '('
                    stack.pop()  # Remove the matched '(' index from stack
                    # Both '(' and ')' are valid, so we keep them (don't mark)
                    
                else:
                    # Stack is empty - no unmatched '(' available
                    # This ')' has no matching '(' before it
                    # Mark this index for removal by setting to empty string
                    chars[i] = ''
            
            # Regular characters (letters, digits, etc.)
            # Don't need to do anything - they stay as is
        
        
        # ========== STEP 3: Mark remaining unmatched '(' for removal ==========
        # After the loop, any indices still in stack are unmatched '('
        # These '(' don't have matching ')' after them
        
        while stack:
            # Pop each unmatched '(' index from stack
            idx = stack.pop()
            
            # Mark that position for removal by setting to empty string
            chars[idx] = ''
        
        # Now chars list has:
        # - Valid '(' and ')' unchanged
        # - Invalid '(' and ')' marked as ''
        # - All letters/regular characters unchanged
        
        
        # ========== STEP 4: Build result from non-empty characters ==========
        # Join all characters, empty strings '' will be skipped naturally
        return ''.join(chars)

# Variant : Do it in place (no additional space). String is given as a list.

class Solution:
    def minRemoveToMakeValid(self, s: list) -> str:
        """
        Strategy:
        - Pass 1 (L→R): Mark invalid ')' with '*', count all '('
        - Pass 2 (L→R): Mark invalid '(' with '*' using keep count
        - Pass 3: Filter out all '*' markers to build result
        
        Time Complexity: O(n)
            - Pass 1: O(n) to scan and mark invalid ')'
            - Pass 2: O(n) to scan and mark invalid '('
            - Pass 3: O(n) to filter and build result
            - Total: O(n)
        
        Space Complexity: O(1) auxiliary space
            - Only uses integer counters (extra_opens, total_opens, keep)
            - Modifies input array in-place by marking with '*'
            - Output string is O(n) but that's required return value

        Example:
        Input:  [')','(',')',')','m','(','s',')','(']
        Pass 1: ['*','(',')', '*','m','(','s',')','(']  # marked invalid ')'
        Pass 2: ['*','(',')', '*','m','(','s',')','*']  # marked invalid '('
        Output: "()m(s)"
        """
        
        n = len(s)
        
        # ========== PASS 1 (L→R): Mark invalid ')' and count '(' ==========
        # Purpose: Remove any ')' that doesn't have a matching '(' before it
        #          Also count all '(' for later calculation
        
        # extra_opens: Acts as a "balance" counter
        #   - Increases when we see '(' (one more waiting for ')')
        #   - Decreases when we see ')' (matched with a '(')
        #   - When 0 and we see ')', that ')' is invalid
        extra_opens = 0
        
        # total_opens: Total count of ALL '(' in the string
        #   - Needed to calculate how many '(' are valid in Pass 2
        #   - Formula: valid '(' = total '(' - unmatched '('
        total_opens = 0
        
        for i in range(n):
            char = s[i]
            
            if char == '(':
                total_opens += 1
                extra_opens += 1
                
            elif char == ')':
                if extra_opens > 0:
                    extra_opens -= 1
                else:
                    s[i] = '*'
        
        # After Pass 1 completes:
        # -------------------------
        # s now contains:
        #   - All valid ')' (unchanged)
        #   - All '(' - both valid and invalid (we'll handle in Pass 2)
        #   - All regular characters (unchanged)
        #   - Invalid ')' marked as '*'
        #
        # Variables state:
        #   - total_opens = total number of '(' in the array
        #   - extra_opens = number of '(' that are still unmatched
        #                 = number of invalid '(' that need removal
        
        
        # ========== PASS 2 (L→R): Mark invalid '(' going LEFT-TO-RIGHT ==========
        # Purpose: Remove '(' that don't have matching ')' after them
        
        # Calculate how many '(' are VALID (have matching ')')
        # Formula: valid '(' = total '(' - unmatched '('
        #
        # Example: If we have 3 total '(' and 1 is unmatched:
        #          valid = 3 - 1 = 2 (keep first 2, remove last 1)
        keep = total_opens - extra_opens
        
        for i in range(n):
            char = s[i]
            
            if char == '(':
                if keep > 0:
                    keep -= 1
                else:
                    s[i] = '*'
        
        # After Pass 2 completes:
        # -------------------------
        # s now contains:
        #   - All VALID parentheses (unchanged)
        #   - All regular characters (unchanged)
        #   - All INVALID parentheses marked as '*'
        #
        # Example: ['*','(',')', '*','m','(','s',')','*']
        #          Invalid chars marked with '*'
        
        
        # ========== PASS 3: Build result from non-marked chars ==========
        result = []
        for i in range(n):
            if s[i] != '*':
                result.append(s[i])

        # ========== PASS 3: Compact in-place (NO additional list!) ==========
        # Use two-pointer technique to overwrite '*' markers
        
        # j = 0  # Write pointer - position to write next valid character
        
        # # Read through entire array
        # for i in range(n):
        #     if s[i] != '*':
        #         # Valid character - write it at position j
        #         s[j] = s[i]
        #         j += 1
        #     # else: Skip '*' markers (don't write, don't increment j)

        # return ''.join(s[:j])

        return ''.join(result)

# Another approach using write pointer

class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        """
        Two-Pointer Compaction Approach (Space-Optimized)
        
        Key Idea: Use write pointer (j) to compact valid chars in-place
        - Read pointer: iterates through input (implicit in loop)
        - Write pointer (j): tracks where to write next valid char
        
        Approach:
        - Pass 1 (L→R): Compact by skipping invalid ')', count unmatched '('
        - Pass 2 (L→R): Compact by skipping invalid '(' using keep count
        
        Time Complexity: O(n) - two passes
        Space Complexity: O(n) in Python (list conversion), O(1) in C++
        """
        
        if not s:
            return ""
        
        # Convert to list for in-place modification (Python strings are immutable)
        s_list = list(s)
        
        # ========== PASS 1: Remove invalid closing parentheses ==========
        # Goal: Skip ')' that don't have matching '(' before them
        #       Keep all '(' (we'll handle unmatched ones in Pass 2)
        #       Keep all other characters
        
        j = 0  # Write pointer - position where we write next valid character
               # Read pointer is implicit (the loop variable)
               # Invariant: j <= read position (write never ahead of read)
        
        extra_opens = 0  # Balance counter: unmatched '(' so far
                         # Increases when we see '('
                         # Decreases when we see valid ')'
                         # When 0, any ')' is invalid
        
        total_opens = 0  # Total count of all '(' characters
                         # Needed for Pass 2 calculation
        
        # Iterate through each character (read pointer)
        for ch in s_list:
            
            if ch == '(':
                # Opening parenthesis - always write it for now
                # (We'll determine if it's valid in Pass 2)
                total_opens += 1      # Count total '(' for later
                extra_opens += 1      # One more unmatched '(' waiting for ')'
                s_list[j] = ch        # Write to position j
                j += 1                # Move write pointer forward
                
            elif ch == ')':
                # Closing parenthesis - check if it has a matching '('
                if extra_opens == 0:
                    # Invalid ')' - no unmatched '(' before it
                    # Skip this character (don't write it, don't increment j)
                    # This effectively removes the invalid ')'
                    continue
                
                # Valid ')' - has a matching '(' before it
                extra_opens -= 1   # Match this ')' with a previous '('
                s_list[j] = ch     # Write to position j
                j += 1             # Move write pointer forward
                
            else:
                # Regular character (letter, digit, space, etc.)
                # Always keep these characters
                s_list[j] = ch  # Write to position j
                j += 1          # Move write pointer forward
        
        # After Pass 1:
        # ──────────────────────────────────────────────────────────
        # s_list[0:j] contains compacted result with:
        #   - All '(' (both matched and unmatched)
        #   - Only valid ')' (that had matching '(' before them)
        #   - All regular characters
        # 
        # Variables state:
        #   - j = length of compacted array
        #   - extra_opens = number of unmatched '(' (need to remove these)
        #   - total_opens = total number of '(' in compacted array
        
        length = j  # Save compacted length from Pass 1
        
        
        # ========== PASS 2: Remove invalid opening parentheses ==========
        # Goal: Remove '(' that don't have matching ')' after them
        #       Keep all ')' (they're all valid from Pass 1)
        #       Keep all other characters
        
        # Calculate how many '(' to keep (the valid ones)
        # Formula: valid '(' = total '(' - unmatched '('
        # Example: If we have 5 total '(' and 2 are unmatched
        #          We keep first 3, skip last 2
        keep = total_opens - extra_opens
        
        j = 0  # Reset write pointer for second compaction
               # We'll only process s_list[0:length] from Pass 1
        
        # Process the compacted array from Pass 1
        for i in range(length):
            ch = s_list[i]
            
            if ch == '(':
                # Opening parenthesis - check if we should keep it
                if keep == 0:
                    # We've already kept enough '(' (all valid ones)
                    # This is an unmatched '(' - skip it
                    # Don't write, don't increment j
                    continue
                
                # This is a '(' we want to keep (has matching ')' after it)
                s_list[j] = ch  # Write to position j
                j += 1          # Move write pointer forward
                keep -= 1       # Decrement count of '(' still to keep
                
            else:
                # Either ')' or regular character
                # All ')' are valid from Pass 1 - always keep
                # All regular characters - always keep
                s_list[j] = ch  # Write to position j
                j += 1          # Move write pointer forward
        
        # After Pass 2:
        # ──────────────────────────────────────────────────────────
        # s_list[0:j] contains final result with:
        #   - Only valid, matched '(' and ')'
        #   - All regular characters
        #
        # j = final length of valid string
        
        # Build and return final string from compacted array
        return ''.join(s_list[:j])

# Another approach : Pass 2 is from right to left

class Solution:
    def minRemoveToMakeValid(self, s: list) -> str:
        """
        Remove minimum parentheses using marking with R→L Pass 2.
        
        Time: O(n)
        Space: O(1) auxiliary
        """
        # Convert to list for in-place modification
        s = list(s)
        
        n = len(s)

        # Pass 1 (L→R): Mark invalid ')'
        open_count = 0
        for i in range(n):
            if s[i] == '(':
                open_count += 1
            elif s[i] == ')':
                if open_count > 0:
                    open_count -= 1
                else:
                    s[i] = '*'  # Mark invalid ')'
        
        # Pass 2 (R→L): Mark invalid '(' from right
        invalid_open = open_count
        for i in range(n - 1, -1, -1):
            if s[i] == '(' and invalid_open > 0:
                s[i] = '*'  # Mark invalid '('
                invalid_open -= 1
        
        # Build result (filter '*')
        return ''.join(c for c in s if c != '*')



# Variant : Multiple parentheses

# Given a string that consists of various types of parentheses ((), [], {}) and 
# alphanumeric characters, delete the least number of parentheses (any of them) 
# to make the string balanced and return any result.

# A balanced string is defined as a string where every type of opening parentheses 
# has a matching closing parentheses.

# IMPORTANT: Each bracket type is balanced INDEPENDENTLY (not requiring proper nesting)
           
#            This means we count each type (), [], {} separately. Each type only 
#            needs equal opening and closing brackets. We DON'T check if brackets 
#            are properly nested or follow LIFO order.
           
#            Example: "([)]" is VALID (each type has 1 opening + 1 closing)
#            But with proper nesting: "([)]" would be INVALID (brackets cross)

# CLARIFICATION: This is NOT the "properly nested parentheses" problem
# ───────────────────────────────────────────────────────────────────────────────

# This problem does NOT follow the formal definition:
#     A parentheses string is valid if and only if:
#    * It is the empty string, or
#    * It can be written as AB (A concatenated with B), or
#    * It can be written as (A), where A is a valid string."

# That definition requires PROPER NESTING (LIFO order using a stack).

# This problem uses INDEPENDENT BALANCING (counting each type separately).

# Algorithm Difference:
#   Proper Nesting: Uses STACK to enforce LIFO order
#     - Closing bracket must match TOP of stack
#     - Rejects crossings like "([)]"
  
#   Independent Balancing: Uses COUNTERS per bracket type
#     - Each type tracked separately: {'(': count, '[': count, '{': count}
#     - Allows crossings like "([)]"

# This Problem Uses: INDEPENDENT BALANCING (counters, no stack needed)

# Examples:
# ─────────
# Input:  "([)]"        → Output: "([)]"  (both types balanced independently)
# Input:  "lee(t(c)o)de)" → Output: "lee(t(c)o)de"
# Input:  "([{"         → Output: ""  (no closing brackets)
# Input:  "{a[b(c]d)e}" → Output: "{a[b(c]d)e}" (all types balanced)

# def delete_least_parentheses(s):
#     """
#     Remove minimum parentheses to make each bracket type independently balanced.
    
#     Independent Balancing: Each bracket type (), [], {} is counted separately.
#     We don't check nesting order - only that each type has equal opening/closing.
    
#     Time Complexity: O(n)
#         - Pass 1: O(n) to iterate through string once
#         - Calculate keep: O(1) to iterate through at most 3 bracket types
#         - Pass 2: O(n) to iterate through temp array once
#         - Join: O(n) to build final string
#         - Total: O(n) + O(1) + O(n) + O(n) = O(n)
    
#     Space Complexity: O(n)
#         - extra_opens: O(1) - at most 3 bracket types
#         - total_opens: O(1) - at most 3 bracket types
#         - temp: O(n) - worst case stores all characters
#         - keep: O(1) - at most 3 bracket types
#         - result: O(n) - worst case stores all characters
#         - Total: O(n) dominated by temp and result arrays
        
#         Note: Dictionaries are O(1) because they store at most 3 keys each,
#               which is constant regardless of input size.
#     """
    
#     # ========== INITIALIZATION ==========
    
#     # Mapping from closing bracket to its corresponding opening bracket
#     # Used to identify which opening bracket type a closing bracket needs
#     # Example: ')' needs '(', ']' needs '[', '}' needs '{'
#     mapping = {
#         ')': '(',
#         ']': '[',
#         '}': '{'
#     }
    
#     # Dictionary to track UNMATCHED opening brackets for each type
#     # Key: opening bracket character ('(', '[', or '{')
#     # Value: count of unmatched opening brackets
#     # Example: extra_opens = {'(': 2, '[': 1} means 2 unmatched '(' and 1 unmatched '['
#     #
#     # WITH defaultdict:
#     # ─────────────────────────────────────────────────────────────
#     # from collections import defaultdict
#     # extra_opens = defaultdict(int)  # Auto-initializes to 0
#     # Then use: extra_opens[ch] += 1  (no .get() needed)
#     #           extra_opens[ch] -= 1
#     #           if extra_opens[open_char] == 0:  (instead of .get())
#     extra_opens = {}
    
#     # Dictionary to track TOTAL opening brackets for each type
#     # Key: opening bracket character ('(', '[', or '{')
#     # Value: total count of that bracket type seen
#     # Used to calculate how many opening brackets to keep in Pass 2
#     #
#     # WITH defaultdict:
#     # ─────────────────────────────────────────────────────────────
#     # total_opens = defaultdict(int)  # Auto-initializes to 0
#     # Then use: total_opens[ch] += 1  (no .get() needed)
#     total_opens = {}
    
#     # Temporary list to store result after Pass 1
#     # Contains: all opening brackets, valid closing brackets, all other characters
#     # Missing: invalid closing brackets (skipped in Pass 1)
#     temp = []
    
    
#     # ========== PASS 1: Remove Invalid Closing Brackets ==========
#     # Goal: Skip closing brackets that don't have matching opening brackets
#     #       of the SAME TYPE before them
    
#     for ch in s:
        
#         # ──────────────────────────────────────────────────────────
#         # CASE 1: Opening Bracket ('(', '[', or '{')
#         # ──────────────────────────────────────────────────────────
#         # CHECK OPENING BRACKETS FIRST (more common in code)
#         #
#         # CRITICAL CHECK: Verify character is actually an opening bracket
#         # 
#         # Why this check is important:
#         # ───────────────────────────────────────────────────────────
#         # WITHOUT this check (using 'else' instead):
#         #   Input: "a@b(c)d"
#         #   Problem: '@' is not in mapping, would fall to else
#         #   Result: '@' treated as opening bracket
#         #   total_opens = {'@': 1, '(': 1}  ← WRONG! '@' is not a bracket
#         #   extra_opens = {'@': 1, '(': 0}  ← Wastes memory
#         #   keep = {'@': 0, '(': 1}         ← Unnecessary tracking
#         #
#         # WITH this check (ch in mapping.values()):
#         #   Input: "a@b(c)d"
#         #   '@' is not in mapping.values() → goes to else (Case 3)
#         #   Result: '@' treated as regular character ✓
#         #   total_opens = {'(': 1}          ← CORRECT! Only actual brackets
#         #   extra_opens = {'(': 0}          ← Clean
#         #   keep = {'(': 1}                 ← Only tracks real brackets
#         #
#         # Impact of missing this check:
#         #   - Semantic incorrectness: Non-brackets tracked as brackets
#         #   - Wasted memory: Dictionaries grow with non-bracket chars
#         #   - Potential bugs: If special chars are processed later
#         #   - Harder debugging: Confusing state in dictionaries
#         #
#         # mapping.values() returns: dict_values(['(', '[', '{'])
#         # This explicitly validates the character is an opening bracket
#         #
#         # Alternative if input ONLY contains brackets + alphanumeric:
#         # ───────────────────────────────────────────────────────────
#         # If we're GUARANTEED the string only has brackets and alphanumeric
#         # characters (no special chars like @, #, !, etc.), we could simplify:
#         #
#         #   if ch in mapping.values():
#         #       # handle opening bracket
#         #   elif ch in mapping:
#         #       # handle closing bracket
#         #   else:
#         #       # SAFE to assume it's alphanumeric
#         #       # (because no other characters possible)
#         #       temp.append(ch)
#         #
#         # This works ONLY if the problem guarantees input format.
#         # Current approach with 'ch in mapping.values()' is SAFER
#         # because it works for ANY input (including special characters).
#         # ───────────────────────────────────────────────────────────
        
#         if ch in mapping.values():
#             # This is an opening bracket
#             # Verified explicitly using mapping.values()
            
#             # Opening bracket - always add to temp for now
#             # We'll determine if it's matched or not in Pass 2
            
#             # Increment count of unmatched opening brackets for this type
#             # This bracket is waiting for a matching closing bracket
#             #
#             # WITH defaultdict: extra_opens[ch] += 1
#             extra_opens[ch] = extra_opens.get(ch, 0) + 1
            
#             # Increment total count for this bracket type
#             # Used in Pass 2 to calculate: keep = total - unmatched
#             #
#             # WITH defaultdict: total_opens[ch] += 1
#             total_opens[ch] = total_opens.get(ch, 0) + 1
            
#             # Add to temp array
#             temp.append(ch)
        
#         # ──────────────────────────────────────────────────────────
#         # CASE 2: Closing Bracket ('), ']', or '}')
#         # ──────────────────────────────────────────────────────────
#         elif ch in mapping:
#             # This is a closing bracket
#             # Get the corresponding opening bracket for this closing bracket
#             # Example: if ch = ')', then open_char = '('
#             open_char = mapping[ch]
            
#             # Check if there's an unmatched opening bracket of the SAME TYPE
#             # .get(open_char, 0) returns count if exists, 0 if not in dictionary
#             #
#             # WITH defaultdict: if extra_opens[open_char] == 0:
#             # (defaultdict returns 0 for missing keys automatically)
#             if extra_opens.get(open_char, 0) == 0:
#                 # No matching opening bracket available for this closing bracket
#                 # This closing bracket is INVALID - skip it (don't add to temp)
#                 # Continue to next character without appending
#                 continue
            
#             # Valid closing bracket - has a matching opening bracket before it
#             # Decrement the count of unmatched opening brackets of this type
#             # (We just matched one of them with this closing bracket)
#             #
#             # WITH defaultdict: extra_opens[open_char] -= 1
#             extra_opens[open_char] = extra_opens.get(open_char, 0) - 1
            
#             # Add this valid closing bracket to temp
#             temp.append(ch)
        
#         # ──────────────────────────────────────────────────────────
#         # CASE 3: Other Characters (alphanumeric, special chars)
#         # ──────────────────────────────────────────────────────────
#         else:
#             # Not a bracket - could be:
#             #   - Alphanumeric: 'a', 'b', '1', '2'
#             #   - Special characters: '@', '#', '!', ' ', '.', etc.
#             # Always keep these characters
#             temp.append(ch)
    
#     # After Pass 1:
#     # ─────────────────────────────────────────────────────────────
#     # temp[] contains:
#     #   - All opening brackets (both matched and unmatched)
#     #   - Only VALID closing brackets (those with matching opening)
#     #   - All non-bracket characters
#     #
#     # extra_opens{} contains:
#     #   - Count of UNMATCHED opening brackets for each type
#     #   - These need to be removed in Pass 2
#     #
#     # total_opens{} contains:
#     #   - Total count of opening brackets for each type
    
    
#     # ========== CALCULATE How Many Opening Brackets to Keep ==========
#     # For each bracket type, calculate: valid = total - unmatched
#     # This tells us how many opening brackets to KEEP in Pass 2
#     #
#     # Example: If we have 3 total '(' and 1 is unmatched:
#     #          keep['('] = 3 - 1 = 2
#     #          Meaning: keep first 2 occurrences of '(', skip the 3rd
    
#     # WITH defaultdict:
#     # ─────────────────────────────────────────────────────────────
#     # keep = defaultdict(int)  # Auto-initializes to 0
#     # for open_char in total_opens:
#     #     keep[open_char] = total_opens[open_char] - extra_opens[open_char]
#     # (No .get() needed since defaultdict handles missing keys)
#     keep = {}
#     for open_char, _ in total_opens.items():
#         # Calculate how many opening brackets of this type to keep
#         # Formula: keep = total - unmatched
#         keep[open_char] = total_opens[open_char] - extra_opens.get(open_char, 0)
    
    
#     # ========== PASS 2: Remove Unmatched Opening Brackets ==========
#     # Goal: Remove opening brackets that don't have matching closing brackets
#     #       Keep only the calculated number of each opening bracket type
#     #
#     # Strategy: Keep the FIRST N occurrences of each opening bracket type,
#     #           where N = keep[bracket_type]
#     #           This removes the LEFTMOST unmatched opening brackets
    
#     result = []  # Final result list
    
#     for ch in temp:
        
#         # ──────────────────────────────────────────────────────────
#         # CASE 1: Opening Bracket
#         # ──────────────────────────────────────────────────────────
#         if ch in total_opens:
#             # This is an opening bracket
#             # (If it's in total_opens dictionary, it's an opening bracket)
            
#             # Check if we should keep this opening bracket
#             #
#             # WITH defaultdict: if keep[ch] == 0:
#             if keep.get(ch, 0) == 0:
#                 # We've already kept all the opening brackets we need for this type
#                 # This is an UNMATCHED opening bracket - skip it
#                 # Don't add to result, just continue to next character
#                 continue
            
#             # This is a MATCHED opening bracket - keep it
#             # Decrement the keep count for this bracket type
#             #
#             # WITH defaultdict: keep[ch] -= 1
#             keep[ch] = keep.get(ch, 0) - 1
            
#             # Add to final result
#             result.append(ch)
        
#         # ──────────────────────────────────────────────────────────
#         # CASE 2: Closing Bracket or Other Character
#         # ──────────────────────────────────────────────────────────
#         else:
#             # Either:
#             #   - Closing bracket (all are valid from Pass 1)
#             #   - Non-bracket character (letter, digit, special char)
#             # Always keep these - add to result
#             result.append(ch)
    
#     # After Pass 2:
#     # ─────────────────────────────────────────────────────────────
#     # result[] contains:
#     #   - Only MATCHED opening brackets
#     #   - Only MATCHED closing brackets (from Pass 1)
#     #   - All non-bracket characters
#     #
#     # All bracket types are now independently balanced!
    
#     # Build final string from result list and return
#     return ''.join(result)

# Check the proper nesting solution too
        