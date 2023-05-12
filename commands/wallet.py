import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *

class Wallet(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wallet(self, ctx):
        current_wallet = get_user_wallet(ctx.author.id)
        embed = discord.Embed(title= "", description= "Time: **"+give_current_time(True, True, True)+"**", color= discord.Color.from_rgb(231,225,212))
        embed.add_field(name="**Current Wallet:**", value="Your current wallet is: **"+ str(current_wallet)+"** MP")
        await ctx.send(embed = embed)


async def setup(client):
    await client.add_cog(Wallet(client))