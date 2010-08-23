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

import simplejson as json

from flow_expression_id import FlowExpressionId
from fields import Fields


########################################
# Factories
#######################################

# Convert dictionaries to Classes

def fei_factory(fei_dict):
    """
    @type result: C{dict}
    @param result: A dictionary containing the fei attributes  

    @rtype result: C{FlowExpressionId}
    @rparam result: The FlowExpressionId
    """
    fei = FlowExpressionId(fei_dict['wfid'],
                           fei_dict['sub_wfid'],
                           fei_dict['expid'],
                           fei_dict.get('engine_id', None))
    return fei


def fields_factory(fields_dict):
    """
    @type result: C{dict}
    @param result: A dictionary containing the field attributes  

    @rtype result: C{Fields}
    @rparam result: The Fields
    """
    result = fields_dict['__result__']
    timed_out = fields_dict['__timed_out__']
    error = fields_dict['__error__']
    dispatched_at = fields_dict['dispatched_at']
    forget = fields_dict['params']['forget']
    fields = Fields(result, timed_out, error, dispatched_at, forget)
    return fields

######################################
# Workitem
######################################

class Workitem(object):
    """
    A workitem can be thought of an "execution token", 
    but with a payload (fields).
    """

    def __init__(self, message):
        """
        @type message: C{json}
        @param message: A jsonified dict  
        """
        message_dict = json.loads(message)
        self._message_dict = message_dict 
        self.fei = fei_factory(message_dict['fei'])
        self.fields = fields_factory(message_dict['fields'])
        self.participant_name = message_dict['participant_name']

    #################################
    # DELEGATES 
    #################################

    # FIXME do we really want to retain these?

    @property
    def sid(self):
        """
        @type sid: C{string}
        @param sid: The storage id
        """
        return self.fei.storage_id

    @property 
    def wfid(self):
        """
        @type wfid: C{string}
        @param wfid: The workflow id
        """
        return self.fei.wfid

    @property 
    def result(self):
        """
        @type result: C{bool}
        @param result: The result
        """
        return self.fields.__result__

    @property 
    def dispatch_at(self):
        """
        @type dispatch_at: C{string}
        @param dispatch_at: The dispatch location
        """
        
        return self.fields.dispatched_at

    @property 
    def forget(self):
        """
        @type forget: C{string}
        @param forget: FIXME
        """
        return self.fields.parameters.forget

    @property 
    def timed_out(self):
        """
        @type timed_out: C{bool}
        @param timed_out: Has it timed out
        """
        return self.fields.__timed_out__

    @property 
    def error(self):
        """
        @type error: C{string}
        @param error: The workflow id
        """
        return self.fields.__error__

    @property 
    def parameters(self):
        """
        @type parameters: L{Parameters]
        @param parameters: The Ruote Parameters
        """
        return self.fields.parameters
