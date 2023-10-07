import unittest

from . import entity

class EntityTest(unittest.TestCase):
    def test_get_siblings(self):
        class A(entity.Entity):
            pass

        root = A()
        test = A()

        root.add_child(A())
        root.add_child(test) 

        # "test" should not return as a sibling of itself
        self.assertNotIn(test, test.get_siblings())

        # "test" should remain a child of "root" even after we
        # asked for its siblings.
        # 
        # Depending on the implementation of get_siblings, it is
        # possible mistakes could be made which unintentionally remove
        # "test" from children.
        self.assertIn(test, root.get_children())
