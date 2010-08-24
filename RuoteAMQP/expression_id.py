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

#This is a WIP to clarify the interfaces 
#And drive discussion

#Based on original work:
# 
#http://github.com/jmettraux/ruote/tree/ruote2.1/lib/ruote
#http://github.com/lbt/ruote-amqp-pyclient/tree/master/RuoteAMQP/

CHILD_SEP = "_"

def expression_id_factory(expid):
    """
    @type expid: C{string} of form '^\d{0,2}%s\d{0,2}%s\d{0,2}$'
    @param expid: The expression id as a string
    
    @rtype expid: L{ExpressionId}
    @rtype expid: The ExpressionId object
    """
    expid_list = [int(arg) for arg in expid.split(CHILD_SEP)]
    return ExpressionId(expid_list)

class ExpressionId(object):
    """
    The ExpressionId
    FIXME more documentation
    """
    def __init__(self, expid_list):
        """
        @type args: C{list} of C{int}
        @param args: Integers representing the Expression Id
        """

        self._expid_list = expid_list

    def __iter__(self):
        """
        @ytype: C{int}
        @yield: The arguments that make up the ExpressionId 
        """
        for arg in self._expid_list: yield int(arg)

    def __str__(self):
        """
        @rtype: C{string}
        @return:form '^\d{0,2}%s\d{0,2}%s\d{0,2}$'
        """
        return CHILD_SEP.join([str(arg) for arg in self])

    @property 
    def child_id(self):
        """
        @rtype: C{int}
        @return: The child id
        """
        #TODO: The logic here needs verifying
        return int(self._expid_list[-1]) 

    @property 
    def parent_id(self):
        """
        @rtype: L{ExpressionId}
        @return: The ExpressionId of the parent
        """
        #TODO: The logic here needs verifying
        return ExpressionId(self._expid_list[:-1])

    def __eq__(self, expression_id):
        """
        @rtype: C{bool}
        @return: Are the ExpressionIds equal
        """
        return (self._expid_list == expression_id._expid_list)
