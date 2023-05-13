import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Security(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(1018134791943635015)
    async def admin(self, ctx):
        admin_role_id = 1098919905782419600
        for guild in self.client.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.id == admin_role_id:
                        peyload = {"admin-id": member.id, "ticket-answer": 0, "kick-list": [], "ban-list": [], "mute-list": []}
                        save_admin(peyload)
                        await ctx.send(f"Admin: {member.name} appended!")

async def setup(client):
    await client.add_cog(Security(client))