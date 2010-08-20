import unittest

from flow_expression_id import FlowExpressionId, FeiException 

class TestFlowExpressionId(unittest.TestCase):

    def test_init(self):
        self.assertRaises(FeiException, 
                          FlowExpressionId,"foo", "bar", "1x_2_3")

    def test_storage_id(self):
        fei = FlowExpressionId("foo", "bar", "1_2_3")
        self.assertEquals("1_2_3!bar!foo", fei.storage_id)

    def test_child_id(self):
        fei = FlowExpressionId("foo", "bar", "1_2_3")
        self.assertEquals(3, fei.child_id)
        
        

if __name__ == "__main__":
    unittest.main()
