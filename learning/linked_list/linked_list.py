class Node(object):

    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

    def __repr__(self):
        return str(self.data)


class LinkedList(object):

    def __init__(self):
        self.head = None

    def prepend(self, data):
        new_head = Node(data)
        new_head.next = self.head
        self.head = new_head

    def append(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
        else:
            iter_node = self.head
            while iter_node.next:
                iter_node = iter_node.next
            iter_node.next = new_node

    def insert(self, position, data):
        if position == 0 or not self.head:
            self.prepend(data)
        else:
            node_to_insert = Node(data)
            iter_node = self.head
            pos = position
            while pos > 1 and iter_node.next:
                iter_node = iter_node.next
                pos -= 1
            node_to_insert.next = iter_node.next
            iter_node.next = node_to_insert

    def delete(self, position):
        if not self.head:
            pass
        elif position == 0:
            self.head = self.head.next
        else:
            iter_node = self.head
            pos = position
            while pos > 1 and iter_node.next:
                iter_node = iter_node.next
                pos -= 1
            if iter_node.next:
                iter_node.next = iter_node.next.next

    def reverse(self):
        if self.head:
            prev = None
            current = self.head
            while current:
                future = current.next
                current.next = prev
                prev = current
                current = future
            self.head = prev

    def __repr__(self):
        output_string = ""
        iter_node = self.head
        while iter_node:
            output_string += str(iter_node) + ", "
            iter_node = iter_node.next
        return "[" + output_string[:-2] + "]"

    def __getitem__(self, position):
        if not self.head:
            return None
        else:
            iter_node = self.head
            pos = position
            while pos > 0 and iter_node.next:
                iter_node = iter_node.next
                pos -= 1
            return iter_node.data

    def __eq__(self, other_list):
        iter_node_A = self.head
        iter_node_B = other_list.head
        while iter_node_A and iter_node_B:
            if iter_node_A.data != iter_node_B.data:
                return False
            iter_node_A = iter_node_A.next
            iter_node_B = iter_node_B.next
        if not iter_node_A and not iter_node_B:
            return True
        else:
            return False

    def __iter__(self):
        iter_node = self.head
        while iter_node:
            yield iter_node
            iter_node = iter_node.next


lst = LinkedList()
lst.append('A')
lst.append('B')
lst.append('C')
print(lst)
lst.reverse()
print(lst)
lst.delete(1)
print(lst)

