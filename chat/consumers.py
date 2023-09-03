import json

from asgiref.sync import async_to_sync
#from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

#class ChatConsumer(WebsocketConsumer):
class ChatConsumer(AsyncWebsocketConsumer):
    #def connect(self):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group (Synchronous)
        # async_to_sync(self.channel_layer.group_add)(
            # self.room_group_name, self.channel_name
        # )
        # self.accept()

        # Join room group (Asynchronous)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    #def disconnect(self, close_code):
    async def disconnect(self, close_code):
        # Leave room group (Synchronous)
        # async_to_sync(self.channel_layer.group_discard)(
            # self.room_group_name, self.channel_name
        # )

        # Leave room group (Asynchronous)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    # Receive message from WebSocket
    #def receive(self, text_data):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group (Synchronous)
        # async_to_sync(self.channel_layer.group_send)(
            # self.room_group_name, {"type": "chat_message", "message": message}
        # )

        # Send message to room group (Asynchronous)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        
    # Receive message from room group
    #def chat_message(self, event):
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket (Synchronous)
        # self.send(text_data=json.dumps({"message": message}))
        
        # Send message to WebSocket (Asynchronous)
        await self.send(text_data=json.dumps({"message": message}))

