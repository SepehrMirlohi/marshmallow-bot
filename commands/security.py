import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Security(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(1018134791943635015, 1098919905782419600)
    async def Admin(self, ctx):
        # Embeds ------------------------------------------
        menu = discord.Embed(title="Admin", description=f"here dear {ctx.author.name}, some of useful options that will help you!", color=discord.Colour.from_str("#9B59B6"))
        menu.add_field(name="Get Log", value="This button will help you to take a log from a priavte channel that created in this server!", inline=False)
        menu.add_field(name="Admin list", value="Show you the list of admins and their permissions", inline=False)
        menu.add_field(name="Report", value="This one can help you to report something to Owners of the server", inline=False)

        def make_alert(name: str = None, text: str = None):
            alert_embed = discord.Embed(title=name, description=text, color= discord.Colour.from_str("#B03A2E"))
            return alert_embed
        
       
        # buttons -----------------------------------------
        get_log_btn = Button(label = "Get Log", style= discord.ButtonStyle.gray)
        admin_list_btn = Button(label = "Admin list", style= discord.ButtonStyle.gray)
        report_btn = Button(label = "Report", style= discord.ButtonStyle.gray)
        # functions ---------------------------------------

        async def get_log_process(interaction):
            await interaction.response.defer(ephemeral=True)
            user = interaction.user

            

            await interaction.channel.send(embed = make_alert("Warning", "Enter the ticket id you want to get the log: you have 20 seconds to enter!"))
            def check(x):
                return lambda x: x.channel == user.channel and x.author == user
                    
            message = await self.client.wait_for("message", check = check, timeout= 20)
            ticket = get_ticket(int(message.content))
            if ticket:
                admin_log = ticket['admin-log'].split("//")
                member_log = ticket['user-log'].split("//")
                #Embeds 
                log_embed = discord.Embed(title=f"Chat between {ticket['admin-name']} and {ticket['username']}", description="", color= discord.Colour.from_str("#8E44AD"))
                for admin in admin_log:
                    for member in member_log:
                        log_embed.add_field(name = "", value = admin, inline=True)
                        log_embed.add_field(name = "", value = member, inline=False)

                await interaction.channel.send(embed = log_embed)


        async def admin_list_process(interaction):
            pass

        async def report_process(interaction):
            pass
        
        get_log_btn.callback = get_log_process
        admin_list_btn.callback = admin_list_process
        report_btn.callback = report_process

        # views -------------------------------------------
        view = View()
        view.add_item(get_log_btn)
        view.add_item(admin_list_btn)
        view.add_item(report_btn)
        # Other process -----------------------------------

        await ctx.send(embed = menu, view = view)

async def setup(client):
    await client.add_cog(Security(client))