# https://leetcode.com/problems/3sum/


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        ans = []

        nums.sort()
        for i in range(0, n-2):
            j = i+1
            k = n-1
            if(i>0 and nums[i]==nums[i-1]): continue
            while(j<k):
                total = nums[i]+nums[j]+nums[k]
                if(total==0):
                    ans.append([nums[i],nums[j],nums[k]])
                    while(j<k and nums[j]==nums[j+1]): j+=1
                    while(j<k and nums[k]==nums[k-1]): k-=1
                    j+=1
                    k-=1
                elif(total<0):
                    j+=1
                elif(total>0):
                    k-=1
            
        return ans


sol = Solution()
print(sol.threeSum([-1,0,1,2,-1,-4]))
