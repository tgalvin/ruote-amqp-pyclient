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

class ExpressionId(object):
    """
    The ExpressionId
    FIXME more documentation
    """

    CHILD_SEP = "_"

    def __init__(self, *args):
        """
        @type args: *{int}
        @param args: Integers representing the Expression Id
        """

        self.args = args

    def __iter__(self):
        """
        @ytype: C{int}
        @yield: The arguments that make up the ExpressionId 
        """
        for arg in self.args: yield int(arg)

    def __str__(self):
        """
        @rtype: C{string}
        @return:form '^\d{0,2}%s\d{0,2}%s\d{0,2}$'
        """
        return self.CHILD_SEP.join([str(arg) for arg in self])

    @property 
    def child_id(self):
        """
        @rtype: C{int}
        @return: The child id
        """
        return int(self.args[-1]) 

    @property 
    def parent_id(self):
        """
        @rtype: L{ExpressionId}
        @return: The ExpressionId of the parent
        """
        return ExpressionId(*self.args[:-1])

    def __eq__(self, expression_id):
        """
        @rtype: C{bool}
        @return: Are the ExpressionIds equal
        """
        return (self.args == expression_id.args)
