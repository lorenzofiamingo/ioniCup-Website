import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from skeleton.models import Match


class ScoreBoardConsumer(AsyncConsumer):
    async def websocket_connet(self, event):
        print("connected", event)

    async def websocket_receive(self, event):
        print("received", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)
