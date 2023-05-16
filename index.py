import os, discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncio, glob
from discord import app_commands
from lib.config import *



#------------------------------------ Custom functions ---------------------------------------

def find_invite_by_code(invite_list, code):

    # Simply looping through each invite in an
    # invite list which we will get using guild.invites()
    for inv in invite_list:
        # Check if the invite code in this element
        # of the list is the one we're looking for
        if inv.code == code:   
            # If it is, we return it.   
            return inv

#------------------------------------ Loading modules ----------------------------------------
intents = discord.Intents.all()
load_dotenv()

#--------------------------------- Define variables ------------------------------------------
TOKEN = os.getenv('TOKEN')

#---------------------------------- Start server ---------------------------------------------


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix= commands.when_mentioned_or("-"), intents = intents)

    async def on_ready(self):


        # Getting all invite guilds that exists


        # Checking for slash keys and logging information
        slash = await self.tree.sync()
        refresh_member_list.start()
        print(f"Logged in as {self.user.name}")


    async def setup_hook(self):
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                if filename[:-3] != "init":
                    await self.load_extension(f"commands.{filename[:-3]}")
                    print(f"{filename[:-3]} has been loaded as command!")

        for filename in os.listdir("./events"):
            if filename.endswith(".py"):
                if filename[:-3] != "init":
                    await self.load_extension(f"events.{filename[:-3]}")
                    print(f"{filename[:-3]} has been loaded as event!")




#------------------------------------------------------- tasks
@tasks.loop(minutes= 1)
async def refresh_member_list():
    pass
    for guild in client.guilds:
        for member in guild.members:
            if not member.bot:
                if not is_member_exists(member.id):
                    payload = {
                        "name" : member.id,
                        "avatar": str(member.avatar),
                        "wallet": 0,
                        "level": 0,
                        "boost": False,
                        "voice-timer": 0,
                        "xp": 0,
                        "premium": False,
                        "premium-date": 0,
                        "invites": []
                    }
                    save_member(payload)
                    for role in guild.roles:
                        if role in member.roles:
                            if str(role.name).find("〆") == 0:
                                options = {"name": member.id, "border-color": str(role.color), "user-color-id": role.id, "user-color": str(role.color)}
                                save_member_options(options)




client = Client()

client.remove_command("help")


client.run(TOKEN)
