import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Invites(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def giveInvites(self, ctx):
        embed = discord.Embed(title= "Invite Tracker", description= "You can see the list of all invite links that still exists!", color = discord.Colour.from_str("#1970C1"))
        list_of_invites = give_invites_list()
        counter = 3
        for invite in list_of_invites:
            if counter % 2 == 0:
                status = True
            else:
                status = False
            counter += 1
            for guild in self.client.guilds:
                for invites in await guild.invites():
                    if str(invites.code) == str(invite['code']): 
                        time_left = invite['validation-time'] - (time.time() - invite['created-time'])
                        user = discord.utils.get(ctx.guild.members, id = invite['user'])
                        embed.add_field(name = user.name, value = f'''**Max using count**: {invite['max-using']}  
                        **Uses times:** {invites.uses}
                        **Validation time left**: {int(time_left/60)} min 
                        **Code**: {invite['code']}
                        ''', inline = status)
        
        await ctx.send(embed = embed)

async def setup(client):
    await client.add_cog(Invites(client))