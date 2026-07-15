# https://leetcode.com/problems/maximum-subarray/

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [nums[0]]*n
        mx = dp[0]
        for i in range(1,n):
            dp[i] = max(nums[i], nums[i]+dp[i-1])
            mx = max(mx, dp[i])
        
        return mx
    
sol = Solution()
print(sol.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))