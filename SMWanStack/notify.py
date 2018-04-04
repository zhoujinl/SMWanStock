# -*- coding:utf-8 -*-


def solution(nums):
    if nums == None :
        return "[]"
    else :
        nums.sort()
        return nums

nums = [1,2,3,10,5]
print(solution(nums))

nums = []
print(solution(nums))

nums = None
print(solution(nums))