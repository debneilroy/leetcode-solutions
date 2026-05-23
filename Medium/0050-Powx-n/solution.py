"""
LeetCode 50. Pow(x, n)
Difficulty: Medium
URL: https://leetcode.com/problems/powx-n/
"""

# Naive Approach

# class Solution:
# def myPow(x: float, n: int) -> float:
#         """
#         Naive approach: multiply x by itself n times
        
#         TC: O(n) - we do n-1 multiplications
#         SC: O(1) - only use one variable
#         """
#         if n < 0:
#             x = 1 / x
#             n = -n
        
#         result = 1.0
#         for i in range(n):
#             result *= x  # Multiply x exactly n times
        
#         return result


# Recursive Solution

class Solution:
    def myPow(self, x: float, n: int) -> float:
        """
        Calculate x raised to the power n using fast exponentiation (recursive).
    
        TIME COMPLEXITY: O(log n)
        ─────────────────────────────
        • We divide n by 2 in each recursive call: n → n/2 → n/4 → ... → 1 → 0
        • Question: How many divisions by 2 until we reach 0?
        • Answer: log₂(n) divisions
        
        Mathematical proof:
        After k divisions: n/2^k ≈ 0
        We need: 2^k ≥ n
        Taking log₂: k ≥ log₂(n)
        Therefore: k = ⌈log₂(n)⌉ + 1 (including base case)
        
        Work per call:
        • Constant operations: if checks, n//2, n%2, multiplications
        • Each call does O(1) work
        
        Total time = (number of calls) × (work per call)
                = O(log n) × O(1)
                = O(log n)
        
        Concrete examples:
        n=8:   8→4→2→1→0     (5 calls, log₂(8)=3)
        n=10:  10→5→2→1→0    (5 calls, log₂(10)≈3.32)
        n=16:  16→8→4→2→1→0  (6 calls, log₂(16)=4)
        n=100: ~7 calls       (log₂(100)≈6.64)
        n=1000: ~10 calls     (log₂(1000)≈9.97)
        
        Pattern: Doubling n only adds ONE more call!
        
        SPACE COMPLEXITY: O(log n)
        ──────────────────────────────
        • Space is used by the recursion call stack
        • Each recursive call creates a stack frame that holds:
            - Parameters: x, n
            - Local variables: half
            - Return address
        • Maximum stack depth = deepest level of recursion = log₂(n) + 1
        
        Stack frame visualization for n=10:
        Frame 5: myPow(2, 0)  ← base case (top of stack)
        Frame 4: myPow(2, 1)
        Frame 3: myPow(2, 2)
        Frame 2: myPow(2, 5)
        Frame 1: myPow(2, 10) ← initial call (bottom of stack)
        
        Space per frame: O(1) - constant variables
        Total space = (number of frames) × (space per frame)
                    = O(log n) × O(1)
                    = O(log n)
        
        Why not O(1)? Because all frames exist simultaneously on the stack
        until the base case returns and unwinding begins.
        """
        
        # Base case
        if n == 0:
            return 1.0
        
        # Handle negative exponent: x^(-n) = 1/(x^n)
        if n < 0:
            return 1 / myPow(x, -n)
        
        # Recursive case: divide problem size by 2 each time
        # Why halve? To compute x^n, we first compute x^(n/2), then square it
        # Example breakdown for x^10:
        #   x^10 = (x^5)^2, so we solve smaller problem x^5 first
        #   x^5 = x * (x^2)^2, so we solve x^2 first  
        #   x^2 = (x^1)^2, so we solve x^1 first
        #   x^1 = x * (x^0)^2, so we solve x^0 first
        #   x^0 = 1 (base case)
        # Then we return back up: x^0=1 → x^1=x → x^2=x² → x^5=x⁵ → x^10=x¹⁰
        # For concrete example with x=2: 1 → 2 → 4 → 32 → 1024
        # This breaks n → n//2 → n//4 → ... until n=0
        # For n=10: 10 → 5 → 2 → 1 → 0 (only 4 recursive calls!)
        half = myPow(x, n // 2)  # This is where n gets halved
        
        if n % 2 == 0:
            # Even: x^n = (x^(n/2))^2
            # Example: x^10 = (x^5)^2 = half^2
            return half * half
        else:
            # Odd: x^n = x * (x^(n/2))^2
            # Why? For odd n: x^n = x^(n-1) × x = x^(2×(n-1)/2) × x = (x^((n-1)/2))^2 × x
            # Since (n-1)/2 = n//2 for odd n, we get: x^n = x × (x^(n//2))^2
            # Example: x^5 = x × (x^2)^2 because 5 = 1 + 2×2, so x^5 = x^1 × x^4 = x × (x^2)^2
            # Example: x^7 = x × (x^3)^2 because 7 = 1 + 2×3, so x^7 = x^1 × x^6 = x × (x^3)^2
            return half * half * x

# Example : 2^6

# Recursive Calls (Going Down)
# Call 1: myPow(2, 6)

# n = 6 (even)
# Need to calculate: myPow(2, 3) first
# Will return: half * half

# Call 2: myPow(2, 3)

# n = 3 (odd)
# Need to calculate: myPow(2, 1) first
# Will return: half * half * 2

# Call 3: myPow(2, 1)

# n = 1 (odd)
# Need to calculate: myPow(2, 0) first
# Will return: half * half * 2

# Call 4: myPow(2, 0)

# n = 0 → BASE CASE
# Returns 1

# Unwinding (Coming Back Up)
# myPow(2, 0):

# Returns 1

# myPow(2, 1):

# half = 1
# n is odd → return 1 * 1 * 2 = 2
# Returns 2

# myPow(2, 3):

# half = 2
# n is odd → return 2 * 2 * 2 = 8
# Returns 8

# myPow(2, 6):

# half = 8
# n is even → return 8 * 8 = 64
# Returns 64 ✓

# Summary
# Call sequence: 6 → 3 → 1 → 0
# Return values: 1 → 2 → 8 → 64

# Breakdown:
# - 2^0 = 1
# - 2^1 = 1 * 1 * 2 = 2
# - 2^3 = 2 * 2 * 2 = 8
# - 2^6 = 8 * 8 = 64
# Only 4 recursive calls instead of 6 multiplications in the naive approach!


# Iterative solution using bit manipulation

class Solution:
    def myPow(self, x: float, n: int) -> float:
        """
        Calculate x raised to the power n using fast exponentiation (iterative).
    
        TIME COMPLEXITY: O(log n)
        ─────────────────────────────
        • Loop processes n bit by bit from right to left
        • Question: How many bits does n have in binary?
        • Answer: ⌊log₂(n)⌋ + 1 bits
        
        Why log₂(n) bits?
        Any number n can be represented with ⌊log₂(n)⌋ + 1 bits
        Examples:
            n=1:   1₂        (1 bit,  log₂(1)=0,   ⌊0⌋+1=1)
            n=2:   10₂       (2 bits, log₂(2)=1,   ⌊1⌋+1=2)
            n=7:   111₂      (3 bits, log₂(7)≈2.8, ⌊2.8⌋+1=3)
            n=8:   1000₂     (4 bits, log₂(8)=3,   ⌊3⌋+1=4)
            n=10:  1010₂     (4 bits, log₂(10)≈3.3, ⌊3.3⌋+1=4)
            n=100: 1100100₂  (7 bits, log₂(100)≈6.6, ⌊6.6⌋+1=7)
        
        Loop iterations:
        • Each iteration processes one bit
        • n //= 2 removes the rightmost bit
        • Loop continues until all bits processed (n becomes 0)
        • Number of iterations = number of bits = ⌊log₂(n)⌋ + 1
        
        Work per iteration:
        • n % 2: check bit (O(1))
        • result *= current_power: optional multiplication (O(1))
        • current_power *= current_power: squaring (O(1))
        • n //= 2: right shift (O(1))
        • Total: O(1) per iteration
        
        Total time = (number of iterations) × (work per iteration)
                = O(log n) × O(1)
                = O(log n)
        
        Concrete examples:
        n=5 (101₂):      3 iterations (process bits 1,0,1)
        n=10 (1010₂):    4 iterations (process bits 0,1,0,1)
        n=100 (1100100₂): 7 iterations (process all 7 bits)
        
        SPACE COMPLEXITY: O(1)
        ──────────────────────────────
        • Only uses a fixed number of variables:
            - result (float)
            - current_power (float)
            - n (int, modified in place)
            - x (float, may be modified for negative n)
        
        • No recursion = no call stack growth
        • No arrays or data structures that grow with n
        • Memory usage is CONSTANT regardless of n
        
        Space usage:
        n=10:      ~4 variables
        n=1000:    ~4 variables (same!)
        n=1000000: ~4 variables (same!)
        
        Total space = O(1) - constant space
    
        This is a key advantage over recursive approach!
        Recursive: O(log n) space due to stack frames
        Iterative: O(1) space, just a few variables

        This approach reduced 4 multiplications (recursive approach) to just 2 multiplications!
        """

        # STEP 1: Handle negative exponents
        # For negative n: x^(-n) = 1 / x^n
        # Example: 2^(-3) = 1/(2^3) = (1/2)^3 = (0.5)^3
        if n < 0:
            x = 1 / x  # Change base: 2 → 0.5
            n = -n     # Make exponent positive: -3 → 3
        
        # STEP 2: Initialize accumulator variables
        result = 1.0        # Accumulates final answer
        current_power = x   # Tracks x^1, x^2, x^4, x^8, ...

        # Note: No explicit base case needed!
        # If n=0: loop condition (n > 0) is False, loop never runs
        # We immediately return result=1.0, which is correct for x^0
        
        # ════════════════════════════════════════════════════════════════
        # COMPLETE EXAMPLE: Calculate 2^5
        # ════════════════════════════════════════════════════════════════
        # 
        # Goal: 2^5 = ?
        # 
        # Binary: 5 = 101₂ = 4 + 1 = 2² + 2⁰
        # So: 2^5 = 2^4 × 2^1 = 16 × 2 = 32
        # 
        # We'll process bits from RIGHT to LEFT: 1-0-1
        # 
        # ────────────────────────────────────────────────────────────────
        # ITERATION 1: Process rightmost bit (position 0)
        # ────────────────────────────────────────────────────────────────
        # Before: n=5 (101₂), result=1.0, current_power=2
        # 
        # Check bit: 5 % 2 = 1 (rightmost bit of 101₂ is 1)
        # Action: Bit is 1 → include this power
        #         result = 1.0 × 2 = 2.0
        #         (We collected 2^1 = 2)
        # 
        # Prepare next: 
        #   current_power = 2 × 2 = 4 (now represents 2^2)
        #   n = 5 // 2 = 2 (binary: 101₂ → 10₂)
        # 
        # After: n=2 (10₂), result=2.0, current_power=4
        # 
        # ────────────────────────────────────────────────────────────────
        # ITERATION 2: Process middle bit (position 1)
        # ────────────────────────────────────────────────────────────────
        # Before: n=2 (10₂), result=2.0, current_power=4
        # 
        # Check bit: 2 % 2 = 0 (rightmost bit of 10₂ is 0)
        # Action: Bit is 0 → skip this power
        #         result stays 2.0
        #         (We don't need 2^2 = 4)
        # 
        # Prepare next:
        #   current_power = 4 × 4 = 16 (now represents 2^4)
        #   n = 2 // 2 = 1 (binary: 10₂ → 1₂)
        # 
        # After: n=1 (1₂), result=2.0, current_power=16
        # 
        # ────────────────────────────────────────────────────────────────
        # ITERATION 3: Process leftmost bit (position 2)
        # ────────────────────────────────────────────────────────────────
        # Before: n=1 (1₂), result=2.0, current_power=16
        # 
        # Check bit: 1 % 2 = 1 (rightmost bit of 1₂ is 1)
        # Action: Bit is 1 → include this power
        #         result = 2.0 × 16 = 32.0
        #         (We collected 2^4 = 16)
        # 
        # Prepare next:
        #   current_power = 16 × 16 = 256 (not needed)
        #   n = 1 // 2 = 0 (binary: 1₂ → 0₂)
        # 
        # After: n=0, result=32.0
        # 
        # ────────────────────────────────────────────────────────────────
        # LOOP EXITS (n=0)
        # ────────────────────────────────────────────────────────────────
        # 
        # Final result: 32.0
        # 
        # What we collected:
        #   Iteration 1: 2^1 = 2   ✓ (bit was 1)
        #   Iteration 2: 2^2 = 4   ✗ (bit was 0, skipped)
        #   Iteration 3: 2^4 = 16  ✓ (bit was 1)
        # 
        # Calculation: 2 × 16 = 32 = 2^5 ✓
        # 
        # ════════════════════════════════════════════════════════════════
        
        while n > 0:  # Continue while there are bits to process
            
            # Check if rightmost bit is 1
            if n % 2 == 1:  # n % 2 gets the rightmost bit (1 or 0)
                # Bit is 1: include this power of 2 in our result
                result *= current_power
            # If bit is 0: skip (don't multiply)
            
            # Prepare for next bit:
            # 1. Square current_power to get next power of 2
            #    x^1 → x^2 → x^4 → x^8 → x^16 ...
            current_power *= current_power
            
            # 2. Remove rightmost bit (shift right)
            #    This moves us to the next bit position
            n //= 2  # Integer division by 2 (same as n >> 1)
        
        return result














