"""
LeetCode 528. Random Pick with Weight
Difficulty: Medium
URL: https://leetcode.com/problems/random-pick-with-weight/
"""

# Brute Force Approach

# Idea:
# Expand the array so each index i appears w[i] times, then pick randomly from it.
# Each position in the expanded list has an equal chance of being chosen, so the probability of picking index i becomes proportional to w[i] / Σw[i].

# Example:
# For w = [1, 3, 2] → [0, 1, 1, 1, 2, 2],
# randomly choosing an element gives the correct probabilities:
# P(0)=1/6, P(1)=3/6, P(2)=2/6.

# Trade-offs:
# ✅ Very easy to implement
# ❌ Extremely inefficient when weights are large — uses too much memory and preprocessing time.


class Solution:
    """
    BRUTE FORCE APPROACH - Expand weights into individual slots
    
    Approach:
    Create an expanded array where each index appears exactly weight[i] times.
    Then randomly pick one element from this expanded array.
    
    Example: w = [1, 3, 2]
    choices = [0, 1, 1, 1, 2, 2]
              ^  ^  ^  ^  ^  ^
            idx0  idx1 (3x)  idx2 (2x)
    
    Pros:
    - Simple and intuitive
    - O(1) pick time
    
    Cons:
    - Huge memory usage if weights are large
    - Slow initialization for large weights
    - Fails for w = [1, 1000000] (creates 1,000,001 slots!)
    """
    
    def __init__(self, w: List[int]):
        """
        Expand each index into individual slots based on its weight.
        
        Time Complexity: O(sum of weights)
        - Outer loop: O(n) iterations where n = len(w)
        - Inner loop for index i: O(w[i]) iterations
        - Total: O(w[0] + w[1] + ... + w[n-1]) = O(sum of all weights)
        - Example: w = [1, 3, 2] → O(1+3+2) = O(6)
        - Worst case: w = [10^5, 10^5, ..., 10^5] → O(n * 10^5)
        
        Space Complexity: O(sum of weights)
        - choices array stores sum of all weights elements
        - Each element is an integer (index)
        - Example: w = [1, 3, 2] → choices has 6 elements
        - Worst case: w = [10^5, 10^5] → 200,000 integers stored
        """
        self.choices = []  # Expanded array: O(sum) space
        
        for i, weight in enumerate(w):  # O(n) outer iterations
            # Append index i 'weight' times to create weighted slots
            for _ in range(weight):  # O(weight[i]) inner iterations
                self.choices.append(i)  # O(1) amortized per append

    def pickIndex(self) -> int:
        """
        Pick a random index from the expanded choices array.
        
        Time Complexity: O(1)
        - random.choice() picks one element uniformly in constant time
        - Internally uses random.randint(0, len-1) which is O(1)
        
        Space Complexity: O(1)
        - No additional space used
        - Only returns one integer

         # random.choice() - most Pythonic and efficient for random element selection
        # Alternatives: randint(0, len(self.choices)-1), randrange(len(self.choices)), but choice() is clearest
        """
        # Pick one random element uniformly from the expanded list
        # Each index appears proportional to its weight, giving correct probabilities
        return random.choice(self.choices)  # O(1)

# Approach : Prefix Sums + Binary Search

class Solution:
    """
    OPTIMIZED APPROACH - Prefix Sums + Binary Search
    
    Problem: Given weights, randomly pick indices proportional to their weights.
    
    Approach:
    Instead of creating an array with repeated indices (brute force), we use
    prefix sums to create cumulative weight ranges, then use binary search
    to efficiently find which range a random number falls into.
    
    Key Insight:
    - Map each index to a range proportional to its weight
    - Use prefix sums to define cumulative boundaries
    - Binary search to find which range contains our random target
    
    Example: w = [1, 3, 2]
    - prefix_sums = [1, 4, 6]
    - total = 6
    
    Number line mapping:
    0         1         2    3    4         5         6
    |---------|---------|----|----|---------|---------|
    [ Index 0 )[      Index 1      )[    Index 2      )
      [0, 1)          [1, 4)              [4, 6)
    
    When target = 2.5:
    - We find the first prefix_sum where target < prefix_sum
    - 2.5 < 1? NO
    - 2.5 < 4? YES → return index 1 ✓
    
    Probabilities:
    - Index 0: range [0, 1) → length 1 → prob 1/6
    - Index 1: range [1, 4) → length 3 → prob 3/6
    - Index 2: range [4, 6) → length 2 → prob 2/6
    
    Complexity:
    - Init: O(n) time, O(n) space
    - Pick: O(log n) time, O(1) space
    
    Advantages over Brute Force:
    ✅ Works with large weights (w = [1, 1000000] uses only 2 elements)
    ✅ Fast initialization O(n) vs O(sum of weights)
    ✅ Reasonable space O(n) vs O(sum of weights)
    ❌ Slightly slower pick O(log n) vs O(1), but negligible
    """

    def __init__(self, w: List[int]):
        """
        Initialize with weights array and build prefix sums.
        
        Args:
            w: List of positive integers representing weights
        
        Raises:
            ValueError: If w is empty or contains non-positive weights
        
        Time Complexity: O(n) where n = len(w)
        - Single pass through weights array to build prefix sums
        
        Space Complexity: O(n)
        - Store prefix_sums array of size n
        """
        # Edge case: empty weights array
        if not w:
            raise ValueError("Weights array cannot be empty")
        
        # Edge case: check for non-positive weights
        if any(weight <= 0 for weight in w):
            raise ValueError("All weights must be positive integers")
        
        self.prefix_sums = []  # Stores cumulative sums
        prefix_sum = 0
        
        # Build prefix sum array
        # Example: w = [1, 3, 2] → prefix_sums = [1, 4, 6]
        for weight in w:
            prefix_sum += weight
            self.prefix_sums.append(prefix_sum)
        
        self.total_sum = prefix_sum  # Total sum of all weights
        

    def pickIndex(self) -> int:
        """
        Pick a random index based on weights using binary search.
        
        Returns:
            int: Random index in range [0, len(weights)-1]
        
        How it works:
        1. Generate random target in [0, total_sum)
        2. Binary search to find smallest index i where target < prefix_sums[i]
        3. This gives us the index whose range contains the target
        
        Why "target < prefix_sum" (not <=)?
        - Each range is [prefix_sums[i-1], prefix_sums[i]) - left-inclusive, right-exclusive
        - We want the FIRST index where target hasn't exceeded the boundary yet
        - Example: target=1.0 with prefix_sums=[1,4,6]
          * 1.0 < 1? NO (boundary belongs to next range)
          * 1.0 < 4? YES → return index 1 ✓
        
        Example walkthrough with prefix_sums = [1, 4, 6]:
        - target = 0.5: First i where 0.5 < prefix_sums[i] → 0.5 < 1 → index 0
        - target = 1.0: First i where 1.0 < prefix_sums[i] → 1.0 < 4 → index 1
        - target = 2.5: First i where 2.5 < prefix_sums[i] → 2.5 < 4 → index 1
        - target = 5.0: First i where 5.0 < prefix_sums[i] → 5.0 < 6 → index 2
        
        Time Complexity: O(log n)
        - Binary search through prefix_sums array
        
        Space Complexity: O(1)
        - Only use constant extra space for variables
        """
        # Edge case: single element (should never happen if init validated, but defensive)
        if len(self.prefix_sums) == 1:
            return 0
        
        # Generate random target in range [0, total_sum)
        # random() * total_sum → continuous floats in [0, total_sum)
        #   Example: total_sum=6 → can generate 0.0, 0.5, 2.7, 5.999... (use prefix_sum > target)
        # Alternative 1: random.randint(1, total_sum) → discrete integers [1, total_sum]
        #   Example: total_sum=6 → can generate 1, 2, 3, 4, 5, 6 (use prefix_sum >= target)
        # Alternative 2: random.randint(0, total_sum - 1) → discrete integers [0, total_sum-1]
        #   Example: total_sum=6 → can generate 0, 1, 2, 3, 4, 5 (use prefix_sum > target)
        target = self.total_sum * random.random()
        
        # Alternative: Linear Search - O(n) time, simpler but slower
        # Find first index where target < prefix_sum
        # for i, prefix_sum in enumerate(self.prefix_sums):
        #     if target < prefix_sum:
        #         return i
        
        # Binary search: find smallest index i where target < prefix_sums[i]
        low, high = 0, len(self.prefix_sums) # Search range [low, high) - low inclusive, high exclusive
        
        while low < high:
            mid = low + (high - low) // 2 # Equivalent to (low + high) // 2, avoids overflow in other languages
            
            if target < self.prefix_sums[mid]:
                # Target is less than this boundary, could be our answer
                # But search left to find the smallest such index
                high = mid
            else:
                # target >= self.prefix_sums[mid]
                # Target has exceeded this boundary, search right
                low = mid + 1
        
        # Return low (same as high since low == high when loop exits)
        # low points to the smallest index where target < prefix_sums[low] (equivalently: target < prefix_sums[high])
        return low

# Overall Complexity for k calls:
# Time: O(n + k*log n) - O(n) init + O(k*log n) for k pickIndex calls
# Space: O(n) - prefix_sums array

# Your Solution object will be instantiated and called as such:
# obj = Solution(w)
# param_1 = obj.pickIndex()


# Variant : Random Pick with Weight - Return City Name

# You are conducting an A/B test and need to randomly pick a person from a user base spread across multiple cities. Each city has a known population, and you need to ensure that the probability of choosing a user from each city is proportional to the city's population. 

# You are given a 0-indexed array of pairs city_populations, where each pair consists of a string representing the name of the i-th city, and an integer representing the population of the i-th city (in millions, but treat these values as if in ones for computation purposes)

# You need to implement the function pickIndex(), which randomly picks a person and returns the name of the city the person is in.

# Example : 

# Input:
# ["Solution", "pickIndex", "pickIndex"]
# [[["Seattle", 500], ["New York", 900], ["Los Angeles", 400]], [], []]

# Output:
# [null, "New York", "Los Angeles"]

# Explanation:
# Solution solution = new Solution([["Seattle", 500], ["New York", 900], ["Los Angeles", 400]]);
# solution.pickIndex(); // returns "New York" with probability 900/(500+900+400)
# solution.pickIndex(); // returns "Los Angeles" with probability 400/(500+900+400)

# class Solution:
#     """
#     Random Pick with Weight - Return City Name Variant
    
#     Approach:
#     - Build prefix sums using populations
#     - Sample a random target in [0, total)
#     - Binary search to find the corresponding city
    
#     Time Complexity:
#     - __init__: O(n)
#     - pickIndex: O(log n)
    
#     Space Complexity: O(n)
#     """
    
#     def __init__(self, city_populations: List[Tuple[str, int]]):
#         """
#         Args:
#             city_populations: List of (city_name, population) tuples
#             Example: [("Seattle", 500), ("New York", 900), ("Los Angeles", 400)]
        
#         Raises:
#             ValueError: If input is invalid or contains duplicate city names
        
#         Time: O(n), Space: O(n)
#         """
#         # --- Base Case 1: Empty input ---
#         if not city_populations:
#             raise ValueError("city_populations cannot be empty")
        
#         self.city_names = []
#         self.prefix_sums = []  # Cumulative populations
#         total = 0
#         seen_cities = set()  # Track duplicate city names
        
#         # Alternative Option 2: Merge duplicates by combining populations
#         # Instead of rejecting duplicates, we can merge them:
#         # city_dict = {}  # city_name → total_population
#         # for item in city_populations:
#         #     if not isinstance(item, (list, tuple)) or len(item) != 2:
#         #         raise ValueError("Each entry must be (city_name, population)")
#         #     city_name, population = item
#         #     if not isinstance(city_name, str):
#         #         raise ValueError("City name must be a string")
#         #     if not isinstance(population, int) or population <= 0:
#         #         raise ValueError("Population must be a positive integer")
#         #     # Merge: if city exists, add to its population
#         #     if city_name in city_dict:
#         #         city_dict[city_name] += population
#         #     else:
#         #         city_dict[city_name] = population
#         # 
#         # # Build prefix sums from merged data
#         # total = 0
#         # for city_name, population in city_dict.items():
#         #     total += population
#         #     self.city_names.append(city_name)
#         #     self.prefix_sums.append(total)
#         # self.total = total
        
#         for item in city_populations:
#             # --- Base Case 2: Validate structure ---
#             if not isinstance(item, (list, tuple)) or len(item) != 2:
#                 raise ValueError("Each entry must be (city_name, population)")
            
#             city_name, population = item
            
#             # --- Base Case 3: Validate city name type ---
#             if not isinstance(city_name, str):
#                 raise ValueError("City name must be a string")
            
#             # --- Base Case 4: Validate population ---
#             if not isinstance(population, int) or population <= 0:
#                 raise ValueError("Population must be a positive integer")
            
#             # --- Base Case 5: Check for duplicate city names ---
#             # Option 1 (Current): Reject duplicates
#             if city_name in seen_cities:
#                 raise ValueError(f"Duplicate city name found: '{city_name}'")
#             seen_cities.add(city_name)
            
#             # Build prefix sums
#             total += population
#             self.city_names.append(city_name)
#             self.prefix_sums.append(total)
        
#         self.total = total  # Guaranteed > 0 due to validation
    
#     def pickIndex(self) -> str:
#         """
#         Randomly pick a city based on population weights.
        
#         Returns:
#             str: Random city name sampled proportional to population
        
#         Steps:
#         1. Generate target in [0, total)
#         2. Binary search for first index i where target < prefix_sums[i]
#         3. Return city_names[i]
        
#         Time: O(log n), Space: O(1)
#         """
#         # Generate random target in [0, total)
#         # random() * total → continuous floats in [0, total)
#         # Example: total=1800 → can generate 0.0, 500.5, 1250.3, 1799.9...
#         target = self.total * random.random()
        
#         # Alternative: Linear Search - O(n) time, simpler but slower
#         # Find first index where target < prefix_sum
#         # for i, prefix_sum in enumerate(self.prefix_sums):
#         #     if target < prefix_sum:
#         #         return self.city_names[i]
        
#         # Binary search: find smallest index i where target < prefix_sums[i]
#         left, right = 0, len(self.prefix_sums)  # Search range [left, right)
        
#         while left < right:
#             mid = left + (right - left) // 2  # Equivalent to (left + right) // 2
            
#             if target < self.prefix_sums[mid]:
#                 # Target is less than this boundary, search left
#                 right = mid
#             else:
#                 # target >= prefix_sums[mid], search right
#                 left = mid + 1
        
#         # Return CITY NAME at found index (instead of index itself)
#         # left == right at loop exit, both point to the answer
#         return self.city_names[left]
