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

from parameters import Parameters

class Fields(object):

    __result__ = False
    __timed_out__ = False
    __error__ = None

    def __init__(self, result, timed_out, error, dispatched_at, forget):
        """
        @type result: C{bool}
        @param result: The result 
                  
        @type timed_out: C{bool}
        @param timed_out: Did it timeout 
           
        @type error: C{string}
        @param error: The error message

        @type dispatched_at: string
        @param dispatched_at:  The dispatch location

        @type dispatched_at: string
        @param dispatched_at: The dispatch location

        @type forget: string
        @param forget: TODO        
        """
        self.__result__ = result
        self.__timed_out__ = timed_out
        self.__error__ = error
        self.dispatched_at = dispatched_at
        self.parameters = Parameters()
        self.parameters.forget = forget

