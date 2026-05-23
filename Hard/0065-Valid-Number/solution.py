"""
LeetCode 65. Valid Number
Difficulty: Hard
URL: https://leetcode.com/problems/valid-number/
"""

class Solution:
    def isNumber(self, s: str) -> bool:
        """
        Validate if a string represents a valid number (integer, decimal, or scientific notation).
        
        Valid number formats:
        - Integer: "2", "-3", "+1"
        - Decimal: "0.1", "-0.5", ".3", "3."
        - Scientific: "1e5", "1e-5", "6.02e23", "-1.5E-10"
        
        Algorithm:
        - Use three flags to track: digits seen, decimal point seen, exponent seen
        - Parse character by character and validate rules for each character type
        - Reset seen_digit after exponent to ensure digits exist in exponent part
        
        Time Complexity: O(n) where n is length of string
        - Single pass through all characters
        
        Space Complexity: O(1)
        - Only using three boolean flags regardless of input size
        
        Args:
            s: Input string to validate
            
        Returns:
            True if s represents a valid number, False otherwise
        """
        # ========== STEP 1: Initialize tracking flags ==========
        # These flags maintain state as we parse through the string
        
        seen_digit = False      # Tracks if we've encountered at least one digit (0-9)
                                # Must be True by the end for valid number
                                
        seen_dot = False        # Tracks if we've encountered a decimal point (.)
                                # Can only appear once in the entire number
                                
        seen_exponent = False   # Tracks if we've encountered exponent notation (e/E)
                                # Can only appear once in the entire number
        
        
        # ========== STEP 2: Parse each character ==========
        for i in range(len(s)):
            
            # -------------------- Case 1: Digit (0-9) --------------------
            # VALID: "123", "1.5", "1e5", ".5", "5.", "1e-5"
            # INVALID: N/A (digits are always valid)
            if s[i].isdigit():
                # Mark that we've seen at least one digit
                # This is crucial for final validation
                seen_digit = True
                
                
            # -------------------- Case 2: Sign (+/-) --------------------
            # VALID: "+5" (at start), "-3" (at start), "1e+5" (after e), "2E-10" (after E)
            # INVALID: "6+1" (middle), "3.+5" (after dot), "+-5" (consecutive), "1+e5" (before e)
            elif s[i] in ["+", "-"]: # elif s[i] == "+" or s[i] == "-"
                # Check if sign is in a valid position
                # Valid positions: start of string OR right after 'e'/'E'
                
                # Condition breakdown:
                # - i != 0: We're NOT at the start of string
                # - s[i-1] not in {"E", "e"}: Previous char is NOT an exponent
                if i != 0 and s[i - 1] not in ["E", "e"]:
                    # Sign is in invalid position
                    # Examples that fail here: "6+1", "3.+5", "+-5"
                    return False
                
                # If we reach here, sign is valid (either at start or after 'e')
                # Examples that pass: "+5" (i=0), "1e+5" (prev='e')
                # No need to set any flags - signs don't affect validity by themselves
                
                    
            # -------------------- Case 3: Decimal point (.) --------------------
            # VALID: "3.14" (standard), ".5" (no integer), "5." (no fraction), "0.1"
            # INVALID: "1.2.3" (multiple dots), "1e2.5" (dot in exponent), "." (no digits)
            elif s[i] == ".":
                # Check if decimal point is allowed at this position
                
                # Restriction 1: Can't have multiple decimal points
                # Example that fails: "1.2.3" (second dot would have seen_dot=True)
                
                # Restriction 2: Can't have decimal in exponent part
                # Example that fails: "1e2.5" (exponent must be integer)
                # When we see 'e', we set seen_exponent=True, so any dot after fails
                
                if seen_dot or seen_exponent:
                    # Either already have a dot OR we're in exponent part
                    return False
                
                # Mark that we've now seen a decimal point
                seen_dot = True
                
                # Note: We DON'T require digits before or after the dot
                # ".5" is valid (no integer part)
                # "5." is valid (no fractional part)
                
                
            # -------------------- Case 4: Exponent (e/E) --------------------
            # VALID: "1e5", "2E10", "3.5e-2", ".5e10", "1e+5"
            # INVALID: "e5" (no digit before), "1e2e3" (multiple exponents), "1e" (no digit after)
            elif s[i] in ["e", "E"]:
                # Check if exponent is allowed at this position
                
                # Restriction 1: Can't have multiple exponents
                # Example that fails: "1e2e3" (second 'e' would have seen_exponent=True)
                
                # Restriction 2: Must have at least one digit BEFORE exponent
                # Example that fails: "e5" (no digit before, seen_digit=False)
                # Example that passes: ".5e10" (dot doesn't count, but '5' does)
                
                if seen_exponent or not seen_digit:
                    # Either already have exponent OR no digit before it
                    return False
                
                # Mark that we've now seen an exponent
                seen_exponent = True
                
                # CRITICAL: Reset seen_digit to False
                # Why? To enforce that exponent part ALSO has digits
                # Example: "1e" should fail
                #   - Before 'e': seen_digit=True (from '1')
                #   - After 'e': seen_digit=False (reset here)
                #   - Final check: seen_digit=False → return False ✓
                # Example: "1e5" should pass
                #   - After 'e': seen_digit=False (reset here)
                #   - When we see '5': seen_digit=True (set in Case 1)
                #   - Final check: seen_digit=True → return True ✓
                seen_digit = False
                
                
            # -------------------- Case 5: Any other character --------------------
            # VALID: N/A (all other characters are invalid)
            # INVALID: "abc", "1a", "5 5", "2#3", "1_000"
            else:
                # Invalid characters include:
                # - Letters (except 'e'/'E'): "abc", "1a"
                # - Whitespace: "5 5"
                # - Special characters: "2#3", "1_000"
                # - Any other symbol
                return False
        
        
        # ========== STEP 3: Final validation ==========
        # Return True if we saw at least one digit, False otherwise
        # This catches edge cases like: ".", "+", "+.", "1e", "e5"
        return seen_digit
        

# Variant : No exponents e or E

# class Solution:
#     def isNumber(self, s: str) -> bool:
#         """
#         Validate if a string represents a valid number (integer or decimal) WITHOUT exponents.
        
#         Valid number formats:
#         - Integer: "2", "-3", "+1", "0089"
#         - Decimal: "0.1", "-0.5", ".3", "3."
        
#         NOT Valid (exponents not allowed):
#         - Scientific: "1e5", "1e-5", "6.02e23"
        
#         Algorithm:
#         - Use two flags to track: digits seen, decimal point seen
#         - Parse character by character and validate rules for each character type
#         - No exponent handling needed
        
#         Time Complexity: O(n) where n is length of string
#         - Single pass through all characters
        
#         Space Complexity: O(1)
#         - Only using two boolean flags regardless of input size
        
#         Args:
#             s: Input string to validate
            
#         Returns:
#             True if s represents a valid number (without exponent), False otherwise
#         """
#         # ========== STEP 1: Initialize tracking flags ==========
#         # These flags maintain state as we parse through the string
        
#         seen_digit = False      # Tracks if we've encountered at least one digit (0-9)
#                                 # Must be True by the end for valid number
                                
#         seen_dot = False        # Tracks if we've encountered a decimal point (.)
#                                 # Can only appear once in the entire number
        
        
#         # ========== STEP 2: Parse each character ==========
#         for i in range(len(s)):
            
#             # -------------------- Case 1: Digit (0-9) --------------------
#             # VALID: "123", "1.5", ".5", "5."
#             # INVALID: N/A (digits are always valid)
#             if s[i].isdigit():
#                 # Mark that we've seen at least one digit
#                 # This is crucial for final validation
#                 seen_digit = True
                
                
#             # -------------------- Case 2: Sign (+/-) --------------------
#             # VALID: "+5" (at start), "-3" (at start), "+3.14" (at start)
#             # INVALID: "6+1" (middle), "3.+5" (after dot), "+-5" (consecutive)
#             elif s[i] in {"+", "-"}:
#                 # Sign is ONLY valid at position 0 (start of string)
#                 # Since no exponents allowed, signs can't appear after 'e'
                
#                 if i != 0:
#                     # Sign is not at start, so it's invalid
#                     # Examples that fail: "6+1", "3.+5", "+-5"
#                     return False
                
#                 # If we reach here, sign is at start (valid)
#                 # Example: "+5", "-3.14"
#                 # No need to set any flags - signs don't affect validity by themselves
                
                    
#             # -------------------- Case 3: Decimal point (.) --------------------
#             # VALID: "3.14" (standard), ".5" (no integer), "5." (no fraction), "0.1"
#             # INVALID: "1.2.3" (multiple dots), "." (no digits)
#             elif s[i] == ".":
#                 # Check if decimal point is allowed at this position
                
#                 # Restriction: Can't have multiple decimal points
#                 # Example that fails: "1.2.3" (second dot would have seen_dot=True)
                
#                 if seen_dot:
#                     # Already have a dot, can't have another
#                     return False
                
#                 # Mark that we've now seen a decimal point
#                 seen_dot = True
                
#                 # Note: We DON'T require digits before or after the dot
#                 # ".5" is valid (no integer part)
#                 # "5." is valid (no fractional part)
                
                
#             # -------------------- Case 4: Any other character --------------------
#             # VALID: N/A (all other characters are invalid)
#             # INVALID: "abc", "1a", "5 5", "2#3", "1_000", "1e5" (exponent not allowed)
#             else:
#                 # Invalid characters include:
#                 # - Letters (including 'e'/'E'): "abc", "1a", "1e5"
#                 # - Whitespace: "5 5"
#                 # - Special characters: "2#3", "1_000"
#                 # - Any other symbol
#                 return False
        
        
#         # ========== STEP 3: Final validation ==========
#         # Return True if we saw at least one digit, False otherwise
#         # This catches edge cases like: ".", "+", "+.", "-"
#         return seen_digit