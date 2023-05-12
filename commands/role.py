import os, sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from commands.init import *


class Role(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def role(self, ctx):
            
        #------------------------------- Buttons Section
        add_role_key = Button(label="Add", style=discord.ButtonStyle.green)
        role_list_key = Button(label="Default roles List", style=discord.ButtonStyle.green)
        remove_role_key = Button(label="Remove", style=discord.ButtonStyle.red)
        guide_role_key = Button(label="Guideline", style=discord.ButtonStyle.grey)
        #------------------------------- Embed section
        embed = discord.Embed(title="", description= "Time: **"+give_current_time(True, True, True)+"**", color=discord.Color.from_rgb(231,225,212))
        embed.add_field(name="**Role Editor**", value="Please select the option you want to make the changes with")
        #---
        help_embed = discord.Embed(title="A short guide:", description="", color = discord.Color.from_rgb(231,225,212))
        help_embed.add_field(name="Add", value="You can use this one to append some role to default-roles list, this list will check and if someone trying to join our server will get this role automatically!", inline= True)
        help_embed.add_field(name="Remove", value="This one can remove a role from default-roles list!", inline = False)

        #-------------------------------- function and config section ---
        async def give_guide_page(interaction):
            await interaction.response.edit_message(view = None, embed = help_embed)

        async def give_add_page(interaction):

            alert_embed = discord.Embed(title="", description="Time: **"+give_current_time(True, True, True)+"**", color= discord.Color.from_rgb(231,225,212))
            alert_embed.add_field(name="Alert", value="Send the role name or role id you want to **add**: ")
            await interaction.response.edit_message(embed = alert_embed, view = None)
            def check(m: discord.Message):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            message = await self.client.wait_for("message", check = check, timeout = 20)
            if message.content:
                rolename = int(message.content)
                if type(rolename) is int:
                    add_default_role(int(rolename))
                    await ctx.send("The role has appended!")


        async def give_remove_field(interaction):
            alert_embed = discord.Embed(title="", description="Time: **"+give_current_time(True, True, True)+"**", color= discord.Color.from_rgb(231,225,212))
            alert_embed.add_field(name="Alert", value="Send the role name or role id you want to **remove**: ")
            await interaction.response.edit_message(view = None, embed = alert_embed)
            def check(m: discord.Message):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            message = await self.client.wait_for("message", check = check, timeout = 20)
            if message.content:
                rolename = int(message.content)
                if type(rolename) is int:
                    remove_default_role(int(rolename))
                    await ctx.send("The role has removed!")

        async def give_roles_list(interaction):
            counter = 1
            default_roles = give_default_roles()
            alert_embed = discord.Embed(title="", description= f"Time: **{give_current_time(True, True, True)}**", color = discord.Color.from_rgb(231,225,212))
            for role in default_roles:
                for guild in self.client.guilds:
                    for role_name in guild.roles:
                        if role == role_name.id:
                            alert_embed.add_field(name=f"Number {counter}", value= role_name.name)
                            counter = counter + 1

            await interaction.response.edit_message(view = None, embed = alert_embed)
        #-------------------- Other workings ---
        add_role_key.callback = give_add_page
        remove_role_key.callback = give_remove_field
        guide_role_key.callback = give_guide_page
        role_list_key.callback = give_roles_list
        view = View(timeout= None)
        view.add_item(add_role_key)
        view.add_item(role_list_key)
        view.add_item(remove_role_key)
        view.add_item(guide_role_key)

        await ctx.send(embed = embed, view= view)

    @commands.command()
    async def ColorList(self, ctx):
        counter = 1
        roles_list = discord.Embed(title="List of **normal** colours Page 1", description="", color= discord.Color.from_rgb(212,232,15))
        roles_list2 = discord.Embed(title="List of **normal** colours Page 2", description="", color= discord.Color.from_rgb(212,232,15))
        for guild in self.client.guilds:
            for roles in guild.roles:
                status = str(roles.name).find("〆")
                if status == 0:
                        if counter <= 25:
                            roles_list.add_field(name="", value=f"({counter})   " + roles.mention, inline=False)
                        else:
                            roles_list2.add_field(name="", value=f"({counter})   " + roles.mention, inline=False)
                        counter += 1
        roles_list2.add_field(name="", value="Choose a color here and send \n the number of that color here!", inline=False)        
        roles_list.set_footer(text="Marshmallow Moderation")
        roles_list2.set_footer(text="Marshmallow Moderation")

        await ctx.send(embed = roles_list)
        await ctx.send(embed = roles_list2)


async def setup(client):
    await client.add_cog(Role(client))