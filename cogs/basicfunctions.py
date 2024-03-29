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