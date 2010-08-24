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

from message_io import send, receive, WORKITEM_ROUTING_KEY
from workitem import Workitem

class TestMessageIO(unittest.TestCase):

    def setUp(self):
        fei_dict = {'expid': 'expid_value',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        params_dict = {'forget': 'baz'}
        fields_dict = {'__result__': True, 
                       '__timed_out__': False,
                       '__error__': 'err',
                       'dispatched_at': 'bar',
                       'params': params_dict}
        self.all_dict = {'fei': fei_dict, 
                    'participant_name': "foo",
                    'fields': fields_dict}

    def test_send(self):
        class ChannelStub:
            def basic_publish(self, msg, exchange, routing_key):
                self.msg = msg
                self.exchange = exchange
                self.routing_key = routing_key 
        channel = ChannelStub()
        send(channel, Workitem(json.dumps(self.all_dict)))
        msg = channel.msg
        self.assertEquals(self.all_dict, json.loads(msg.body))
        self.assertEquals('', channel.exchange)
        self.assertEquals(WORKITEM_ROUTING_KEY, channel.routing_key)

    def test_receive(self):        
        class MessageStub:
            body = json.dumps(self.all_dict)
        workitem = receive(MessageStub())
        self.assertEquals(self.all_dict, workitem.to_dict)

if __name__ == "__main__":
    unittest.main()
