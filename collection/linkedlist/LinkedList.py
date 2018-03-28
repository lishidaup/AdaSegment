# !/usr/bin/env python
# coding=utf-8
# by lsd 2017-05-18

class Node(object):
    def __init__(self, data, pnext=None):
        self.data = data
        self._next = pnext

    def __repr__(self):
        return str(self.data)


class LinkedList(object):
    def __init__(self):
        self.head = None
        self.length = 0

    def isEmpty(self):
        return self.length == 0

    def init(self, data_list):
        for i in data_list:
            self.append(i)
        return self

    def append(self, dataOrNode):
        item = None
        if isinstance(dataOrNode, Node):
            item = dataOrNode
        else:
            item = Node(dataOrNode)

        if not self.head:
            self.head = item
            self.length += 1

        else:
            node = self.head
            while node._next:
                node = node._next
            node._next = item
            self.length += 1

    def delete(self, index):
        if self.isEmpty():
            return

        if index < 0 or index >= self.length:
            return

        if index == 0:
            self.head = self.head._next
            self.length -= 1
            return

        j = 0
        node = self.head
        prev = self.head
        while node._next and j < index:
            prev = node
            node = node._next
            j += 1

        if j == index:
            prev._next = node._next
            self.length -= 1

    def insert(self, index, dataOrNode):
        item = None
        if isinstance(dataOrNode, Node):
            item = dataOrNode
        else:
            item = Node(dataOrNode)

        if index == 0:
            item._next = self.head
            self.head = item
            self.length += 1
            return

        if index < 0 or index >= self.length:
            return

        j = 0
        node = self.head
        prev = self.head
        while node._next and j < index:
            prev = node
            node = node._next
            j += 1

        if j == index:
            item._next = node
            prev._next = item
            self.length += 1

    def update(self, index, data):
        if self.isEmpty() or index < 0 or index >= self.length:
            return
        j = 0
        node = self.head
        while node._next and j < index:
            node = node._next
            j += 1

        if j == index:
            node.data = data

    def getItem(self, index):
        if self.isEmpty() or index < 0 or index >= self.length:
            return
        j = 0
        node = self.head
        while node._next and j < index:
            node = node._next
            j += 1

        return node.data

    def getIndex(self, data):
        j = 0
        if self.isEmpty():
            return
        node = self.head
        while node:
            if node.data == data:
                return j
            node = node._next
            j += 1

        if j == self.length:
            return

    def clear(self):
        self.head = None
        self.length = 0

    def getLast(self):
        if not self.isEmpty():
            return self[self.length - 1]
        return

    def getFirst(self):
        if not self.isEmpty():
            return self[0]
        return

    def addAll(self, c):
        for i in range(len(c)):
            self.append(c[i])

    def __repr__(self):
        if self.isEmpty():
            return "__repr__:empty linkedlist"
        node = self.head
        nlist = ''
        while node:
            nlist += str(node.data) + ' '
            node = node._next
        return nlist

    def __getitem__(self, ind):
        if self.isEmpty() or ind < 0 or ind >= self.length:
            return
        return self.getItem(ind)

    def __setitem__(self, ind, val):
        if self.isEmpty() or ind < 0 or ind >= self.length:
            return
        self.update(ind, val)

    def __len__(self):
        return self.length


if __name__ == '__main__':
    chain = LinkedList()
    chain.init([1, 2, 3])
    print chain
    chain.insert(0, 0)
    print chain
    a = iter(chain)
    print a.next()
    print a.next()

