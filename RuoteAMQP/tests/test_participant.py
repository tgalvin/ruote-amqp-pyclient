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

from amqplib import client_0_8 as amqp

import json

from participant import Participant

def _init_queue(channel, queue, exchange, routing_key):
    channel.queue_declare(queue = queue, 
                          durable = False, 
                          exclusive = False,
                          auto_delete=True)
    channel.exchange_declare(exchange = exchange,
                             type = 'direct',
                             durable = False,
                             auto_delete = True)
    channel.queue_bind(queue = queue,
                       exchange = exchange,
                       routing_key = routing_key)

class TestParticipant(unittest.TestCase):

    def test_amqp_message_callback(self):
        participant = Participant("foo", "localhost", 
                                  "guest", "guest", "/")
        fields = {'params':{'forget':1}}
        fei_dict = {'expid': 'expid_value',
                    'wfid': 'wfid_value',
                    'sub_wfid': 'sub_wfid_value',
                    'engine_id': 'engine_id_value'}
        params_dict = {'forget': 'baz'}
        fields_dict = {'__result__': False,
                       '__timed_out__': True,
                       '__error__': 'err',
                       'dispatched_at': 'bar',
                       'params': params_dict}


        class MessageStub:
             body = json.dumps({'fei': fei_dict, 
                               'fields': fields_dict,
                                'participant_name': "foo"})
        participant.workitem_callback(MessageStub())
        self.assertEquals("foo", participant.workitem.participant_name)

    def _amqp(self):
        connection = amqp.Connection(host = "localhost", 
                                     userid = "guest",
                                     password = "guest",
                                     virtual_host = "/", 
                                     insist = False)
        self.channel = connection.channel()
        _init_queue(self.channel, 
                    'bar', 
                    '',
                    'ruote_workitems')
        def test_cb(message):
            self.assertEquals({"foo" : "bar"}, json.loads(message.body))
        self.channel.basic_consume(queue = "bar", 
                                   callback = test_cb)
       
    def test_reply_to_engine(self):
        self._amqp()
        participant = Participant("bar", "localhost", 
                                  "guest", "guest", "/")
        class WorkitemStub:
            @property
            def to_dict(self):
                return {"foo" : "bar"} 
        participant.workitem = WorkitemStub()
        participant.reply_to_engine()        
        self.channel.wait()


if __name__ == "__main__":
    unittest.main()
