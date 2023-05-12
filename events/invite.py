import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from events.init import *


#--------------------- Define Variables
INVITE_CHANNEL = os.getenv('INVITE_LOG_CHANNEL')


class Invite(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        channel = self.client.get_channel(1093496503630311516)
        # -------------------------- Creating the embeds
        embed = discord.Embed(title="invite tracker", description="An invite link has been created!", color = discord.Colour.from_str("#19AFC1"))
        embed.add_field(name = "Username", value= invite.inviter.mention, inline=False)
        embed.add_field(name = "Code", value= invite.code, inline=True)
        embed.add_field(name = "URL", value= invite.url, inline=False)
        embed.add_field(name = "Max using count", value= invite.max_uses, inline=True)
        embed.add_field(name = "Max validation time", value= f"{invite.max_age / 3600} H", inline=False)

        #----------------------------------- Sending data to database
        payload = {"user": invite.inviter.id, "code": invite.code, "validation-time": invite.max_age, "created-time": time.time(), "max-using": invite.max_uses}
        add_inviter_info(payload)

        await channel.send(embed = embed)
        
        
async def setup(client):
    await client.add_cog(Invite(client))