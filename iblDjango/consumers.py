# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from iblDjango.processers import run_flow
from tutor.tutor import TutorClient


class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'ibl_education'  # Change this to your room/group name

        # Validate the token
        try:
            token_key = self.scope['query_string'].decode().split('=')[1]
            self.user = await self.get_user(token_key)
        except (Token.DoesNotExist, IndexError):
            self.user = AnonymousUser()

        if not self.user.is_authenticated:
            await self.close()
            return

        # Join room/group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room/group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Receive message from WebSocket
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message'] if "message" in text_data_json else None
            tutor = text_data_json["tutor"] if "tutor" in text_data_json else None
        
            # Broadcast message to room/group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message' if message else "tutor_input",
                    'message': message if message else tutor
                }
            )
        except json.decoder.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'message': "invalid input"
            }))
       

    async def tutor_input(self, event):
        message = event['message']
        client = TutorClient()
        courses = client.get_courses()
        await self.send(text_data=json.dumps({
                'courses': courses
            }))


    async def chat_message(self, event):
        message = event['message']
        inputs = {"input": message}
        response = run_flow(inputs).get("result", None)
        if response is not None:
            await self.send(text_data=json.dumps({
                'message': response.get("response")
            }))

    @database_sync_to_async
    def get_user(self, token_key):
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()
