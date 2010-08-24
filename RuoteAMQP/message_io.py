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

from amqplib import client_0_8 as amqp
from workitem import Workitem
import simplejson as json

#This is a WIP to clarify the interfaces 
#And drive discussion

#Based on original work:
# 
#http://github.com/jmettraux/ruote/tree/ruote2.1/lib/ruote
#http://github.com/lbt/ruote-amqp-pyclient/tree/master/RuoteAMQP/

WORKITEM_ROUTING_KEY = 'ruote_workitems'

def receive(msg):
    """
    @type msg: L{amqplib.client_0_8.basic_message.Message}
    @param msg: The AMQP message 
        
    @rtype workitem: L{Workitem}
    @rparam workitem: The ruote workitem
    """
    workitem = Workitem(msg.body)
    return workitem
       
def send(channel, workitem):
    """
    @type channel: L{amqplib.client_0_8.channel.Channel}
    @param channel: The AMQP channel 
        
    @type workitem: L{Workitem}
    @param workitem: The ruote workitem
    """
    msg = amqp.Message(json.dumps(workitem.to_dict))
    # delivery_mode=2 is persistent
    msg.properties["delivery_mode"] = 2 
    channel.basic_publish(msg, 
                          exchange='', 
                          routing_key = WORKITEM_ROUTING_KEY)
