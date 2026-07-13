# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted

def twoSum(numbers: List[int], target: int) -> List[int]:
    n = len(numbers)
    l = 0
    r = n-1

    while(l<r):
        if(numbers[l]+numbers[r]==target):
            return[l+1, r+1]
        elif(numbers[l]+numbers[r]<target):
            l+=1
        else:
            r-=1

print(twoSum([2,7,11,15], 9))

