import unittest

from expression_id import ExpressionId

class TestExpressionId(unittest.TestCase):

    def test_str(self):
        self.assertEquals("1_2_3", str(ExpressionId(1,2,3)))

    def test_iter(self):
        self.assertEquals([1, 2, 3], list(ExpressionId(1,2,3)))

    def test_child_id(self):
        self.assertEquals(4, ExpressionId(1, 2, 3, 4).child_id)

    def test_parent_id(self):
        self.assertEquals("1_2_3", str(ExpressionId(1, 2, 3, 4).parent_id))

    def test_eq(self):
        expid_1 = ExpressionId(1, 2, 3)
        expid_2 = ExpressionId(1, 2, 3)
        self.assertEquals(expid_1, expid_2)
        expid_3 = ExpressionId(1, 2, 3, 4)
        self.assertFalse(expid_1 == expid_3) 

if __name__ == "__main__":
    unittest.main()
