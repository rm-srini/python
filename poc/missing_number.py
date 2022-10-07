input = [4, 5, 1, 10, 8]
pre_val = 0
output = []
for val in sorted(input):
    diff = val - pre_val
    if diff > 1:
        for miss_val in range(diff-1):
            output.append(pre_val + miss_val + 1)
    pre_val = val
print(output)