import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def profile(self ,ctx):
        # List of buttons-----------------------------------
        edit_btn = Button(label = "Edit Profile", style = discord.ButtonStyle.grey)
        border_btn = Button(label = "Border", style = discord.ButtonStyle.grey)
        reset_border_btn = Button(label = "Reset Border", style = discord.ButtonStyle.grey)


        # List of embeds---------------------------
        profile_embed = discord.Embed(title="Profile status:", description=f"Time:  **{give_current_time(True,True,True)}**", color= discord.Color.from_str(give_member_options(ctx.author.id, "border-color")))
        profile_embed.add_field(name="Your username:", value=f"{ctx.author.mention}", inline=True)
        profile_embed.add_field(name="Your current wallet:", value=f"{get_user_wallet(ctx.author.id)}", inline=False)
        profile_embed.add_field(name="Your current Level:", value=get_user_level(ctx.author.id), inline=False)
        profile_embed.add_field(name="Your current xp:", value= get_user_xp(ctx.author.id), inline=False)
        profile_embed.set_image(url = get_user_profile_url(ctx.author.id))
        profile_embed.set_footer(text = "Marshmallow Moderation")

        edit_embed = discord.Embed(title = "Edit Profile", description= "Choose a button with these explantions!", color = discord.Color.from_str("#ba4141"))
        edit_embed.add_field(name="Border", value = "If you look at the border on the left you will understand what will happen", inline = True)

        def make_error_embed(name: str, content: str):
            error = discord.Embed(title = "Error", description= "", color = discord.Color.from_str("#CBCFB5"))
            error.add_field(name=name, value = content, inline = True)
            return error
        
        def make_success_embed(name: str, content: str):
            error = discord.Embed(title = "Success!", description= "", color = discord.Color.from_str("#19C164"))
            error.add_field(name=name, value = content, inline = True)
            return error


        #---------------------------- Define functions
        async def editCallback(interaction):
            await interaction.response.defer(ephemeral= True)
            await interaction.followup.edit_message(message_id = interaction.message.id,embed = edit_embed, view = view_edit)

        async def borderEdit(interaction):
            await interaction.response.defer(ephemeral= True)
            user = interaction.user
            await interaction.channel.send("You have 20 second to enter hex color code you want: ")
            def check(x):
                return lambda x: x.channel == user.channel and x.author == user
                    
            msg = await self.client.wait_for("message", check = check, timeout= 20)
            if msg.content:
                if str(msg.content).startswith("#"):
                    if len(str(msg.content)) < 8 :
                        update_member_options(ctx.author.id, "border-color", str(msg.content))
                        await interaction.channel.send(embed = make_success_embed("Color changing", "Your border color has change use **-profile** command again!"))
                    else:
                        await interaction.channel.send(embed = make_error_embed("Too much character", "Your code must be under 8 character! try again"), view = view_edit)
                else:
                    await interaction.channel.send(embed = make_error_embed("Not Hex code", "make sure you entered a hex code color like: #ffffff"), view = view_edit)

        async def resetBorder(interaction):
            color = give_member_options(ctx.author.id, "user-color")
            update_member_options(ctx.author.id, "border-color", color)
            await interaction.response.edit_message(embed = make_success_embed("Reset to default", "You have been reset your color successfully!"), view = None)


        #----------------------- Set callback for btns
        edit_btn.callback = editCallback
        border_btn.callback = borderEdit
        reset_border_btn.callback = resetBorder
        #---------------------------- Define View's

        view = View()
        view.add_item(edit_btn)
        
        view_edit = View()
        view_edit.add_item(border_btn)
        view_edit.add_item(reset_border_btn)



        await ctx.send(embed = profile_embed, view = view)


async def setup(client):
    await client.add_cog(Profile(client))