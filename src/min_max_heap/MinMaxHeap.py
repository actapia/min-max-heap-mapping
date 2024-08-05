import operator
from collections import namedtuple
from dataclasses import dataclass
from numbers import Number
import math

from collections.abc import MutableMapping

def heap_parent(i):
    if i > 0:
        return ((i + 1) >> 1) - 1 

def heap_left(i):
    return 2*i + 1

def heap_right(i):
    return 2*(i+1)

def heap_level(i):
    return len("{:b}".format(i+1)) - 1

order = namedtuple("orders", ["lt", "gt", "ext"])

orders = [
    order(operator.lt, operator.gt, min),
    order(operator.gt, operator.lt, max)
]

@dataclass(order=True)
class HeapNode:
    priority: Number
    value: object

    def __iter__(self):
        yield self.priority
        yield self.value

class MinMaxHeap(MutableMapping):
    def __init__(self, data=None, key=lambda x: x, maxsize=0):
        if data is None:
            data = []
        self._values = [HeapNode(key(i), i) for i in data]
        self._length = len(data)
        self._lookup = dict(map(reversed, enumerate(data)))
        self._max_size = maxsize
        self._priorities = {k.value: k.priority for k in self._values}
        self._key = key
        self._make_heap()

    # def qsize(self):
    #     return len(self)
    
    # def empty(self):
    #     return len(self) > 0

    def _make_heap(self):
        for i in range(self._length//2 - 1, -1, -1):
            self._push_down(i)

    def _has_child(self, i):
        return heap_left(i) < self._length
    
    def _get_left(self, i):
        if (res := heap_left(i)) < self._length:
            return res
        
    def _get_right(self, i):
        if (res := heap_right(i)) < self._length:
            return res
        
    def _children(self, i):
        if (left := self._get_left(i)):
            yield left
        if (right := self._get_right(i)):
            yield right

    @property
    def _height(self):
        return heap_level(self._length-1)
    
    def _descendants(self, i, levels=None):
        if levels is None:
            levels = self._height - heap_level(i)
        yield from self._children(i)
        if levels > 1:
            for c in self._children(i):
                yield from self._descendants(c, levels=levels-1)

    def _push_down(self, i):
        return self._push_down_ext(i, orders[heap_level(i)%2])

    def _push_down_ext(self, i, ord):
        if self._has_child(i):
            m = ord.ext(
                (self._values[i], i) for i in self._descendants(i, 2)
            )[1]
            if heap_parent(m) != i:
                if ord.lt(self._values[m], self._values[i]):
                    self._swap_indices(m, i)
                    if ord.gt(self._values[m], self._values[heap_parent(m)]):
                        self._swap_indices(m, heap_parent(m))
                    self._push_down(m)
            elif ord.lt(self._values[m], self._values[i]):
                self._swap_indices(m, i)
    
    def _push_up(self, i):
        if i != 0:
            level = heap_level(i)%2
            ord = orders[level]
            rord = orders[not level]
            parent = heap_parent(i)
            if ord.gt(self._values[i], self._values[parent]):
                self._swap_indices(i, parent)
                return self._push_up_ext(parent, rord)
            else:
                return self._push_up_ext(i, ord)
            
    def _push_up_ext(self, i, ord):
        if i > 0 and heap_parent(i) > 0:
            grandparent = heap_parent(heap_parent(i))
            if ord.lt(self._values[i], self._values[grandparent]):
                self._push_up_ext(grandparent, ord)

    @property
    def _min_index(self):
        if self._length <= 0:
            raise IndexError("empty heap")
        return 0
    
    @property
    def _max_index(self):
        if self._length <= 0:
            raise IndexError("empty heap")
        if self._length == 1:
            return 0
        elif self._length == 2:
            return 1
        elif self._values[1] > self._values[2]:
            return 1
        else:
            return 2
        
    @property
    def min(self):
        return self._values[self._min_index]
    
    @property
    def max(self):
        return self._values[self._max_index]
    
    @property
    def min_value(self):
        return self.min.value
    
    @property
    def max_value(self):
        return self.max.value
    
    def _delete_at(self, i):
        self._swap_indices(i, self._length - 1)
        del self._lookup[self._values[self._length - 1].value]
        del self._priorities[self._values[self._length - 1].value]
        self._length -= 1
        self._push_down(i)
        return self._values[self._length]

    def pop_min(self):
        return self._delete_at(self._min_index)
    
    def pop_min_value(self):
        return self.pop_min().value
    
    def pop_max(self):
        return self._delete_at(self._max_index)
    
    def pop_max_value(self):
        return self.pop_max().value
    
    def heapsort_asc(self):
        while self:
            yield self.pop_min_value()

    def heapsort_desc(self):
        while self:
            yield self.pop_max_value()
    
    def delete_value(self, value):
        return self._delete_at(self._lookup[value])
    
    def _decrease_priority_at(self, i, priority):
        if priority > self._values[i].priority:
            raise ValueError(
                "new key is too large ({} > {})".format(
                    priority,
                    self._values[i].priority
                )
            )
        self._values[i].priority = priority
        self._priorities[self._values[i].value] = priority
        self._push_up(i)

    def add(self, value, priority=None):
        if value in self._lookup:
            raise ValueError("heap must not contain value")
        new_element = HeapNode(math.inf, value)
        if (len(self._values) == self._length):
            self._values.append(new_element)
        else:
            self._values[self._length] = new_element
        self._lookup[value] = self._length
        self._length += 1
        if priority is None:
            priority = self._key(value)
        self._decrease_priority_at(self._length - 1, priority)

    # def put(self, value, priority=None):
    #     return self.add(value, priority=priority)

    def _swap_indices(self, i, j):
        temp = self._values[i]
        self._values[i] = self._values[j]
        self._values[j] = temp
        self._lookup[self._values[i].value] = i
        self._lookup[self._values[j].value] = j
    
    def __getitem__(self, k):
        return self._priorities[k]
    
    def __setitem__(self, k, v):
        try:
            self._decrease_priority_at(self._lookup[k], v)
        except KeyError:
            self.add(k, v)

    def __delitem__(self, k):
        self.pop(k)

    def __iter__(self):
        return self.keys()

    def __len__(self):
        return self._length
    
    def __contains__(self, k):
        return k in self._lookup
    
    def keys(self):
        return self._priorities.keys()

    def values(self):
        return self._priorities.values()
    
    def __eq__(self, other):
        return self._priorities == other._priorities
    
    def __ne__(self, other):
        return self._priorities != other._priorities
    
    def __bool__(self):
        return self._length > 0
    
    def pop(self, k):
        return self.delete_value(k).priority
    

if __name__ == "__main__":
    from IPython import embed
    embed()