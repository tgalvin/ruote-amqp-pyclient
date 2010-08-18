import unittest 

import json

from workitem import FlowExpressionId, Workitem

class TestFlowExpressionId(unittest.TestCase):

    def setUp(self):
        fei_dict = {'expid': 'expid_value',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        self.fe_id = FlowExpressionId(fei_dict)

    def test_ex_pid(self):
        self.assertEquals('expid_value', self.fe_id.expid())
    
    def test_wfid(self):
        self.assertEquals('wfid_value', self.fe_id.wfid())

    def test_sub_wfid(self):
        self.assertEquals('sub_wfid_value', self.fe_id.sub_wfid())

    def test_engine_id(self):
        self.assertEquals('engine_id_value', self.fe_id.engine_id())

    def test_to_storage_id(self):
        self.assertEquals("expid_value!sub_wfid_value!wfid_value",
                          self.fe_id.to_storage_id())

    def test_child_id(self):
        self.assertTrue(self.fe_id.child_id() is None)

        fei_dict = {'expid': 'expid_value_1',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        fe_id = FlowExpressionId(fei_dict)
        self.assertEquals(1, fe_id.child_id()) 

    def test_direct_child(self):
        #FIXME: Unsure of intent of the code
        pass

class TestWorkitem(unittest.TestCase):

    def setUp(self):
        fei_dict = {'expid': 'expid_value',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        #FIXME: Is there a link to a definition of these dictionarys?
        self.params_dict = {'forget': 'baz'}
        self.fields_dict = {'__result__': True, 
                            '__timed_out__': False,
                            '__error__': 'err',
                            'dispatched_at': 'bar',
                            'params': self.params_dict}
        self.foo_dict = {'fei': fei_dict, 
                         'participant_name': "foo",
                         'fields': self.fields_dict}
        
        self.msg = json.dumps(self.foo_dict)
        self.workitem = Workitem(self.msg)
        
    def test_to_h(self):
        self.assertEquals(self.foo_dict,
                          self.workitem.to_h())

    def test_sid(self):
        self.assertEquals("expid_value!sub_wfid_value!wfid_value",
                          self.workitem.sid())

    def test_wfid(self):
        self.assertEquals('wfid_value', self.workitem.wfid())

    def test_fei(self):
        self.assertTrue(isinstance(self.workitem.fei(), FlowExpressionId))

    def test_dup(self):
        pass

    def test_participant_name(self):
        self.assertTrue("foo", self.workitem.participant_name())

    def test_fields(self):
        self.assertTrue("bar", self.workitem.fields())

    def test_set_fields(self):
        self.assertRaises(TypeError, self.workitem.set_fields, 11)

    def test_result(self):
        self.assertTrue(self.workitem.result())

    def test_set_result(self):
        self.workitem.set_result(False)
        self.assertFalse(self.workitem.result())

    def test_dispatch_at(self):
        self.assertEquals("bar", self.workitem.dispatch_at())

    def test_forget(self):
        self.assertEquals("baz", self.workitem.forget())

    def test_eq(self):
        pass

    def test_ne(self):
        pass

    def test_hash(self):
        #TODO
        self.workitem.hash()

    def test_lookup(self):
        import sys
        std_out = sys.stdout 
        class StdOutStub:
            out = []
            def write(self, arg):
                self.out.append(arg)
        stub = StdOutStub()
        sys.stdout = stub
        import this
        sys.stdout = std_out
        print stub.out[0].split("\n")[-1]
        
    def test_lf(self):
        pass

    def test_set_field(self):
        pass

    def test_timed_out(self):
        self.assertFalse(self.workitem.timed_out())

    def test_error(self):
        self.assertEquals("err", self.workitem.error())

    def test_params(self):
        self.assertEquals({'forget': 'baz'},
                          self.workitem.params())

if __name__ == "__main__":
    unittest.main()
