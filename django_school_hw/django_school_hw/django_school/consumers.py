import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class BidConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'all'
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        print('disconect')

    def receive(self, text_data, **kwargs):
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            'type': 'chat_message',
            'message': text_data
        })

    def chat_message(self, event):
        self.send(event['message'])