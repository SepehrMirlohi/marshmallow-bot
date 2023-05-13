import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        counter = 1
        for guild in self.client.guilds:
            for role in guild.roles:
                if role.name.find('〆') != -1:
                    peyload = {'number': counter, 'color-id': role.id, "color-name": role.name}
                    counter += 1
                    add_colour_roles(peyload)

    @commands.command()
    async def test2(self, ctx):

        await ctx.send(dir(ctx.author))
        




async def setup(client):
    await client.add_cog(Test(client))        