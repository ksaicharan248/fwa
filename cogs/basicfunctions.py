import discord
from discord.ext import commands
import COC
import pickle
from discord import Embed , Color

from main import p


class basicfuctions(commands.Cog) :
    def __init__(self , client) :
        self.client = client

    @commands.command(name='changenick' , aliases=['nick' , 'cnick'] , help='Change the nickname of a user' ,
                      usage=f"{p}changenick <user> <new_nickname>")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'TSL' , 'WAL' , 'HML')
    async def changenick(self , ctx , member: discord.Member , * , new_nickname) :
        if not ctx.me.top_role > member.top_role :
            await ctx.send("Insufficient permissions or role hierarchy to change the user's nickname.")
            return
        try :
            await member.edit(nick=new_nickname)
            embed = Embed(title="Nickname changed" , color=Color.random())
            embed.add_field(name="User" , value=member.mention , inline=False)
            embed.add_field(name="Moderator" , value=ctx.author.mention , inline=False)

            await ctx.send(embed=embed)
        except discord.Forbidden :
            await ctx.send("I do not have permission to change the user's nickname.")
        except discord.HTTPException :
            await ctx.send("An error occurred while changing the user's nickname.")

    @commands.command(name='role' , help='Add a role to a user' , usage=f"{p}role <user> <@roles>")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
    async def role(self , ctx , user: discord.Member , *roles: discord.Role) :
        if ctx.author.guild_permissions.manage_roles :
            if ctx.guild.me.guild_permissions.manage_roles :
                await user.add_roles(*roles)
                await ctx.message.delete()
            else :
                await ctx.send("I don't have permission to manage roles.")
        else :
            await ctx.send('You do not have permission to manage roles.')

    @commands.command(name="rm" , help="Remove a role from a user" , usage=f"{p}rm <user> <@roles>")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
    async def rm_role(self , ctx , user: discord.Member , *roles: discord.Role) :
        if ctx.author.guild_permissions.manage_roles :
            if ctx.guild.me.guild_permissions.manage_roles :
                await user.remove_roles(*roles)
                await ctx.message.delete()
            else :
                await ctx.send("I don't have permission to manage roles.")
        else :
            await ctx.send('You do not have permission to manage roles.')

    @commands.command()
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'TSL' , 'WAL' , 'HML')
    async def removenick(self , ctx , member: discord.Member) :
        if not ctx.me.top_role > member.top_role :
            await ctx.send("Insufficient permissions or role hierarchy to remove the user's nickname.")
            return
        try :
            await member.edit(nick=None)
            embed = Embed(title="Nickname Removed" , color=Color.random())
            embed.add_field(name="User" , value=member.mention , inline=False)
            embed.add_field(name="Moderator" , value=ctx.author.mention , inline=False)
            await ctx.send(embed=embed)
        except discord.Forbidden :
            await ctx.send("I do not have permission to remove the user's nickname.")
        except discord.HTTPException :
            await ctx.send("An error occurred while removing the user's nickname.")

    @commands.command(name='checkall' , aliases=['ca'])
    async def checkall(self , ctx , member_role: discord.Role = None , clan_tag=None) :
        re_apply = ctx.guild.get_role(1055440440968617994)
        re_apply_tags = []
        re_apply_channel = ctx.guild.get_channel(1055440286806966322)
        with open('datasheets/userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if clan_tag is None :
            clan_tag = user_data[ctx.author.id]['clan']
        else :
            clan_tag = clan_tag.strip('#')
        member_ids = [member.id for member in ctx.guild.members if member_role in member.roles]
        user_data_tags = {}
        for member_id in member_ids :
            try :
                user_data_tags[member_id] = user_data[member_id]['tag']
            except KeyError :
                user_data_tags[member_id] = None
        updated_data = await COC.fetch_users_info(user_data_tags)
        embed_no_data = Embed(title="NON LINKED USERS" , color=Color.red())
        embed_linked_no_update = Embed(title="LINKED USERS" , color=Color.green())
        embed_linked_reapply = Embed(title="REMOVED USERS" , color=Color.random())
        embed_linked_updated = Embed(title="UPDATED USERS DATA" , color=Color.green())
        embed_no_data_description = f"NO DATA EXITS \nfor the following users :\n\n"
        embed_linked_updated_description = ""
        embed_linked_no_update_description = ""
        embed_linked_reapply_description = ""
        for user_id , player_data in updated_data :
            member = await ctx.guild.get_member(user_id)
            if player_data :
                user_data[user_id] = {'tag' : player_data['tag'].strip('#') , 'name' : player_data['name'] ,
                                      'clan' : player_data['clan']['tag'] if 'clan' in player_data else 'no clan' ,
                                      'clanname' : player_data['clan']['name'] if 'clan' in player_data else 'no clan'}
                if player_data['clan'] and player_data['clan']['tag'] == clan_tag :
                    if member :
                        role = player_data['role']
                        nickname = await member.nick
                        if role == "leader" and nickname[0] != 'L' :
                            nick = "Lead - "
                            await member.edit(nick=f'{nick}{player_data["name"]}')
                            embed_linked_updated_description += f"{nickname} to {member.nick} \n"
                        elif role == "coLeader" and nickname[0] != 'C' :
                            nick = "Co - "
                            await member.edit(nick=f'{nick}{player_data["name"]}')
                            embed_linked_updated_description += f"{nickname} to {member.nick} \n"
                        elif role == "admin" and nickname[0] != 'E' :
                            nick = "Eld - "
                            await member.edit(nick=f'{nick}{player_data["name"]}')
                            embed_linked_updated_description += f"{nickname} to {member.nick} \n"
                        elif role == "member" and nickname[0] != 'M' :
                            nick = "Mb - "
                            await member.edit(nick=f'{nick}{player_data["name"]}')
                            embed_linked_updated_description += f"{nickname} to {member.nick} \n"
                        else:
                            embed_linked_no_update_description += f"{member.nick} \n"
                elif player_data['role']:
                    if player_data['role'] == "leader" or player_data['role'] == "coLeader" :
                        pass
                else :
                    if member :
                        embed_linked_reapply_description += f"{member.nick} \n"
                        re_apply_tags.append(member.id)
                        #await member.edit(nick=f're - {member.name}' , roles=[re_apply])
            else :
                if member :
                   embed_no_data_description += f"{member.nick} \n"

        embed_linked_reapply.description = embed_linked_reapply_description
        embed_linked_updated.description = embed_linked_updated_description
        embed_linked_no_update.description = embed_linked_no_update_description
        embed_no_data.description = embed_no_data_description
        await ctx.send(embeds=[embed_linked_no_update , embed_linked_updated , embed_no_data , embed_linked_reapply])

    @commands.command(name='usage' , aliases=['u'])
    async def usage(self , ctx , command_name: str) :
        await ctx.message.delete()
        command = self.client.get_command(command_name)
        if command :
            help_info = f"```command : {ctx.prefix}{command.name}\nabout  : {command.help}\n\nusage  : {command.usage}``` \n "
            await ctx.send(help_info)
        else :
            await ctx.send("Command not found. Please provide a valid command name.")


async def setup(client) :
    await client.add_cog(basicfuctions(client))
