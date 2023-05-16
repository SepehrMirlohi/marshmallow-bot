import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class BirthDay(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(1018134791943635015, 1098919905782419600)
    async def play(self, ctx):
        channel = self.client.get_channel(1018479145442885662)
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio("../musics/phonk.mp3"))

async def setup(client):
    await client.add_cog(BirthDay(client))