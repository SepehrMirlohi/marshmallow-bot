import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Colour(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roles(self, ctx):
        if ctx.author.id == 767030513088331797:
            # Embeds -----------------------------------------------------------------
            roles_menu = discord.Embed(title="Colour Menu", description="", color= discord.Color.from_rgb(0,51,102))
            roles_menu.add_field(name="Colours", value="Normal colour roles that everyone can achive it you can see the list and choose one of them by using this key!", inline=False)
            roles_menu.add_field(name="Premium Colours", value="if you have Premium you can have a spesific colour by using this key", inline=False)
            roles_menu.set_image(url="https://s2.uupload.ir/files/discord-colour-roles_v5l7.gif")


            alert = discord.Embed(title="Marshmallow alert", description="You have 10 second to send the number", color= discord.Color.from_rgb(13,124,200))
            alert.add_field(name="", value="Please send the number of the color you wanted to have: ", inline = True)
            alert.set_footer(text="Marshmallow moderation")


            seccess_alert = discord.Embed(title="Marshmallow alert", description="Success!", color= discord.Color.from_rgb(14,194,39))
            seccess_alert.add_field(name="", value="You have successfully got your colour role!", inline = True)


            failed = discord.Embed(title="Marshmallow alert", description="Failed!", color= discord.Color.from_rgb(227,35,9))
            failed.add_field(name="", value="Please accept our apologize but something went wrong :(", inline = True)


            # Buttons -----------------------------------------------------------------
            colour_btn = Button(label = "Colours", style= discord.ButtonStyle.gray)
            spesific_btn = Button(label = "Spesific Colours", style= discord.ButtonStyle.gray)

            #Define dm variable and embeds

    

            # Callback functions 

            async def colours_callback(interaction):
                
                await interaction.response.defer(ephemeral= True)
                user = interaction.user
                is_color = 0
                have_color = 1
                await user.send(embed = alert)
                def check(x):
                    return lambda x: x.channel == user.dm_channel and x.author == user
                    
                msg = await self.client.wait_for("message", check = check, timeout= 20)
                for color in get_colour_roles():
                    if int(color['number']) == int(msg.content):
                            color_giving = discord.utils.get(ctx.guild.roles, id = color['color-id'])
                            for checkrole in user.roles:
                                if int(checkrole.name.find("〆")) == 0:
                                    if str(checkrole.name) != str(color['color-name']):
                                        is_color = 1
                                        have_color = 0
                                        await user.remove_roles(checkrole)
                                        await user.add_roles(color_giving)
                                    
                            if is_color == 0:
                                await user.add_roles(color_giving)

                            if have_color == 1:
                                await user.send('You have already this color! Please try again...')

                            check_status = 0
                            new_user = discord.utils.get(self.client.get_all_members(), id = user.id)

                            for recheck in new_user.roles:
                                
                                if str(recheck.id) == str(color['color-id']):
                                    check_status = 1
                            if have_color != 1:

                                if check_status == 1:
                                    await user.send(embed = seccess_alert)
                                else: 
                                    await user.send(embed = failed)

        
            async def spesific_callback(interaction):
                pass


            colour_btn.callback = colours_callback
            spesific_btn.callback = spesific_callback

            #View ----------------------------------------------------------------------
            view = View(timeout = None)
            view.add_item(colour_btn)
            view.add_item(spesific_btn)

            await ctx.send(embed = roles_menu, view = view)



async def setup(client):
    await client.add_cog(Colour(client))