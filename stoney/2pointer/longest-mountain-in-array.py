# https://leetcode.com/problems/longest-mountain-in-array

class Solution:
    def longestMountain(self, arr: List[int]) -> int:
        n = len(arr)
        i = 1
        ans = 0
        while(i<n):
            upper = 0
            lower = 0

            while(i<n and arr[i-1]==arr[i]):
                i+=1

            while(i<n and arr[i-1]<arr[i]):
                upper+=1
                i+=1

            while(i<n and arr[i-1]>arr[i]):
                lower+=1
                i+=1

            if(upper and lower):
                ans = max(ans, upper+lower+1)
        
        return ans

sol = Solution()
print(sol.longestMountain([2,1,4,7,3,2,5]))