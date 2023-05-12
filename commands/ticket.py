import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class BirthDay(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_any_role(1018134791943635015)
    async def Ticket(self, ctx):
        # Embeds ---------------------------------
        ticket_menu_embed = discord.Embed(title= "Marshmallow Ticket System", description= "", color= discord.Colour.from_str("#F5B041"))
        ticket_menu_embed.add_field(name="normal ticket", value="You can answer your normal question or give us your suggestions!", inline=True)
        ticket_menu_embed.add_field(name="staff ticket", value="You can compelete a form and try to join in our staff team!", inline=True)
        ticket_menu_embed.set_footer(text="Marshmallow Moderation")

        # Buttons ----------------------------------
        menu_btn_staff = Button(label="Staff", style= discord.ButtonStyle.gray)
        menu_btn_public = Button(label="Normal", style=discord.ButtonStyle.gray)

        
        async def callback_public(interaction):
            
            await interaction.response.defer(ephemeral= True)

        async def callback_staff(interaction):

            await interaction.response.defer(ephemeral= True)
        
        menu_btn_staff.callback = callback_staff
        menu_btn_public.callback = callback_public

        view = View(timeout = None)
        view.add_item(menu_btn_public)
        view.add_item(menu_btn_staff)

        await ctx.send(embed = ticket_menu_embed, view = view)





async def setup(client):
    await client.add_cog(BirthDay(client))