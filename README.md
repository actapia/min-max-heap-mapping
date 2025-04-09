# heap-mapping

This is a library containing an implementation of the min-max heap data
structure, which allows for $O(log(n))$ retrieval or removal of both the
minimum and maximum elements of the heap, as well as insertion and keys and
changes to their priorities. Heap creation can be additionally performed in
$O(n)$ time.

The data structure can be accessed as `MutableMapping`; keys are the
"values" stored in the data structure, and values are their priorities.

## Getting started

You can construct a `MinMaxHeap` from a list of values.

```python
from heap_mapping import MinMaxHeap

heap = MinMaxHeap([5, 0, 4, 1, 2, 9, 8])
print(heap.min_value) # 0
print(heap.max_value) # 9
```

By default, priorities are the same as the values.

```python
print(heap[5]) # 5
```

You can specify a key function
in the constructor to get a priority from each element.

```python
heap2 = MinMaxHeap([5, 0, 4, 1, 2, 9, 8], key=lambda x: -x)
print(heap2.min_value) # 9
print(heap2.max_value) # 0
print(heap2[5]) # -5
```

You can add elements with the `add` method. By default, the key function
specified in the constructor is used to get the priority.

```python
heap2.add(7)
print(heap2[7]) # -7
```

Alternatively, you can manually specify a key.

```python
heap2.add(6, -3)
print(heap2[6]) # -3
```

You can change the priorities after they've been inserted.

```python
heap2[7] = 1
print(heap2.max_value) # 7
```

You can look up and delete arbitrary elements in $O(log(n))$ time.

```python
del heap2[6]
print(6 in heap2) # False
```

Iteration is performed out of order. Note that this order is also *not* the
order in which the elements are stored in the heap!

```python
print(list(heap2)) # [5, 0, 4, 1, 2, 9, 8, 7]
```