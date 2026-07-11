"""
LeetCode 121. Best Time to Buy and Sell Stock
Difficulty: Easy
URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
"""

# Brute Force

class Solution:
    def maxProfit(self, prices):
        """ 
        Time Complexity: O(n²) 
        Space Complexity: O(1)
        """

        max_profit = 0
        
        for i in range(len(prices)):           # Try buying on each day
            for j in range(i + 1, len(prices)): # Try selling on each future day
                profit = prices[j] - prices[i]
                max_profit = max(max_profit, profit)
        
        return max_profit

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        Find maximum profit from buying and selling stock once.
        
        Args:
            prices: List[int] - array of stock prices
        
        Returns:
            int - maximum profit possible
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not prices or len(prices) < 2:
            return 0
        
        min_price = prices[0]  # Track minimum price seen so far
        max_profit = 0         # Track maximum profit possible
        
        for price in prices[1:]:
            # Calculate profit if we sell at current price
            profit = price - min_price
            
            # Update maximum profit if current profit is better
            max_profit = max(max_profit, profit)
            
            # Update minimum price if current price is lower
            min_price = min(min_price, price)
        
        return max_profit


# Variant : Best Time to Buy Flight Tickets

# Problem Statement

# You are given two arrays departures and returns where departures[i] and returns[i] are ticket prices for departing and returning flights on the ith day, respectively. You want to minimize your cost by choosing a single day to buy a departure flight and choosing a different day in the future to buy a returning flight. Return the minimum cost you can achieve from a single round-trip flight.

# Note: You must buy the return ticket on a day after the departure ticket (i.e., if you buy departure on day i, you can only buy return on day j where j > i).

# Example:
# Input: departures = [1,2,3,4], returns = [4,3,2,1]
# Output: 2
# Explanation: Buy a departure flight on day 0 (price = 1) and buy a return ticket on day 3 (price = 1), cost = 1+1 = 2.

# def minimumFlightCost(departures, returns):
#     """
#     Find minimum cost for round-trip flight tickets.
    
#     You need to buy a departure ticket on day i and a return ticket on day j
#     where j > i (return must be after departure).
    
#     Args:
#         departures: List[int] - prices for departure flights on each day
#         returns: List[int] - prices for return flights on each day
    
#     Returns:
#         int - minimum cost for round-trip
    
#     Time Complexity: O(n)
#     Space Complexity: O(1)
#     """
#     if not departures or not returns or len(departures) != len(returns):
#         return 0
    
#     n = len(departures)

#     if n < 2:  # Need at least 2 days for round trip
#         return 0
    
#     # Initialize to infinity so any valid cost will be smaller
#     # Why infinity? Because we don't know the valid cost range beforehand.
#     # Why not 0? All prices are >= 0, so min(0, any_valid_cost) would always be 0 (wrong!)
#     # Alternative approaches like min_cost = departures[0] + returns[1] assume 
#     # arrays have at least 2 elements (already checked above).
#     # Using float('inf') is safer and more readable - any real cost replaces it.
#     min_cost = float('inf')
#     min_departure = departures[0]  # Track minimum departure price seen so far
    
#     # Start from day 1 (index 1) since return must be after departure
#     for j in range(1, n):
#         # Current cost = cheapest departure so far + current return price
#         current_cost = min_departure + returns[j]
#         min_cost = min(min_cost, current_cost)
        
#         # Update minimum departure price for future returns
#         min_departure = min(min_departure, departures[j])
    
#     return min_cost
        
# Variant : departures and returns have different lengths

# def minimumFlightCostIterateReturns(departures, returns):
#     """
#     Find minimum cost for round-trip flight tickets when arrays have different lengths.

#     Time Complexity: O(m) - iterate through all m return days
#     Space Complexity: O(1) - only using constant extra space

#     Example (n > m, departures longer than returns):
#         departures = [1, 2, 3, 4, 5]  (n=5)
#         returns = [10, 8, 6]           (m=3)

#         j=1: current_cost = 1 + 8 = 9  -> min_cost = 9
#              min_departure = min(1, departures[1]=2) = 1
#         j=2: current_cost = 1 + 6 = 7  -> min_cost = 7
#              min_departure = min(1, departures[2]=3) = 1

#         Loop ends (range(1, 3) only covers j=1,2).
#         departures[3] and departures[4] are never checked - and that's fine,
#         since there's no return day 4 or 5 for them to pair with anyway.

#         Result: min_cost = 7 (depart day 0 @ $1, return day 2 @ $6)

#     Example (n < m, returns longer than departures):
#         departures = [1, 2, 3]        (n=3)
#         returns    = [5, 4, 3, 2, 1]  (m=5)

#         j=1: current_cost = 1 + 4 = 5  -> min_cost = 5
#              j < n (1<3)  -> min_departure = min(1, departures[1]=2) = 1
#         j=2: current_cost = 1 + 3 = 4  -> min_cost = 4
#              j < n (2<3)  -> min_departure = min(1, departures[2]=3) = 1
#         j=3: current_cost = 1 + 2 = 3  -> min_cost = 3
#              j < n (3<3)? False -> departures[3] doesn't exist, skip update
#         j=4: current_cost = 1 + 1 = 2  -> min_cost = 2
#              j < n (4<3)? False -> skip, departures[4] doesn't exist either

#         Result: min_cost = 2 (depart day 0 @ $1, return day 4 @ $1)

#     """
#     if not departures or not returns:
#         return -1

#     n = len(departures)
#     m = len(returns)

#     INF = float('inf')
#     min_cost = INF
#     min_departure = departures[0]

#     # Start from day 1 (first possible return day)
#     for j in range(1, m):

#         # Use the cheapest departure seen so far (min_departure) paired
#         # with today's return price. No bounds check needed here: this
#         # line only reads min_departure (a plain variable) and returns[j]
#         # (always valid since j ranges over 0..m-1) - neither can go out
#         # of bounds, and min_departure is guaranteed to always hold a
#         # real, valid departure price.
#         current_cost = min_departure + returns[j]
#         min_cost = min(min_cost, current_cost)

#         # CHECK: if j < n
#         # Why needed: we're about to read departures[j] to fold it into
#         # min_departure for FUTURE iterations. departures only has valid
#         # indices 0..n-1. If j >= n, departures[j] simply does not exist.
#         #
#         # What breaks if omitted:
#         #   departures = [1, 2, 3]        (n=3)
#         #   returns    = [5, 4, 3, 2, 1]  (m=5)
#         #   At j=3: departures[3] -> IndexError, list index out of range.
#         #   The loop crashes outright as soon as j reaches n. This check
#         #   is NOT optional - without it the function fails for any input
#         #   where n < m.
#         if j < n:
#             min_departure = min(min_departure, departures[j])

#     # min_cost can only stay INF if the loop never ran at all, i.e. m == 1:
#     # there's only one return day (day 0), and a departure must come
#     # strictly before it, which is impossible.
#     #
#     # Example:
#     #   departures = [1, 2, 3]  (n=3)
#     #   returns = [5]           (m=1)
#     #   range(1, 1) is empty -> loop never runs -> min_cost stays INF
#     return -1 if min_cost == INF else min_cost


# def minimumFlightCostIterateDepartures(departures, returns):
#     """
#     Find minimum cost for round-trip flight tickets, iterating over DEPARTURES
#     instead of returns. Walks backwards, tracking the minimum return seen so
#     far from everything strictly to the right.

#     Time Complexity: O(m) - touches every return day once during the walk
#     Space Complexity: O(1) - only a running min, no suffix array stored

#     Why backwards, not forwards?
#         At departure day i, we need the minimum return among days STRICTLY
#         AFTER i, i.e. [i+1, m-1]. Walking left to right, that information
#         isn't available yet when we reach day i - everything ahead is still
#         unvisited. Walking right to left flips this: by the time we reach
#         day i, everything to its right has already been seen, so the
#         running minimum is available for free in O(1) space. Going forward
#         would require either re-scanning ahead each time (O(n*m)) or
#         precomputing a suffix-min array up front (O(m) space).

#     Example:
#         departures = [1, 2]        (n=2)
#         returns = [10, 9, 8, 1]     (m=4)

#         day=3: 3 < n=2? No, skip.        min_return = min(INF, 1) = 1
#         day=2: 2 < n=2? No, skip.        min_return = min(1, 8) = 1
#         day=1: 1 < n=2? Yes -> cost = departures[1]=2 + min_return=1 = 3
#                                           min_return = min(1, 9) = 1
#         day=0: 0 < n=2? Yes -> cost = departures[0]=1 + min_return=1 = 2
#                                           min_return = min(1, 10) = 1

#         Result: min_cost = 2 (depart day 0 @ $1, return day 3 @ $1)
#     """
#     if not departures or not returns:
#         return -1

#     n = len(departures)
#     m = len(returns)

#     min_cost = float('inf')
#     # Running minimum of returns[day+1 .. m-1] - every return day strictly
#     # AFTER the day currently being examined. Starts at INF because when
#     # day = m-1 (the last day), nothing exists after it yet.
#     min_return = float('inf')

#     # Walk every day from the last one back to day 0. We check "can day be
#     # a departure?" BEFORE folding today's return price into min_return,
#     # so min_return only ever reflects days strictly greater than the
#     # current one - enforcing "return must be after departure."
#     for day in range(m - 1, -1, -1):

#         # departures only has indices 0..n-1, so day must be < n to be a
#         # valid departure day. If valid, pair it with the cheapest return
#         # seen so far among days > day (min_return).
#         if day < n:
#             cost = departures[day] + min_return
#             min_cost = min(min_cost, cost)

#         # Fold returns[day] into the running minimum now, so it's
#         # available for earlier (smaller) departure days to use.
#         min_return = min(min_return, returns[day])

#     # min_cost stays INF if no day ever had both a valid departure (day < n)
#     # and a valid return already seen after it (min_return != INF).
#     #
#     # Example:
#     #   departures = [1, 2, 3]  (n=3)
#     #   returns = [5]           (m=1)
#     #   day=0 is the only day < n, but min_return is still INF at that
#     #   point (m-1=0 is the last day in the walk, nothing came before it),
#     #   so no valid pair exists -> return -1.
#     return -1 if min_cost == float('inf') else min_cost