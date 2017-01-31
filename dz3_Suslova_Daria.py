"""Написать класс MyQueue с использованием двух стеков.
То есть у вас будет класс Stack, внутри которого элементы собираются в массив,
и класс MyQueue, внутри которого элементы каким-то образом организованы в двух стеках.
Подсказка. Различие между очередью и стеком: из очереди удаляется самый старый элемент,
а из стека - самый новый.
Подсказка 2. Если все элементы из одного стека переложить в другой стек,
то "наверху" нового стека теперь будут самые старые элементы."""


class Stack:
    def __init__(self):
        self.st = []
    def push(self, item): 
        self.st.append(item)
    def pop(self): 
        return self.st.pop()
    def peek(self): 
        return self.st[len(self.st)-1]
    def isEmpty(self): 
        if len(self.st) == 0:
            return True
        else:
            return False


class MyQueue:
    def __init__(self):
        self.myq = []

    def enqueue(self, item):
        self.st = []
        self.st.append(item)
        for i in self.st:
            self.myq.append(i)

    def dequeue(self):
        return self.myq.pop()
    
    def peek(self): 
        return self.myq[0]
    
    def isEmpty(self): 
        if len(self.myq) == 0:
            return True
        else:
            return False

m = MyQueue()
x = [1, 3, 7, 8]
for i in x:
    m.enqueue(i)
print(m.peek())
        
        
