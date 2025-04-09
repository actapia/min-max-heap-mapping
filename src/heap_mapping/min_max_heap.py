import operator
from collections import namedtuple
from dataclasses import dataclass
import math

from collections.abc import MutableMapping

from typing import Optional

def heap_parent(i: int) -> Optional[int]:
    """Return the parent index for the provided index in a binary heap."""
    if i > 0:
        return ((i + 1) >> 1) - 1 

def heap_left(i: int) -> int:
    """Return the left child index for the provided index in a binary heap."""
    return 2*i + 1

def heap_right(i: int) -> int:
    """Return the right child index for the provided index in a binary heap."""
    return 2*(i+1)

def heap_level(i: int) -> int:
    """Return the level of the index in a binary heap."""
    return len("{:b}".format(i+1)) - 1

order = namedtuple("orders", ["lt", "gt", "ext", "inf"])

orders = [
    order(operator.lt, operator.gt, min, math.inf),
    order(operator.gt, operator.lt, max, -math.inf)
]

@dataclass(order=True)
class HeapNode:
    """A class representing an element in a heap.
    
    This class has no public attributes. Instances of this class should not be
    modified directly by code outside of MinMaxHeap.

    The priority and value of the node may be accessed using the class's
    properties.
    """
    _priority: object
    _value: object

    @property
    def priority(self):
        """Return the priority of the node in the heap."""
        return self._priority
    
    @property
    def value(self):
        """Return the value associated with the node in the heap."""
        return self._value

    def __iter__(self):
        """Yields the priority followed by the value. (Useful for unpacking.)"""
        yield self.priority
        yield self.value

class MinMaxHeap(MutableMapping):
    """A min-max heap supporting priority updates via a mapping-like interface.
    
    The code in this class is based on pseudocode from Wikipedia (at 
    https://en.wikipedia.org/w/index.php?title=Min-max_heap&oldid=1218430646)
    and Atkinson et al. 1986. Min-Max Heaps and Generalized Priority Queues.

    In addition to the proper heap structure stored in a list, MinMaxHeap keeps
    track of element locations via a dict. Element priorities are also stored
    explicitly in a dict (as well as in the heap proper) to simplify certain
    operations.

    Elements in the heap are stored as instances of the HeapNode class. A
    HeapNode keeps track of its value as well as its priority. Some methods of
    MinMaxHeap return HeapNode objects, allowing one to access both the priority
    and the value. HeapNode objects are iterable, allowing easy unpacking of the
    priority and value.

    A MinMaxHeap may be treated as a double-ended priority queue. The minimum
    (maximum) element may be retrieved with the min (max) property and can be
    removed and retrieved with the pop_min (pop_max) method. A new element can
    be added with the add method.

    A MinMaxHeap can also be treated as a mapping from values to priorities.
    The priority of an element x may be set to p using the heap's __setitem__
    method---e.g., heap[x] = p. If x is not already in the heap, it will be
    added.
    """
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

    def _push_down_ext(self, i, o):
        if self._has_child(i):
            m = o.ext(
                (self._values[i], i) for i in self._descendants(i, 2)
            )[1]
            if heap_parent(m) != i:
                if o.lt(self._values[m], self._values[i]):
                    self._swap_indices(m, i)
                    if o.gt(self._values[m], self._values[heap_parent(m)]):
                        self._swap_indices(m, heap_parent(m))
                    self._push_down(m)
            elif o.lt(self._values[m], self._values[i]):
                self._swap_indices(m, i)
    
    def _push_up(self, i):
        if i != 0:
            level = heap_level(i)%2
            o = orders[level]
            ro = orders[not level]
            parent = heap_parent(i)
            if o.gt(self._values[i], self._values[parent]):
                self._swap_indices(i, parent)
                return self._push_up_ext(parent, ro)
            else:
                return self._push_up_ext(i, o)
            
    def _push_up_ext(self, i, o):
        if i > 0 and heap_parent(i) > 0:
            grandparent = heap_parent(heap_parent(i))
            if o.lt(self._values[i], self._values[grandparent]):
                self._swap_indices(i, grandparent)
                self._push_up_ext(grandparent, o)

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
        priority = self._values[i].priority
        self._swap_indices(i, self._length - 1)
        del self._lookup[self._values[self._length - 1].value]
        del self._priorities[self._values[self._length - 1].value]
        self._length -= 1
        node = self._values[self._length]
        self._push_for_changed_priority(i, priority, self._values[i].priority)
        return node

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
    
    def _push_for_changed_priority(self, i, old_priority, priority):
        # print("Push for ", i)
        o = orders[heap_level(i)%2]
        if o.lt(priority, old_priority):
            self._push_up(i)
        elif o.gt(priority, old_priority):
            if i > 0 and o.gt(
                priority,
                self._values[heap_parent(i)].priority
            ):
                self._swap_indices(i, heap_parent(i))
                self._push_up(heap_parent(i))
            self._push_down(i)
    
    def _update_priority_at(self, i, priority):
        # print("Update priority at", i)
        old_priority = self._values[i].priority
        self._values[i]._priority = priority
        self._priorities[self._values[i].value] = priority
        self._push_for_changed_priority(i, old_priority, priority)

    def add(self, value, priority=None):
        if value in self._lookup:
            raise ValueError("heap must not contain value")
        if priority is None:
            priority = self._key(value)
        # o = orders[heap_level(self._length)%2]
        new_element = HeapNode(priority, value)
        if (len(self._values) == self._length):
            self._values.append(new_element)
        else:
            self._values[self._length] = new_element
        self._lookup[value] = self._length
        self._length += 1
        self._priorities[value] = priority
        self._push_up(self._length - 1)

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
            self._update_priority_at(self._lookup[k], v)
        except KeyError:
            self.add(k, v)

    def __delitem__(self, k):
        self.pop(k)

    def __iter__(self):
        return iter(self.keys())

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