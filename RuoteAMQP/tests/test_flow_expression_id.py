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

from expression_id import ExpressionId
from flow_expression_id import FlowExpressionId, FeiException 

class TestFlowExpressionId(unittest.TestCase):

    def setUp(self):
        expression_id = "1_2_3"
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
        expression_id = "1_2_3"
        fei_2 = FlowExpressionId("not_foo", 
                                    "bar", 
                                    expression_id, 
                                    "baz")
        self.assertFalse(self.fei.is_direct_child(fei_2))


        expression_id = "1_2"
        fei_3 = FlowExpressionId("foo", 
                                 "bar", 
                                 expression_id, 
                                 "baz")
        self.assertTrue(self.fei.is_direct_child(fei_3))
                
       



if __name__ == "__main__":
    unittest.main()
