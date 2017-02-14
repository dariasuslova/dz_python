class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def printList(self):
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print()

    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node

    def size(self):
        node = self.head
        i = 1
        if not node:
            i = 0
        else:
            while node.next:
                node = node.next
                i+=1
        return i

    def delete (self, value):
        node = self.head
        n = node.next
        while n:
            if n.next is not None and n.next.data == value:
                 n.next = n.next.next
            else:
                n = n.next
            
    def insert(self, value, index):
        if index == 0:
            self.push(value)
        elif index == self.size():
            self.append(value)
        elif index > self.size():
            print('index out of range')
        else:
            i = 0
            node = self.head
            node_p = None 
            while node:
                if i != index:
                    node_p = node
                    node = node.next
                else:
                    node_p.next = Node(value, next=node)
                i+=1

    def reverse(self, head):
        current = self.head
        previous = None
        while current is not None:
            nxt = current.next
            current.next = previous
            previous = current
            current = nxt
        self.head = previous

n3 = Node(3)
n2 = Node(2, next=n3)
n1 = Node(1, next=n2)


l = LinkedList(head=n1)
for i in [1,2,3,4,5,4,5,6,6,6,6,1,1,54,3]:
    l.append(i)
l.insert(18,1)
l.reverse(n1)
l.printList()


