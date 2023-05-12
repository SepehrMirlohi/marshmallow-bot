import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from events.init import *


class Voice(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.Cog.listener()
    #Updating scores and timers
    async def on_voice_state_update(self, member, before, after):
        if after.channel == None:
            calculate_time(member.id)
        if before.channel == None:
            save_time(member.id)

    # Creating voice channels

        member_list = []
        bot_list = []
        text_channel = self.client.get_channel(1018134189373136939)
        if before.channel == None: 
            
            if int(after.channel.id) == 1018477653440864296:
                
                if not is_private_user_exists(member.id):
                    for guild in self.client.guilds:
                        for category in guild.categories:
                            if int(category.id) == 1018477346996617267:
                                
                                channel = await guild.create_voice_channel(str(member.name)+"'s Voice", category = category)
                
                                await member.move_to(channel)
                                make_private_user(member.id, channel.id)
                else:
                    for guild in self.client.guilds:
                        for category in guild.categories:
                            if int(category.id) == 1018477346996617267:
                                count = change_private_user_count(member.id)
                                channel = await guild.create_voice_channel(str(member.name)+f"'s Voice {count}", category = category)
                                await member.move_to(channel)
                                change_private_user_channels(member.id, channel.id)
                                

                        
        if after.channel == None:
            del_channel_id = int(before.channel.id)
            if is_private_channel_exist(del_channel_id):

                del_channel = self.client.get_channel(del_channel_id)
                for check in del_channel.members:
                    if check.bot:
                        bot_list.append(check.name)
                    else: 
                        member_list.append(check.name)
                
                if not member_list and not bot_list:
                    await del_channel.delete()
                    del_private_info(member.id ,del_channel_id)

                if not member_list and bot_list:
                    await del_channel.delete()
                    del_private_info(member.id ,del_channel_id)
        if before.channel and after.channel:
            
            if int(before.channel.id) != int(after.channel.id):
                if int(after.channel.id) == 1018477653440864296:
                    if not is_private_user_exists(member.id):
                        for guild in self.client.guilds:
                            for category in guild.categories:
                                if int(category.id) == 1018477346996617267:
                                    channel = await guild.create_voice_channel(str(member.name)+"'s Voice", category = category)
                    
                                    await member.move_to(channel)
                                    make_private_user(member.id, channel.id)
                    else:
                        for guild in self.client.guilds:
                            for category in guild.categories:
                                if int(category.id) == 1018477346996617267:
                                    count = change_private_user_count(member.id)
                                    channel = await guild.create_voice_channel(str(member.name)+f"'s Voice {count}", category = category)
                                    await member.move_to(channel)
                                    change_private_user_channels(member.id, channel.id)
                del_channel_id = int(before.channel.id)
                if is_private_channel_exist(del_channel_id):        
                    if int(before.channel.id) == del_channel_id:

                        del_channel = self.client.get_channel(del_channel_id)
                        for check in del_channel.members:
                            if check.bot:
                                bot_list.append(check.name)
                            else: 
                                member_list.append(check.name)
                        
                        if not member_list and not bot_list:
                            await del_channel.delete()
                            del_private_info(member.id, del_channel_id)

                        if not member_list and bot_list:
                            await del_channel.delete()
                            del_private_info(member.id, del_channel_id)



        


async def setup(client):
    await client.add_cog(Voice(client))