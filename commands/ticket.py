import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Ticket(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_any_role(1018134791943635015)
    async def ticket(self, ctx):
        # important variables ------------------------
        list_of_custom_btn = {}
        list_of_custom_view = {}

        # Embeds ---------------------------------
        ticket_menu_embed = discord.Embed(title= "Marshmallow Ticket System", description= "", color= discord.Colour.from_str("#F5B041"))
        ticket_menu_embed.add_field(name="normal ticket", value="You can answer your normal question or give us your suggestions!", inline=True)
        ticket_menu_embed.add_field(name="staff ticket", value="You can compelete a form and try to join in our staff team!", inline=True)
        ticket_menu_embed.set_footer(text="Marshmallow Moderation")
        #---------------------------------------------------------------- ||||

        public_embed = discord.Embed(title="Normal Ticket", description="", color=discord.Colour.from_str("#F7DC6F"))
        public_embed.add_field(name="", value="Here you can send a ticket after you sent your ticket hold on one of our admin will appear in your channel to help you!", inline=True)
        public_embed.set_footer(text="Marshmallow moderation")
       
       
        staff_embed = discord.Embed(title="Staff Ticket", description="", color=discord.Colour.from_str("#F7DC6F"))
        staff_embed.add_field(name="", value="If you wanted to join our staff team use this ticket and compelete the following fields!", inline=True)
        staff_embed.set_footer(text="Marshmallow moderation")

        def make_alert(ticket: int, member: str):
            admin_alert = discord.Embed(title=f"Ticket {ticket}", description=f"A member {member} has sent a ticket, open the chat and answer his/her questions!", color=discord.Colour.from_str("#F1C40F"))
            admin_alert.add_field(name="", value=f"Required roles: <@&1098919905782419600>", inline=False)
            return admin_alert



        # Buttons ----------------------------------
        menu_btn_staff = Button(label="Staff", style= discord.ButtonStyle.gray)
        menu_btn_public = Button(label="Normal", style=discord.ButtonStyle.gray)

        public_btn = Button(label = "Ticket", style= discord.ButtonStyle.gray)
        staff_btn = Button(label = "Ticket", style= discord.ButtonStyle.gray)

        def custom_btn(ticket: int):

            list_of_custom_btn[ticket] = Button(label = "Answer", custom_id=str(ticket),style=discord.ButtonStyle.green)

        
        async def callback_public(interaction):
            # user = interaction.user
            await interaction.response.edit_message(view = view_public, embed = public_embed)

        async def callback_staff(interaction):

            await interaction.response.edit_message(view = view_staff, embed = staff_embed)

        async def callback_staff_channel(interaction):
            pass

        async def callback_public_channel(interaction):
            await interaction.response.defer(ephemeral=True)
            user = interaction.user
            if not is_ticket_exists(user.id):
                    
                category = discord.utils.get(ctx.guild.categories, id = 1106835862114816052)
                admin_chat_channel = self.client.get_channel(1105546752645414944)
                ticket_num = get_current_ticket_id()

                # waitiong for an admin accept the ticket----
                custom_btn(ticket_num)
                # print()
                for button in list_of_custom_btn:
                    list_of_custom_btn[button].callback = admin_process

                await admin_chat_channel.send(embed = make_alert(ticket_num, user.name), view = create_custom_view(ticket_num))

                user = interaction.user
                for guild in self.client.guilds:
                    
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        user: discord.PermissionOverwrite(read_messages = True, send_messages=False)  
                    }
                    channel = await guild.create_text_channel("normal-ticket-" + str(get_current_ticket_id()), category = category, overwrites = overwrites)


                # admin = random.choice(get_list_of_admins())
                payload = {"id": get_current_ticket_id() ,"user-id": user.id, "username": user.name,"admin-name": "" ,"admin-id": 0, "log": "", "channel-id": channel.id, "deleted": False}
                save_ticket(payload)
                # await channel.set_permissions(user, read_messages=True, send_messages=False)
                # await channel.send(dir(channel))
            else:
                await user.send("You have a opened ticket!")

        async def admin_process(interaction):

            # define important variables
            # admin_log = ""
            # member_log = ""
            log = ""
            end_log_channel = self.client.get_channel(1018472547110617128)
            await interaction.response.defer(ephemeral=True)
            user = interaction.user
            ticket_id = interaction.data['custom_id']
            ticket_list = get_ticket(int(ticket_id))
            channel = self.client.get_channel(int(ticket_list['channel-id']))
            for guild in self.client.guilds:
                for member_choose in guild.members:
                    if member_choose.id == int(ticket_list['user-id']):
                        member = member_choose

            # handling errors and accesses --------------------------------
            access = False
            error = 0
            for role in user.roles:
                if role.id == 1098919905782419600:
                    if ticket_list['admin-id'] == 0:
                        if user.id != member.id:
                            access = True
                        else: 
                            error = 2
                    else:
                        error = 1
                    
                 

            if access:

                #define embeds ---------------------
                chat_alert = discord.Embed(title=f"{user.name} has opened your chatroom", description="We will take a log from your chats pleas be polite!", color=discord.Colour.from_str("#58D68D"))
                chat_alert.add_field(name="", value=f"{user.mention} After you answered his/her question close session with typing this sentence: `ticket close`", inline=False)
                chat_alert.set_footer(text=f"Admin name is {user.name}")

                end_chat_member = discord.Embed(title=f"Dear {member.name}", description="Your chatroom has been closed! \n Have fun hope you enjoyed our servieces", color = discord.Colour.from_str("#F5B041"))
                end_chat_user = discord.Embed(title=f"Dear {user.name}", description="Thanks for answer him/her questions, The chatroom has been closed by you", color = discord.Colour.from_str("#F5B041"))
                end_chat_log = discord.Embed(title=f"Ticket number {ticket_id} has been closed!", description=f"Related admin: {user.mention}", color= discord.Colour.from_str("#CB4335"))
                #Starting processes ---------------------------
                update_ticket(int(ticket_id), {"admin-id": user.id, "admin-name": user.name})
                await channel.send(embed = chat_alert)
                await channel.set_permissions(user, read_messages = True, send_messages=True)
                await channel.set_permissions(member, read_messages = True, send_messages=True)

                #Start taking log from chatroom
                while True:
                    def check(x):
                        return lambda x: x.channel == user.channel
                    
                    message = await self.client.wait_for("message", check = check, timeout= 3600)
                    if message.author == user:
                        if message.content == "ticket close":
                            await channel.delete()
                            await user.send(embed=end_chat_user)
                            await member.send(embed=end_chat_member)
                            await end_log_channel.send(embed = end_chat_log)
                            update_ticket(int(ticket_id), {"deleted": True})

                            break
                        else:
                            log = log +"//admin::"+ str(message.content)
                            
                    elif message.author == member:
                        log = log + "//member::" + str(message.content)

                update_ticket(int(ticket_id), {"log": log})
                

            else:
                if error == 0:
                    await interaction.channel.send("You don't required role!")
                elif error == 1:
                    await interaction.channel.send("An admin is already entered in this chatroom!")
                elif error == 2:
                    await interaction.channel.send("You can't answer your own ticket!")

        menu_btn_staff.callback = callback_staff
        menu_btn_public.callback = callback_public
        public_btn.callback = callback_public_channel
        staff_btn.callback = callback_staff_channel

      

        view = View()
        view.add_item(menu_btn_public)
        view.add_item(menu_btn_staff)

        view_public = View(timeout= None)
        view_public.add_item(public_btn)

        view_staff = View(timeout= None)
        view_staff.add_item(staff_btn)

        def create_custom_view(ticket: int):

            list_of_custom_view[ticket] = View(timeout= None)
            list_of_custom_view[ticket].add_item(list_of_custom_btn[ticket])
            return list_of_custom_view[ticket]

        await ctx.send(embed = ticket_menu_embed, view = view)





async def setup(client):
    await client.add_cog(Ticket(client))