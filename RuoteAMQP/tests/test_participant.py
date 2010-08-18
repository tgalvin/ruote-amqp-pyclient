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
        class MessageStub:
             body = json.dumps({'fei': "foo", 'fields': fields})
        participant.workitem_callback(MessageStub())
        self.assertEquals("foo", participant.workitem._fei._h)

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
            self.assertEquals("bar", json.loads(message.body))
        self.channel.basic_consume(queue = "bar", 
                                   callback = test_cb)
       
    def test_reply_to_engine(self):
        self._amqp()
        participant = Participant("bar", "localhost", 
                                  "guest", "guest", "/")
        class WorkitemStub:
             def to_h(self):
                 return "bar" 
        participant.workitem = WorkitemStub()
        participant.reply_to_engine()        
        self.channel.wait()


if __name__ == "__main__":
    unittest.main()
