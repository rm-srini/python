"""
Print the unique number in the input list
"""
lst = [1, 1, 2, 3, 3, 4, 4]
dic = {}
for i in lst:
    dic[i] = 1 if i not in dic else dic[i] + 1
for k in dic:
    if dic[k] == 1:
        print(k)

'''
Print the number nearest to zero in below list
'''
lst = [5, 2, -6, -7, -1, 10, 3]
diff = 10000000000
num = 0
for i in range(len(lst)):
    if diff >= abs(0 - abs(lst[i])):
        diff = abs(0-abs(lst[i]))
        num=lst[i]
print(num)


print(min(lst, key=abs))