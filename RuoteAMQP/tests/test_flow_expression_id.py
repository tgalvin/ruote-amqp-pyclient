import unittest

from expression_id import ExpressionId
from flow_expression_id import FlowExpressionId, FeiException 

class TestFlowExpressionId(unittest.TestCase):

    def setUp(self):
        expression_id = ExpressionId(1, 2, 3)
        self.fei = FlowExpressionId("foo", 
                                    "bar", 
                                    expression_id, 
                                    "baz")

    def test_properties(self):
        self.assertEquals("foo", self.fei.wfid)
        self.assertEquals("bar", self.fei.sub_wfid)
        self.assertEquals("1_2_3", self.fei.expid)
        self.assertEquals("baz", self.fei.engine_id) 

    def test_storage_id(self):
        self.assertEquals("1_2_3!bar!foo", self.fei.storage_id)

    def test_child_id(self):
        self.assertEquals(3, self.fei.child_id)

    def test_is_direct_child(self):
        expression_id = ExpressionId(1, 2, 3)
        fei_2 = FlowExpressionId("not_foo", 
                                    "bar", 
                                    expression_id, 
                                    "baz")
        self.assertFalse(self.fei.is_direct_child(fei_2))


        expression_id = ExpressionId(1, 2)
        fei_3 = FlowExpressionId("foo", 
                                 "bar", 
                                 expression_id, 
                                 "baz")
        self.assertTrue(self.fei.is_direct_child(fei_3))
                
       



if __name__ == "__main__":
    unittest.main()