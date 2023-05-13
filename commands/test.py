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

        btn = Button(label="test", custom_id="test-1",style=discord.ButtonStyle.green)

        async def callback(interaction):
            await ctx.send(interaction.data['custom_id'])
        btn.callback = callback
        view = View()
        view.add_item(btn)
        await ctx.send(view = view)
        




async def setup(client):
    await client.add_cog(Test(client))        