"""
LeetCode 227. Basic Calculator II
Difficulty: Medium
URL: https://leetcode.com/problems/basic-calculator-ii/
"""

# Can see the solution from this video too https://www.youtube.com/watch?v=W3Rg4HVSZ9k

# Brute Force

# I would first parse the string into two arrays — one for numbers and one for operators.
# Then I process the expression in two passes:

# Resolve all * and / operations first by computing and updating the arrays.

# Finally, evaluate remaining + and - operations from left to right.

# Time Complexity: O(n²) (due to list deletions/shifting during evaluation)
# Space Complexity: O(n) (to store numbers and operators)


# Approach : Without stack (optimal solution)

class Solution:
    def calculate(self, s):
        """
        Calculate the result of a mathematical expression string.
        
        Time Complexity: O(n)
            - We iterate through the string exactly once
            - Each character is processed in constant time O(1)
            - n is the length of the input string
        
        Space Complexity: O(1)
            - We only use a fixed number of variables (curr_num, prev_num, result, op)
            - No additional data structures that grow with input size
            - This is an optimization over the O(n) stack-based approach
        
        Args:
            s: String containing non-negative integers and operators (+, -, *, /)
        
        Returns:
            Integer result of the expression
            
        Example:
            s = "10-3*2/2+5"
            
            This comprehensive example includes:
            - Multi-digit numbers: 10
            - Addition: +5
            - Subtraction: 10-3
            - Multiplication: 3*2
            - Division: 2/2
            - Operator precedence: * and / before + and -
            - Left-to-right evaluation: 3*2/2 = (3*2)/2 = 6/2 = 3
            
            Step-by-step evaluation:
            10 - 3*2/2 + 5
            = 10 - 6/2 + 5    (multiply first: 3*2=6)
            = 10 - 3 + 5      (divide next: 6/2=3)
            = 7 + 5           (subtract: 10-3=7)
            = 12              (add: 7+5=12)
            
            Execution trace:
            i=0,1: '10' → curr_num=10
            i=2, '-': op was '+' → result=0, prev_num=10, op='-'
            i=3: '3' → curr_num=3
            i=4, '*': op was '-' → result=10, prev_num=-3, op='*'
            i=5: '2' → curr_num=2
            i=6, '/': op was '*' → prev_num=-3*2=-6, op='/'
            i=7: '2' → curr_num=2
            i=8, '+': op was '/' → prev_num=-6/2=-3, op='+'
            i=9: '5' → curr_num=5
            END: op was '+' → result=7, prev_num=5
            Final: result + prev_num = 7 + 5 = 12 ✓
        """

        # Base case: empty string
        if not s:
            return 0

        # The number we're currently building from consecutive digits
        # Example: for "42", first curr_num=4, then curr_num=42
        curr_num = 0
        
        # The number that was processed but not yet added to result
        # This is like the "top of stack" - it might still be multiplied/divided
        # We keep it separate because the NEXT operator might be * or /
        # Example: in "3+2*4", when we see '*', prev_num=2 (will be multiplied)
        prev_num = 0
        
        # Running total of all numbers that are COMPLETELY DONE
        # We only add prev_num to result when we're SURE it won't be multiplied/divided
        # Example: in "3+2*4", result=3 after we see '*' (3 is safe, won't be affected)
        result = 0
        
        # The last operator we encountered (initialized to '+' to handle first number)
        # This is the operator we'll APPLY in the current iteration
        # Example: when we see '2' followed by '*', we use the PREVIOUS operator
        op = '+'
        
        # Iterate through every character in the string
        for i in range(len(s)):
            # If current character is a digit, build the multi-digit number
            # We multiply by 10 and add the new digit to handle numbers like "42"
            # Example: "42" → curr_num = 0*10+4 = 4, then curr_num = 4*10+2 = 42
            if s[i].isdigit():
                curr_num = curr_num * 10 + int(s[i])
            
            # Process when we hit an operator OR reach the end of string
            # Check (not digit AND not space) to identify operators
            # Alternative: s[i] in '+-*/' or i == len(s) - 1
            #
            # WHY CHECK END OF STRING (i == len(s) - 1)?
            # Without it, the LAST NUMBER would never be processed!
            # Example: "3+5" → we'd process 3, but never process 5
            # The last character might be a digit, so we force processing at the end
            if (not s[i].isdigit() and s[i] != ' ') or i == len(s) - 1:
                
                # KEY INSIGHT: We apply the PREVIOUS operator (not current)
                # We're processing the number (curr_num) that came BEFORE this operator
                # Using the operator (op) from the PREVIOUS iteration
                #
                # Example timeline for "3+2*4":
                # - See '3' then '+': apply op='+' to curr_num=3
                # - See '2' then '*': apply op='+' to curr_num=2  
                # - See '4' then END: apply op='*' to curr_num=4
                
                if op == '+':
                    # WHY ADD prev_num NOT curr_num?
                    # Because prev_num is "safe" - we know it won't be multiplied/divided
                    # curr_num is NOT safe yet - the next operator might be * or /
                    # 
                    # Example: "3+2*4" at the '*' operator:
                    # - result += prev_num (add 3, it's safe now)
                    # - prev_num = curr_num (store 2, might be multiplied next)
                    result += prev_num
                    prev_num = curr_num
                
                elif op == '-':
                    # Same logic as '+', but store curr_num as NEGATIVE
                    # We negate it now so that multiplication/division work correctly
                    # Example: "5-2*3" → store -2, then -2*3 = -6 (correct!)
                    result += prev_num
                    prev_num = curr_num * -1
                
                elif op == '*':
                    # HIGH PRECEDENCE: Apply multiplication IMMEDIATELY to prev_num
                    # Don't add to result yet - might be more * or / coming
                    # 
                    # Example: "3+2*4" when we see END:
                    # - prev_num = 2, curr_num = 4
                    # - prev_num = 2 * 4 = 8 (update in place)
                    # - Later we'll add this 8 to result
                    prev_num = prev_num * curr_num
                
                elif op == '/':
                    # HIGH PRECEDENCE: Apply division IMMEDIATELY to prev_num
                    # 
                    # CRITICAL: Use int(/) not // 
                    # - int(/) truncates toward zero: int(7/-2) = int(-3.5) = -3
                    # - // is floor division toward -∞: 7//-2 = -4 (WRONG for LeetCode)
                    # LeetCode expects C/Java behavior (truncate toward zero)
                    prev_num = int(prev_num / curr_num)
                
                # Reset curr_num for the next number we'll parse
                # We've processed it, so start building the next number from scratch
                curr_num = 0
                
                # Update operator to the current character for NEXT iteration
                # This operator will be applied when we process the NEXT number
                # Example: "3+2" → when at '+', we store op='+' to use for '2'
                op = s[i]
        
        # Add the last prev_num to result (handles the final number)
        # 
        # WHY IS prev_num NOT ADDED YET?
        # Because when we processed the last number/operator, we updated prev_num
        # but never added it to result (no more operators to trigger addition)
        # 
        # Example: "3+2*4" at end:
        # - result = 3 (from the '+' operation)
        # - prev_num = 8 (from 2*4)
        # - We need this final addition: 3 + 8 = 11
        result += prev_num
        
        return result


# Approach : Using stack

# class Solution:
#     def calculate(self, s):
#         """
#         Calculate the result of a mathematical expression string using a stack.
        
#         Time Complexity: O(n)
#             - We iterate through the string exactly once
#             - Each character is processed in constant time O(1)
#             - n is the length of the input string
        
#         Space Complexity: O(n)
#             - Stack can grow up to n/2 elements in worst case
#             - Example: "1+2+3+4+5" creates stack [1, 2, 3, 4, 5]
#             - This is less space-efficient than the O(1) approach but more intuitive
        
#         Args:
#             s: String containing non-negative integers and operators (+, -, *, /)
        
#         Returns:
#             Integer result of the expression
            
#         Example:
#             s = "10-3*2/2+5"
            
#             This comprehensive example includes:
#             - Multi-digit numbers: 10
#             - Addition: +5
#             - Subtraction: 10-3
#             - Multiplication: 3*2
#             - Division: 2/2
#             - Operator precedence: * and / before + and -
#             - Left-to-right evaluation: 3*2/2 = (3*2)/2 = 6/2 = 3
            
#             Step-by-step evaluation:
#             10 - 3*2/2 + 5
#             = 10 - 6/2 + 5    (multiply first: 3*2=6)
#             = 10 - 3 + 5      (divide next: 6/2=3)
#             = 7 + 5           (subtract: 10-3=7)
#             = 12              (add: 7+5=12)
            
#             Stack trace:
#             i=0,1: '10' → num=10
#             i=2, '-': op was '+' → stack=[10], op='-'
#             i=3: '3' → num=3
#             i=4, '*': op was '-' → stack=[10, -3], op='*'
#             i=5: '2' → num=2
#             i=6, '/': op was '*' → stack=[10, -6] (pop -3, push -3*2=-6), op='/'
#             i=7: '2' → num=2
#             i=8, '+': op was '/' → stack=[10, -3] (pop -6, push -6/2=-3), op='+'
#             i=9: '5' → num=5
#             END: op was '+' → stack=[10, -3, 5]
#             Final: sum(stack) = 10 + (-3) + 5 = 12 ✓
#         """
#         # Edge case: empty string
#         if not s:
#             return 0
        
#         # Stack to store numbers
#         # HOW THE STACK WORKS:
#         # - For + and -: Push numbers directly (negative for subtraction)
#         # - For * and /: Pop last number, compute, push result back
#         # - This naturally handles operator precedence without extra logic
#         # - At the end, sum all numbers in stack for final result
#         # Example: "3+2*4" → [3] → [3,2] → [3,8] → sum=11
#         stack = []
        
#         # The number we're currently building from consecutive digits
#         # Example: for "42", first num=4, then num=42
#         num = 0
        
#         # The last operator we encountered (initialized to '+' to handle first number)
#         # This is the operator we'll APPLY when we finish building the current number
#         # Example: when we see '2' followed by '*', we use the PREVIOUS operator
#         operation = '+'
        
#         # Iterate through every character in the string
#         for i in range(len(s)):
#             # If current character is a digit, build the multi-digit number
#             # We multiply by 10 and add the new digit to handle numbers like "42"
#             # Example: "42" → num = 0*10+4 = 4, then num = 4*10+2 = 42
#             if s[i].isdigit():
#                 num = num * 10 + int(s[i])
            
#             # Process when we hit an operator OR reach the end of string
#             # Check (not digit AND not space) to identify operators
#             # Alternative: s[i] in '+-*/' or i == len(s) - 1
#             #
#             # WHY CHECK END OF STRING (i == len(s) - 1)?
#             # Without it, the LAST NUMBER would never be processed!
#             # Example: "3+5" → we'd process 3, but never process 5
#             # The last character might be a digit, so we force processing at the end
#             if (not s[i].isdigit() and s[i] != ' ') or i == len(s) - 1:
                
#                 # KEY INSIGHT: We apply the PREVIOUS operator (not current)
#                 # We're processing the number (num) that came BEFORE this operator
#                 # Using the operator (operation) from the PREVIOUS iteration
#                 #
#                 # Example timeline for "3+2*4":
#                 # - See '3' then '+': apply operation='+' to num=3
#                 # - See '2' then '*': apply operation='+' to num=2  
#                 # - See '4' then END: apply operation='*' to num=4
                
#                 if operation == '+':
#                     # For addition: simply push the number onto the stack
#                     # We'll sum everything at the end
#                     # WHY NOT ADD TO RESULT NOW?
#                     # Because the NEXT operator might be * or /, which has higher precedence
#                     # Example: "3+2*4" → push 3, push 2, then multiply 2*4 later
#                     stack.append(num)
                
#                 elif operation == '-':
#                     # For subtraction: push the NEGATIVE number
#                     # This way, we can just sum the stack at the end
#                     # We negate NOW so multiplication/division work correctly later
#                     # Example: "5-2*3" → push -2, then -2*3=-6 (correct!)
#                     stack.append(-num)
                
#                 elif operation == '*':
#                     # HIGH PRECEDENCE: Apply multiplication IMMEDIATELY
#                     # Pop the last number from stack, multiply with current number, push back
#                     # This handles operator precedence (multiply before add/subtract)
#                     # 
#                     # Example: "3+2*4" when we see END:
#                     # - stack = [3, 2], num = 4
#                     # - pop 2, compute 2*4=8, push 8
#                     # - stack = [3, 8]
#                     # - Later sum: 3 + 8 = 11
#                     stack.append(stack.pop() * num)
                
#                 elif operation == '/':
#                     # HIGH PRECEDENCE: Apply division IMMEDIATELY
#                     # Pop the last number from stack, divide by current number, push back
#                     # 
#                     # CRITICAL: Use int(/) not //
#                     # - int(/) truncates toward zero: int(7/-2) = int(-3.5) = -3
#                     # - // is floor division toward -∞: 7//-2 = -4 (WRONG for LeetCode)
#                     # LeetCode expects C/Java behavior (truncate toward zero)
#                     stack.append(int(stack.pop() / num))
                
#                 # Reset num for the next number we'll parse
#                 # We've processed it, so start building the next number from scratch
#                 num = 0
                
#                 # Update operator to the current character for NEXT iteration
#                 # This operator will be applied when we process the NEXT number
#                 # Example: "3+2" → when at '+', we store operation='+' to use for '2'
#                 operation = s[i]
        
#         # Sum all numbers in the stack to get final result
#         # WHY SUM THE STACK?
#         # All operator precedence has been handled during stack operations:
#         # - + and - created separate stack entries
#         # - * and / were applied immediately (pop, compute, push)
#         # Now we just add everything together
#         # 
#         # Example: "3+2*4" at end:
#         # - stack = [3, 8] (3 was pushed for +, 8 is result of 2*4)
#         # - sum(stack) = 3 + 8 = 11
#         return sum(stack)


        