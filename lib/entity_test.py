import unittest

from . import entity


class EntityTest(unittest.TestCase):
    def test_get_siblings(self):
        class A(entity.Entity):
            pass

        root = A(left=0, top=0)
        test = A(left=0, top=0)

        root.add_child(A(left=0, top=0))
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

    def test_global_position(self):
        class A(entity.Entity):
            pass

        test = A(left=20, top=30)

        parent = A(left=5, top=5)
        parent.add_child(test)

        root = A(left=10, top=10)
        root.add_child(parent)

        # "test" should inherit its position from its parent,
        # and that behavior should recurse to the root entity.
        self.assertEqual(test.get_left(), 35)
        self.assertEqual(test.get_top(), 45)
