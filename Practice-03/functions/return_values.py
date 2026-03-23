def get_min_max(numbers):
    return min(numbers), max(numbers)

nums = [3, 7, 1, 9]
mn, mx = get_min_max(nums)
print(mn, mx)