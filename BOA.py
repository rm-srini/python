
d =   [
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
            return lst
            break

def get_hierarchy(emp1,emp2):
    lst = fun(emp1, emp2)
    if emp1 in  lst:
        return True
    else:
        return False



print(get_hierarchy('A', 'X'))