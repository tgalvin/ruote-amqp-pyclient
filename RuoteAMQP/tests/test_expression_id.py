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

from expression_id import ExpressionId, expression_id_factory 

class TestExpressionId(unittest.TestCase):

    def test_expression_id_factory(self):
        expid = expression_id_factory("1_2_3_4")
        self.assertEquals([1,2,3,4], list(expid))
    
    def test_str(self):
        self.assertEquals("1_2_3", str(ExpressionId([1,2,3])))

    def test_iter(self):
        self.assertEquals([1, 2, 3], list(ExpressionId([1,2,3])))

    def test_child_id(self):
        self.assertEquals(4, ExpressionId([1, 2, 3, 4]).child_id)

    def test_parent_id(self):
        self.assertEquals("1_2_3", str(ExpressionId([1, 2, 3, 4]).parent_id))

    def test_eq(self):
        expid_1 = ExpressionId([1, 2, 3])
        expid_2 = ExpressionId([1, 2, 3])
        self.assertEquals(expid_1, expid_2)
        expid_3 = ExpressionId([1, 2, 3, 4])
        self.assertFalse(expid_1 == expid_3) 

if __name__ == "__main__":
    unittest.main()
