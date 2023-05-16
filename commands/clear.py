import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="clear", description = "clear amount of messages")
    @commands.has_any_role(1018134791943635015, 1098919905782419600)
    @app_commands.describe(amount = "amount of clearing")
    async def clear(self, interaction: discord.Interaction, amount: int, member: discord.Member = None):
        await interaction.response.defer(ephemeral= True)
        channel = interaction.channel
        embed= discord.Embed(title='', description='', color=discord.Color.from_rgb(231,225,212))
        embed.add_field(name="**Clear Warn**", value=f"**{str(amount)}** was amount of cleaning!")
        if amount > 50:
            amount = 50
        def check_(m):
            return m.author == member
        if not member:
            await channel.purge(limit=amount)
        else:
            await channel.purge(limit=amount,check=check_)
        await channel.send(embed= embed)
        await asyncio.sleep(3)
        await channel.purge(limit = 1)
        await interaction.followup.send("End of process")
        
        
        

async def setup(client):
    await client.add_cog(Clear(client))