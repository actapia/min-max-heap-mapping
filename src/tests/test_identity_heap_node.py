import unittest

from heap_mapping.min_max_heap import MinMaxHeap, IdentityHeapNode, HeapNode

class TestIdentityHeapNode(unittest.TestCase):
    def test_identity_heap_node(self):
        objs = [object() for _ in range(10)]
        heap = MinMaxHeap()
        heap[objs[0]] = 12
        with self.assertRaises(TypeError):
            heap[objs[1]] = 12
        iheap = MinMaxHeap(node_class=IdentityHeapNode)
        for x in objs[:5]:
            iheap[x] = 12
        for x in reversed(objs[5:]):
            iheap[x] = 12
        self.assertLess(id(iheap.min_value), id(iheap.max_value))