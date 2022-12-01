'''
Piece of code to get two inputs and find if there is a relationship exists between the two
'''
# Solution 1
d = [
    {'B': 'A'},
    {'C': 'A'},
    {'D': 'B'},
    {'X': 'D'},
    {'Y': 'X'},
    {'F': 'E'}
    # #{'Employee': 'F', 'Manager': 'E'}
    ]

def get_parent(emp):
    for i in d:
        if emp in i:
            return i[emp]

def fun(emp1, emp2):
    lst = []
    parent = emp2
    while True:
        parent = get_parent(parent)
        if parent != None:
            lst.append(parent)
        else:
            break
    return lst

def get_hierarchy(emp1,emp2):
    lst = fun(emp1, emp2)
    if emp1 in  lst:
        return True
    else:
        return False

print(get_hierarchy('A', 'F'))



# Solution 2
d = {
    'A': None,
    'B': 'A',
    'C': 'A',
    'D': 'B',
    'X': 'D',
    'Y': 'X',
    'E': None,
    'F': 'E'
}
lst = []
def get_parents(emp):
    if emp in d:
        lst.append(d[emp])
    if d[emp] is None:
        return lst
    e = d[emp]
    return get_parents(e)

def validate(manager, employee):
    lst = get_parents(employee)
    if manager in lst:
        result = True
    else:
        result = False
    return result

print(validate('A', 'F'))
