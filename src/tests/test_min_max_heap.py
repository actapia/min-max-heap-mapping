import unittest
from heap_mapping.min_max_heap import *

class TestMinMaxHeap(unittest.TestCase):
    example_data = [12, 24, -1, 1, 14, 3, 55, 91, 0, 13]
    data2 = [0, 22, 23, 4, 5, 2, 1, 10, 11, 14, 17, 21, 20, 19, 18, 6, 7, 8, 9, 12, 13, 15, 16, 3]

    def test_heap_parent(self):
        self.assertEqual(heap_parent(1), 0)
        self.assertEqual(heap_parent(3), 1)
        self.assertEqual(heap_parent(4), 1)
        self.assertIsNone(heap_parent(0))

    def test_heap_left(self):
        self.assertEqual(heap_left(0), 1)
        self.assertEqual(heap_left(1), 3)
        self.assertEqual(heap_left(2), 5)
        self.assertEqual(heap_left(3), 7)

    def test_heap_right(self):
        self.assertEqual(heap_right(0), 2)
        self.assertEqual(heap_right(1), 4)
        self.assertEqual(heap_right(2), 6)
        self.assertEqual(heap_right(3), 8)

    def test_heap_level(self):
        self.assertEqual(heap_level(0), 0)
        self.assertEqual(heap_level(1), 1)
        self.assertEqual(heap_level(2), 1)
        self.assertEqual(heap_level(5), 2)

    def test_get_left(self):
        heap = MinMaxHeap(self.example_data)
        self.assertEqual(heap._get_left(0), 1)
        self.assertEqual(heap._get_left(4), 9)
        self.assertIsNone(heap._get_left(5))

    def test_get_right(self):
        heap = MinMaxHeap(self.example_data)
        self.assertEqual(heap._get_right(0), 2)
        self.assertEqual(heap._get_right(3), 8)
        self.assertIsNone(heap._get_right(4))

    def test_children(self):
        heap = MinMaxHeap(self.example_data)
        self.assertEqual(set(heap._children(0)), {1, 2})
        self.assertEqual(set(heap._children(2)), {5, 6})
        self.assertEqual(set(heap._children(4)), {9})
        self.assertEqual(set(heap._children(5)), set())

    def test_descendants(self):
        heap = MinMaxHeap(self.example_data)
        self.assertEqual(set(heap._descendants(0, 1)), set(range(1,3)))
        self.assertEqual(set(heap._descendants(0, 2)), set(range(1, 7)))
        self.assertEqual(set(heap._descendants(0, 3)), set(range(1, 10)))
        self.assertEqual(set(heap._descendants(0, 4)), set(range(1, 10)))
        self.assertEqual(set(heap._descendants(0)), set(range(1, 10)))
        self.assertEqual(set(heap._descendants(1, 1)), set(range(3, 5)))
        self.assertEqual(set(heap._descendants(1, 2)), {3, 4, 7, 8, 9})
        self.assertEqual(set(heap._descendants(1, 3)), {3, 4, 7, 8, 9})
        self.assertEqual(set(heap._descendants(1)), {3, 4, 7, 8, 9})
        self.assertEqual(set(heap._descendants(2, 1)), set(range(5, 7)))
        self.assertEqual(set(heap._descendants(2, 2)), set(range(5, 7)))
        self.assertEqual(set(heap._descendants(2)), set(range(5, 7)))
        self.assertEqual(set(heap._descendants(3, 1)), set(range(7, 9)))
        self.assertEqual(set(heap._descendants(3, 2)), set(range(7, 9)))
        self.assertEqual(set(heap._descendants(3)), set(range(7, 9)))
        self.assertEqual(set(heap._descendants(4, 1)), {9})
        self.assertEqual(set(heap._descendants(4, 2)), {9})
        self.assertEqual(set(heap._descendants(4)), {9})
        self.assertEqual(set(heap._descendants(5, 1)), set())
        self.assertEqual(set(heap._descendants(5)), set())

    def assertIsMinMaxHeap(self, heap):
        for i, v in enumerate(heap._values[:heap._length]):
            if heap_level(i)%2:
                # Max
                assert_ = self.assertGreaterEqual
            else:
                assert_ = self.assertLessEqual
            for c in heap._descendants(i):
                assert_(v.priority, heap._values[c].priority)

    def assertLookupIsConsistent(self, heap):
        for k, i in heap._lookup.items():
            self.assertEqual(heap._values[i].value, k)
            self.assertEqual(heap._priorities[k], heap._values[i].priority)

    def test_construction(self):
        heap = MinMaxHeap(self.example_data)
        self.assertIsMinMaxHeap(heap)
        self.assertEqual(heap._length, len(self.example_data))
        self.assertEqual(set(heap._lookup), set(self.example_data))
        self.assertEqual(set(heap._priorities), set(self.example_data))
        self.assertLookupIsConsistent(heap)

    def test_bool(self):
        self.assertTrue(MinMaxHeap(self.example_data))
        self.assertFalse(MinMaxHeap())

    def test_pop_min(self):
        heap = MinMaxHeap(self.example_data)
        min_elem = min(self.example_data)
        self.assertEqual(
            min_elem,
            heap.pop_min().value
        )
        self.assertIsMinMaxHeap(heap)
        self.assertFalse(min_elem in heap._lookup)
        self.assertFalse(min_elem in heap._priorities)
        self.assertEqual(heap._length, len(self.example_data) - 1)
        self.assertLookupIsConsistent(heap)

    def test_pop_max(self):
        heap = MinMaxHeap(self.example_data)
        max_elem = max(self.example_data)
        self.assertEqual(
            max_elem,
            heap.pop_max().value
        )
        self.assertIsMinMaxHeap(heap)
        self.assertFalse(max_elem in heap._lookup)
        self.assertFalse(max_elem in heap._priorities)
        self.assertEqual(heap._length, len(self.example_data) - 1)
        self.assertLookupIsConsistent(heap)

    def test_heapsort_asc(self):
        self.assertEqual(
            list(sorted(self.example_data)),
            list(MinMaxHeap(self.example_data).heapsort_asc())
        )

    def test_heapsort_desc(self):
        self.assertEqual(
            list(sorted(self.example_data, reverse=True)),
            list(MinMaxHeap(self.example_data).heapsort_desc())
        )

    def test_add(self):
        heap = MinMaxHeap(self.example_data)
        heap.add(2)
        self.assertTrue(2 in heap._lookup)
        self.assertTrue(2 in heap._priorities)
        self.assertEqual(heap._priorities[2], 2)
        # from IPython import embed
        # embed()
        self.assertIsMinMaxHeap(heap)
        self.assertLookupIsConsistent(heap)
        self.assertEqual(heap._length, len(self.example_data) + 1)
        # print("b")
        h2 = MinMaxHeap([1, 5, 3, 4])
        h2.add(0)
        self.assertIsMinMaxHeap(h2)

    def test_delete_value(self):
        heap = MinMaxHeap(self.example_data)
        heap.delete_value(3)
        self.assertFalse(3 in heap._lookup)
        self.assertFalse(3 in heap._lookup)
        self.assertIsMinMaxHeap(heap)
        self.assertLookupIsConsistent(heap)
        self.assertEqual(heap._length, len(self.example_data) - 1)
        del heap[14]
        self.assertFalse(14 in heap._lookup)
        self.assertFalse(14 in heap._lookup)
        self.assertIsMinMaxHeap(heap)
        self.assertLookupIsConsistent(heap)
        self.assertEqual(heap._length, len(self.example_data) - 2)
        heap = MinMaxHeap(self.data2)
        del heap[14]
        self.assertIsMinMaxHeap(heap)


    def test_decrease_priority(self):
        # Min level.
        heap = MinMaxHeap(self.example_data)
        self.assertEqual(heap_level(heap._lookup[3])%2, 0)
        heap[3] = -0.5
        self.assertTrue(3 in heap._lookup)
        self.assertTrue(3 in heap._priorities)
        self.assertIsMinMaxHeap(heap)
        self.assertLookupIsConsistent(heap)
        self.assertEqual(heap.pop_min().value, -1)
        self.assertEqual(heap.pop_min().value, 3)
        self.assertEqual(heap.pop_min().value, 0)
        # Max level.
        heap = MinMaxHeap(self.example_data)
        self.assertEqual(heap_level(heap._lookup[55])%2, 1)
        heap[55] = 0.5
        self.assertTrue(3 in heap._lookup)
        self.assertTrue(3 in heap._priorities)
        self.assertIsMinMaxHeap(heap)
        self.assertLookupIsConsistent(heap)
        self.assertEqual(heap.pop_min().value, -1)
        self.assertEqual(heap.pop_min().value, 0)
        self.assertEqual(heap.pop_min().value, 55)

    def test_increase_priority(self):
        # Min level.
        heap = MinMaxHeap(self.example_data)
        self.assertEqual(heap_level(heap._lookup[3])%2, 0)
        heap[3] = 80
        self.assertTrue(3 in heap._lookup)
        self.assertTrue(3 in heap._priorities)
        self.assertIsMinMaxHeap(heap)
        self.assertLookupIsConsistent(heap)
        # from IPython import embed
        # embed()
        self.assertEqual(heap.pop_max_value(), 91)
        self.assertEqual(heap.pop_max_value(), 3)

    