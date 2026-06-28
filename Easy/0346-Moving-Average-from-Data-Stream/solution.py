"""
LeetCode 346. Moving Average from Data Stream
Difficulty: Easy
URL: https://leetcode.com/problems/moving-average-from-data-stream/
"""

# Brute Force Approach : Recalculate the entire sum every time instead of reusing the previous sum

class MovingAverage:
    def __init__(self, size: int):
        """
        Time Complexity: O(1)
        Space Complexity: O(size) - store up to 'size' elements
        """
        self.size = size
        self.queue = deque()
    
    def next(self, val: int) -> float:
        """
        BRUTE FORCE: Recalculate sum every time
        
        Time Complexity: O(size) - sum() iterates through all window elements
        Space Complexity: O(1) - no additional space beyond the queue
        """
        self.queue.append(val)
        
        if len(self.queue) > self.size:
            self.queue.popleft()
        
        # Recalculate sum from scratch every time - O(size) operation
        # sum() works on deque - iterates through all elements
        return sum(self.queue) / len(self.queue)


# Optimized approach : Maintain a running sum and update it incrementally (add new element, subtract removed element)

class MovingAverage:
    def __init__(self, size: int):
        """
        Initialize the MovingAverage object with a fixed window size.
        
        Args:
            size: The maximum number of elements in the sliding window
        
        Time Complexity: O(1)
        Space Complexity: O(size) - for storing up to 'size' elements in the queue
        
        Edge Cases Handled:
        - size = 1: Window contains only the most recent element
        - Empty stream: Queue starts empty, builds up gradually
        
        Data Structures:
        1. self.size: Store the maximum window size
        2. self.queue: A deque (double-ended queue) to efficiently add/remove elements
        3. self.window_sum: Running sum of all elements currently in the window
        
        Why deque? It provides O(1) operations for both:
        - append() to add elements to the right
        - popleft() to remove elements from the left
        """
        # Base case: size must be at least 1
        if size < 1:
            raise ValueError("Window size must be at least 1") # raise not return
        
        self.size = size
        self.queue = deque()  # Stores the actual values in our sliding window
        self.window_sum = 0   # Maintains the sum of all elements in the queue
    
    def next(self, val: int) -> float:
        """
        Add a new value to the stream and return the moving average.
        
        Args:
            val: The new integer value to add to the stream
            
        Returns:
            The average of the last 'size' values (or fewer if we haven't seen 'size' values yet)
        
        Time Complexity: O(1) - all operations (append, popleft, arithmetic) are constant time
        Space Complexity: O(1) - no additional space used beyond the initialized queue
        
        Edge Cases Handled:
        - First element: Queue has only 1 element, returns that element
        - Fewer than 'size' elements: Returns average of all elements seen so far
        - Negative numbers: Handled correctly in sum calculation
        - Zero values: Handled correctly
        - Large numbers: May cause overflow in languages with fixed integer size
          (Python handles arbitrary precision integers automatically)
        
        Algorithm:
        1. Add the new value to the queue and update the running sum
        2. If the queue size exceeds our window size, remove the oldest element
        3. Calculate and return the average using the running sum
        """
        # Step 1: Add the new value to the right end of the queue
        self.queue.append(val)
        
        # Step 2: Update our running sum by adding the new value
        # This is more efficient than recalculating sum(self.queue) every time
        self.window_sum += val
        
        # Step 3: Check if our window has exceeded the maximum size
        if len(self.queue) > self.size:
            # Remove the oldest element (from the left) to maintain window size
            oldest_val = self.queue.popleft()
            
            # Subtract the removed value from our running sum
            # This keeps window_sum accurate without recalculating
            self.window_sum -= oldest_val
        
        # Step 4: Calculate the average
        # Divide the running sum by the current number of elements
        # Note: We use len(self.queue) not self.size because the queue
        # might have fewer elements than size (especially at the beginning)
        # 
        # IMPORTANT: We use / (single slash) for floating-point division
        # This returns decimals: 11 / 2 = 5.5 (not 5)
        # If we used // (double slash), we'd get integer division: 11 // 2 = 5
        # 
        # Edge case: len(self.queue) is guaranteed to be >= 1 since we just appended
        # so division by zero is not possible
        return self.window_sum / len(self.queue)

# Your MovingAverage object will be instantiated and called as such:
# obj = MovingAverage(size)
# param_1 = obj.next(val)

# Variant: Sliding Window Integer Average 

# Given a list of integers nums and an integer size, compute the integer average of elements in every contiguous subarray (sliding window) of length exactly size. 

# Return a list containing these averages, where each average is computed using integer division (//).

# Example 1:
# Input: nums = [5, 2, 8, 14, 3], size = 3
# Output: [5, 8, 8]

# Explanation:
# Window 1: (5 + 2 + 8) // 3 = 5  
# Window 2: (2 + 8 + 14) // 3 = 8  
# Window 3: (8 + 14 + 3) // 3 = 8

def compute_running_sum_variant(nums: List[int], size: int) -> List[int]:
    """
    Compute the average of elements in a sliding window using integer division.
    
    Args:
        nums: List of integers
        size: Size of the sliding window
        
    Returns:
        List of averages (using integer division) for each window position
        
    Time Complexity: O(n)
    Space Complexity: O(n-size+1) for result # remember this!
    
    Algorithm: Window ALWAYS contains EXACTLY 'size' elements when computing average
    - right >= size: Remove oldest element to maintain window size
    - right >= size-1: Record average (window has exactly 'size' elements)
    """
    # Validate inputs
    if size <= 0:
        raise ValueError("Window size must be positive.")
    if not nums or len(nums) < size:
        return []
    
    n = len(nums)
    result = []
    window_sum = 0

    # 'right' tracks the right boundary of our window (current position)
    # As we iterate, we've added elements from index 0 to right
    # Total elements added so far = right + 1
    for right in range(n):
        # STEP 1: Add new element to window
        window_sum += nums[right]
        # Now we have (right + 1) elements in the window
        
        # STEP 2: Maintain window at EXACTLY 'size' elements
        # ------------------------------------------------
        # WHY right >= size?
        # We want to check: "Do we have MORE than 'size' elements?"
        # Elements in window = right + 1
        # Condition: (right + 1) > size
        # Simplify: right >= size
        #
        # Example with size=3:
        #   right=0: 0+1=1 elements, 0>=3? NO, keep all
        #   right=1: 1+1=2 elements, 1>=3? NO, keep all
        #   right=2: 2+1=3 elements, 2>=3? NO, keep all (exactly size!)
        #   right=3: 3+1=4 elements, 3>=3? YES! Too many, remove oldest
        #   right=4: 4+1=5 elements, 4>=3? YES! Too many, remove oldest
        #
        # When right >= size is TRUE:
        # - We have (right+1) elements which is > size
        # - Remove the oldest element at index (right - size)
        # - After removal: window has exactly 'size' elements
        # - Window spans indices [right-size+1, right]
        if right >= size:
            window_sum -= nums[right - size]
            # Example: size=3, right=3
            #   Before: elements [0,1,2,3] = 4 elements
            #   Remove: nums[3-3] = nums[0]
            #   After: elements [1,2,3] = 3 elements ✓
        
        # STEP 3: Record average when window has exactly 'size' elements
        # --------------------------------------------------------------
        # WHY right >= size - 1?
        # We want to check: "Do we have AT LEAST 'size' elements?"
        # This triggers when we form our FIRST complete window and EVERY subsequent window
        #
        # Elements in window = right + 1 (after any removal above)
        # Condition: (right + 1) >= size
        # Simplify: right >= size - 1
        #
        # Example with size=3:
        #   right=0: 0>=2? NO  (only 1 element, incomplete)
        #   right=1: 1>=2? NO  (only 2 elements, incomplete)
        #   right=2: 2>=2? YES! (3 elements, FIRST complete window) ✓
        #   right=3: 3>=2? YES! (3 elements after removal, complete) ✓
        #   right=4: 4>=2? YES! (3 elements after removal, complete) ✓
        #
        # CRITICAL: Why >= and not ==?
        # ----------------------------------------
        # If we used right == size - 1:
        #   right=2: 2==2? YES → Records first window [0,1,2] ✓
        #   right=3: 3==2? NO  → SKIPS second window [1,2,3] ❌
        #   right=4: 4==2? NO  → SKIPS third window [2,3,4] ❌
        #   Result: Only records FIRST window, misses all others!
        #
        # With right >= size - 1:
        #   right=2: 2>=2? YES → Records first window ✓
        #   right=3: 3>=2? YES → Records second window ✓
        #   right=4: 4>=2? YES → Records third window ✓
        #   Result: Records ALL windows as required!
        #
        # At this point, window ALWAYS has EXACTLY 'size' elements because:
        # - Case 1 (right == size-1): We just reached 'size' elements
        # - Case 2 (right >= size): We removed excess, back to 'size' elements
        if right >= size - 1:
            # Use integer division (//) not float division (/)
            # Example: 11 // 2 = 5 (not 5.5)
            result.append(window_sum // size)

    return result
