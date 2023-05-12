import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title = "Shop", description = "", color= discord.Color.from_rgb(231,225,212))
        embed.add_field(name = "Forgive us!", value="This command is still in progress")

        await ctx.send(embed =embed)


async def setup(client):
    await client.add_cog(Shop(client))