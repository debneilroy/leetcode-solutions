"""
LeetCode 121. Best Time to Buy and Sell Stock
Difficulty: Easy
URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
"""

# Brute Force

# def maxProfit(prices):
#     """ 
#     Time Complexity: O(n²) 
#     Space Complexity: O(1)
#     """

#     max_profit = 0
    
#     for i in range(len(prices)):           # Try buying on each day
#         for j in range(i + 1, len(prices)): # Try selling on each future day
#             profit = prices[j] - prices[i]
#             max_profit = max(max_profit, profit)
    
#     return max_profit

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

# You are given two arrays departures and returns where departures[i] and returns[i] are ticket prices for departing and returning flights on the ith day, respectively. You want to minimize your cost by choosing a single day to buy a departure flight and choosing a different day in the future to buy a returning flight.Return the minimum cost you can achieve from a single round-trip flight.

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
#     """
#     if not departures or not returns:
#         return 0
    
#     n = len(departures)
#     m = len(returns)
    
#     INF = float('inf')
#     min_cost = INF
#     min_departure = departures[0]
    
#     # Start from day 1 (first possible return day)
#     for j in range(1, m):
#         # Can only use this return day if we had a valid departure day before it
#         if j - 1 < n:  # If day j-1 exists in departures
#             # Use the cheapest departure from days 0 to min(j-1, n-1)
#             current_cost = min_departure + returns[j]
#             min_cost = min(min_cost, current_cost)
        
#         # Update minimum departure for future returns
#         # Check if j < n: We're on return day j, and we want to consider
#         # departures[j] as a potential departure for FUTURE return days.
#         # But departures[j] only exists if j < n (departures has indices 0 to n-1).
#         # Example: n=3, m=5. When j=4, departures[4] doesn't exist, so we skip.
#         if j < n:
#             min_departure = min(min_departure, departures[j])
    
#     return 0 if min_cost == INF else min_cost