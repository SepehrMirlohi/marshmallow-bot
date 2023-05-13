import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from events.init import *

class Member(commands.Cog) :

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(1093807083792633866)
        public_channel = self.client.get_channel(1018197496222187701)
        # ---------------------- Give the member default roles
        if not member.bot: 
            for guild in self.client.guilds:
                for role in guild.roles:
                    for d_role in give_default_roles():
                        if role.id == d_role:
                            await member.add_roles(role)

        # ---------------------------- Detecting invite
        # for guild in self.client.guilds:
        #     for invite in await guild.invites():'

        


        # ------------------------- Give a log for that member
        if not member.bot:
            log_embed = discord.Embed(title="Member Joined", description="You can see the member status here!", color=discord.Colour.from_str("#19C15B"))
            log_embed.add_field(name = "", value=f"**Username**: {member.mention}", inline=False)

            await channel.send(embed = log_embed)


        if not member.bot:
            log_embed = discord.Embed(title="Member Joined", description="Hey " + member.mention + " ,Welcome to our server!", color=discord.Colour.from_str("#E4D70C"))
            log_embed.add_field(name = "", value = "First of first you need to know our laws and services then check them as soon as you can!", inline = True)
            log_embed.set_footer(text = "Marshmallow Moderation")
            log_embed.set_image(url = "https://s8.uupload.ir/files/slider-banner-programming-image-_y69.jpg")

            await public_channel.send(embed = log_embed)
        #----------------------------------- Give inviter invite model
        # Getting the invites before the user joining
        # from our cache for this specific guild

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            update_boost_status(before.id, True)
        elif after.premium_since is None and before.premium_since is not None:
            update_boost_status(before.id, False)



async def setup(client):
    await client.add_cog(Member(client))