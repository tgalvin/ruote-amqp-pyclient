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

import simplejson as json

from flow_expression_id import FlowExpressionId
from fields import Fields

####################################
# KEYS 
###################################

FEI = 'fei'
FIELDS = 'fields'
PARTICIPANT_NAME = 'participant_name'

WFID = 'wfid'
SUB_WFID = 'sub_wfid'
EXPID = 'expid'
ENGINE_ID = 'engine_id'

RESULT = '__result__'
TIMED_OUT = '__timed_out__'
ERROR = '__error__'
DISPATCHED_AT = 'dispatched_at'
PARAMS = 'params'
FORGET = 'forget'

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
    fei = FlowExpressionId(fei_dict[WFID],
                           fei_dict[SUB_WFID],
                           fei_dict[EXPID],
                           fei_dict.get(ENGINE_ID, None))
    return fei


def fields_factory(fields_dict):
    """
    @type result: C{dict}
    @param result: A dictionary containing the field attributes  

    @rtype result: C{Fields}
    @rparam result: The Fields
    """
    result = fields_dict[RESULT]
    timed_out = fields_dict[TIMED_OUT]
    error = fields_dict[ERROR]
    dispatched_at = fields_dict[DISPATCHED_AT]
    forget = fields_dict[PARAMS][FORGET]
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
        self.fei = fei_factory(message_dict[FEI])
        self.fields = fields_factory(message_dict[FIELDS])
        self.participant_name = message_dict[PARTICIPANT_NAME]

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

    @property 
    def to_dict(self):
        """
        @type parameters: C{dict]
        @param parameters: A dictionary representation of the data structure
        """
        params_dict = {FORGET : self.parameters.forget}
        fields_dict = {RESULT : self.result,
                       TIMED_OUT : self.timed_out,
                       ERROR : self.error,
                       DISPATCHED_AT : self.dispatch_at,
                       PARAMS : params_dict} 
        fei_dict = {WFID : self.fei.wfid,
                    SUB_WFID : self.fei.sub_wfid,
                    EXPID : self.fei.expid,
                    ENGINE_ID : self.fei.engine_id}
        return {FEI : fei_dict,
                FIELDS : fields_dict,
                PARTICIPANT_NAME : self.participant_name}
       
