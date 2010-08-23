import unittest 

import json

from workitem import Workitem, FlowExpressionId, Fields, Parameters, fei_factory, fields_factory

class TestWorkitem(unittest.TestCase):

    def test_fei_factory(self):
        fei_dict = {'expid': 'expid_value',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        fei = fei_factory(fei_dict)
        self.assertEquals('expid_value', fei.expid)
        self.assertEquals('wfid_value', fei.wfid)
        self.assertEquals('sub_wfid_value', fei.sub_wfid)
        self.assertEquals('engine_id_value', fei.engine_id)
        
    def test_fields_factory(self):
        params_dict = {'forget': 'baz'}
        fields_dict = {'__result__': False,
                       '__timed_out__': True,
                       '__error__': 'err',
                       'dispatched_at': 'bar',
                       'params': params_dict}
        fields = fields_factory(fields_dict)
        self.assertFalse(fields.__result__)
        self.assertTrue(fields.__timed_out__)
        self.assertEquals("err", fields.__error__)
        self.assertEquals("bar", fields.dispatched_at)
        self.assertEquals("baz", fields.parameters.forget)
        
    def setUp(self):
        fei_dict = {'expid': 'expid_value',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
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

    def test_sid(self):
        self.assertEquals("expid_value!sub_wfid_value!wfid_value",
                          self.workitem.sid)

    def test_wfid(self):
        self.assertEquals('wfid_value', self.workitem.wfid)

    def test_fei(self):
        self.assertTrue(isinstance(self.workitem.fei, FlowExpressionId))

    def test_participant_name(self):
        self.assertTrue("foo", self.workitem.participant_name)

    def test_fields(self):
        self.assertTrue(isinstance(self.workitem.fields, Fields))

    def test_result(self):
        self.assertTrue(self.workitem.result)

    def test_dispatch_at(self):
        self.assertEquals("bar", self.workitem.dispatch_at)

    def test_forget(self):
        self.assertEquals("baz", self.workitem.forget)

    def test_timed_out(self):
        self.assertFalse(self.workitem.timed_out)

    def test_error(self):
        self.assertEquals("err", self.workitem.error)

    def test_parameters(self):
        self.assertTrue(isinstance(self.workitem.parameters, Parameters))

if __name__ == "__main__":
    unittest.main()
