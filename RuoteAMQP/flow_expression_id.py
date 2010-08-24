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

class FeiException(Exception):
    pass

from expression_id import expression_id_factory

class FlowExpressionId(object):
    """
    The FlowExpressionId (fei for short) is an process expression identifier.
    Each expression when instantiated gets a unique fei.
    
    Feis are also used in workitems, where the fei is the fei of the
    [participant] expression that emitted the workitem.
    
    Feis can thus indicate the position of a workitem in a process tree.
    """

    def __init__(self, wfid, sub_wfid, expid, engine_id = None): 
        """
        @type wfid: C{string}
        @param wfid: workflow instance id, 
                     the identifier for the process instance

        @type sub_wfid: C{string}
        @param sub_wfid: the identifier for the 
                      sub process within the main instance

        @type expid: C{string} of form '^\d{0,2}%s\d{0,2}%s\d{0,2}$'
        @param expid: the expression id, where in the process tree

        @type engine_id: string
        @param engine_id:  only relevant in multi engine scenarii 
        """
        self._wfid = wfid
        self._sub_wfid = sub_wfid 
        self._expid = expression_id_factory(expid)  
        self._engine_id = engine_id

    @property
    def wfid(self):
        """
        @rtype: C{string}
        @return: The wfid
        """
        return self._wfid

    @property
    def sub_wfid(self):
        """
        @rtype: C{string}
        @return: The sub_wfid
        """
        return self._sub_wfid

    @property 
    def expid(self):
        """
        @rtype: C{string}
        @return: The sub_wfid in form '^\d{0,2}%s\d{0,2}%s\d{0,2}$'
        """
        return str(self._expid)

    @property
    def engine_id(self):
        """
        @rtype: C{string}
        @return: The engine_id
        """
        return self._engine_id

    @property 
    def storage_id(self):
        """
        @rtype: C(string)
        @return: The storage id
        """
        return "%s!%s!%s" % (self.expid, 
                             self.sub_wfid, 
                             self.wfid)

    @property
    def child_id(self):
        """
        @rtype: C{int}
        @return: The last number in the expid
        """
        return self._expid.child_id

    def is_direct_child(self, fei):
        """
        @rtype: C{bool}
        @return: Is this FEI a child of the fei passed 
        """
        ret_val = False
        if all([(getattr(self, prop) == getattr(fei, prop)) 
                for prop in [ "sub_wfid", "wfid", "engine_id" ]]):
            ret_val =  (self._expid.parent_id == fei._expid)
        return ret_val
