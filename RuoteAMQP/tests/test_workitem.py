# ***** BEGIN LICENCE BLOCK *****
# This file is part of OTS
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: Mikko Makinen <mikko.al.makinen@nokia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
# ***** END LICENCE BLOCK *****

import unittest 

import json

from fields import Fields
from parameters import Parameters
from workitem import Workitem, FlowExpressionId, fei_factory, fields_factory

class TestWorkitem(unittest.TestCase):

    def test_fei_factory(self):
        fei_dict = {'expid': '1_2_3',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        fei = fei_factory(fei_dict)
        self.assertEquals('1_2_3', fei.expid)
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
        fei_dict = {'expid': '1_2_3',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        self.params_dict = {'forget': 'baz'}
        self.fields_dict = {'__result__': True, 
                            '__timed_out__': False,
                            '__error__': 'err',
                            'dispatched_at': 'bar',
                            'params': self.params_dict}
        self.all_dict = {'fei': fei_dict, 
                         'participant_name': "foo",
                         'fields': self.fields_dict}
        
        self.msg = json.dumps(self.all_dict)
        self.workitem = Workitem(self.msg)

    def test_sid(self):
        self.assertEquals("1_2_3!sub_wfid_value!wfid_value",
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

    def test_to_dict(self):
        self.assertEquals(self.all_dict, self.workitem.to_dict)

if __name__ == "__main__":
    unittest.main()
