"""
Question 1: A String with number separated by space will be passed to a method
and an operator will be present at the end like '5 12 3 +', based on the
operator we need to add/subtract these number 0 + 5 + 12 + 3 = 20
Similarly for '2 9 - ' it should be 0 - 2 - 9 = 11
"""

def perform_operation(num: int, val: str, opr: str):
    if opr == '+':
        num += int(val)
    elif opr == '-':
        num -= int(val)
    elif opr == '*':
        num = num * int(val)
    elif opr == '/':
        num = num / int(val)
    return num

def simple_calculate(exp: str, num=0):
    lst = exp.split()
    opr = lst[-1]
    for i in range(len(lst)-1):
        num = perform_operation(num, lst[i], opr)
    return num


print(simple_calculate('5 6 8 1 +'))
print(simple_calculate('5 6 1 +'))

"""
Question 2: Similar to previous question only difference is that the number and
operator can be mixed together for example '2 5 + 8 * 4 10 +' for this case
it should work like (0 + 2 + 5) * 8 + (4 + 10) = 94
"""
def complex_calculator_sol1(exp: str):
    lst = exp.split()
    cnt = 0
    lst_dic = []
    while cnt < len(lst):
        num_lst = []
        dic = {}
        for i in range(cnt, len(lst)):
            if lst[i] in ['+', '-', '*', '/']:
                dic['opr'] = lst[i]
                dic['num'] = num_lst
                cnt = i + 1
                break
            else:
                num_lst.append(int(lst[i]))
        lst_dic.append(dic)
    num = 0
    for i_dic in lst_dic:
        for n in i_dic['num']:
            num = perform_operation(num, n, i_dic['opr'])
    return num


print(complex_calculator_sol1('2 5 + 4 10 + 2 * 10 2 -'))


def complex_calculator_sol2(exp: str):
    start = 0
    end = 0
    num = 0
    for pos in range(0, len(exp)):
        if exp[pos] in ['+', '-', '*', '/']:
            end = pos + 1
            num = simple_calculate(exp[start: end], num)
            start = end + 1
    return num


print(complex_calculator_sol2('2 5 + 4 10 + 2 * 10 2 -'))
