import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(1018134791943635015, 1098919905782419600)
    async def Server(self, ctx):
        await ctx.send('This command will be ready soon! This command will help you to configure our server configs!')
    

async def setup(client):
    await client.add_cog(Server(client))