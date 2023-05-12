import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from events.init import *

class Message(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not str(message.content).startswith("-") and not str(message.content).startswith("http"):
                    
                point_amount = len(message.content)
                save_chat_points(message.author.id, int(point_amount))
    

async def setup(client):
    await client.add_cog(Message(client))