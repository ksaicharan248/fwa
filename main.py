import io
import discord
from discord.ui import Button , View
from PIL import Image , ImageDraw , ImageFont
import requests
from io import BytesIO
from discord.ext import commands
import COC
from discord import Embed , Color
from setkey import keyy
from webser import keep_alive
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle

# Define the intents
intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix="$" , intents=intents)
client.remove_command("help")

p = client.command_prefix


@client.event
async def on_ready() :
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_command_error(ctx , error) :
    if isinstance(error , commands.MissingRequiredArgument) :
        embed = discord.Embed(title="WARNING ⚠️⚠️⚠️" ,
                              description="You forgot to mention the user. Please use the command again by mentioning the user" ,
                              color=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error , commands.MissingRole) or isinstance(error , commands.MissingAnyRole) :
        embed = discord.Embed(title="WARNING ⚠️⚠️⚠️" , description="You don't have the required role ❌❌❌." ,
                              color=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error , commands.MemberNotFound) :
        embed = discord.Embed(title="WARNING ⚠️⚠️⚠️" , description="The user is not in the server." ,
                              color=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error , commands.CommandInvokeError) and isinstance(error.original , discord.HTTPException) :
        embed = discord.Embed(title="WARNING ⚠️⚠️⚠️" , description="something is missing please check and try again." ,
                              color=discord.Color.red())
        await ctx.send(embed=embed)

    else :
        raise error


@client.event
async def on_member_remove(member) :
    with open("userdata.pkl" , "rb") as file :
        user_data = pickle.load(file)
    if member.id in user_data.keys() :
        try :
            del user_data[member.id]
        except :
            user_data.pop(member.id)
        with open("userdata.pkl" , "wb") as file :
            pickle.dump(user_data , file)


@client.event
async def on_member_join(member) :
    if member.guild.id == 1054435038881665024 :
        welcome_channel = client.get_channel(1055439542863274038)
        if welcome_channel :
            p = client.command_prefix
            await member.add_roles(discord.utils.get(member.guild.roles , name='🔸ENTRY🔸'))
            await welcome_channel.send(f'Hello, {member.mention} !')
            embed = Embed(title=f"Welcome  to  ⚔️TEAM ELITES⚔️!" , color=Color.random())
            embed.description = f"You can read our rules and details about 💎FWA💎 in <#1054438569378332754> \n\n" \
                                f"If you wish to join one of our clans then please follow the steps below.\n\n" \
                                f"**•Step 1** : Post your PLAYER tag\n" \
                                f"**•Step 2** : type this ⚠️ important ⚠️ ```{p}link #your_player_tag``` \n" \
                                f"**•Step 3** : Post a picture of My Profile tab\n" \
                                f"**•Step 4** : Post a picture of your 💎FWA💎 base \n" \
                                f"If you don’t have a 💎FWA💎 base then you can type \n```{p}bases```" \
                                f" OR visit <#1054438501233479760>\n " \
                                f"**•Step 5** : Have some patience, " \
                                f"you will be assisted shortly.\n\nWe may not have an instant space but **ASAP** we have " \
                                f"a space, we will recruit you. Till then we will put you in <#1055439744739315743> " \
                                f"\n\n🚨Note - We don’t recruit FWA BANNED players."
            await welcome_channel.send(embed=embed)


@client.command(name='help')
async def help(ctx) :
    p = client.command_prefix
    embed = discord.Embed(
        description=f"{p}wel                - Welome player\n{p}ping               - Show latency\n{p}help               - Show help\n{p}role                - Add role\n{p}rm                  - Remove role\n{p}changenick  - Change nickname\n{p}removenick  - remove nick name" ,
        colour=Color.random())

    embed.add_field(name="LEADER COMMANDS" ,
                    value=f"`ts-m`         -  add player to The shield\nusage:  {p}ts-m  @mention\n\n`mn-m`         - add player to Monsters\nusage:  {p}mn-m  @mention \n\n`wa-m`         - add player to warning \nusage:  {p}wa-m  @mention \n\n`sv-m`         - add player to ACTIVE CLAN | —< SAVAGE >—  \nusage:  {p}sv-m  @mention \n\n`unq`         - add player to unqualify\nusage:  {p}unq  @mention  IGN\n\n`app`       -  approve the player\nusage:   {p}app @mention \n\n`re`         - send the player to reapply \nusage : {p}re @mention  IGN\n\n`check`        - check the player with chocolate clash\nusage : {p}check playertag \nNOTE : if linked mention player \n\n `force_link`        - link any other player with tag \nusage :  || {p}force_link   @mention   #player_tag ||" ,
                    inline=False)
    embed.add_field(name="PLAYER COMMANDS" ,
                    value=f"`link`          - link the bot with player tag \nusage : {p}link  #**player_tag**  "
                          f" \n\n`profile`         - profile of player" , inline=False)

    await ctx.send(embed=embed)


@client.command(name='wel' , help='Welome player')
async def welcome(ctx , member: discord.Member = None) :
    if member is None :
        await ctx.send('welcome !')
    else :

        await ctx.send(f'Hello, {member.mention} !')
    p = client.command_prefix
    embed = Embed(title=f"Welcome  to  ⚔️TEAM ELITES⚔️!" , color=Color.random())
    embed.description = f"You can read our rules and details about 💎FWA💎 in <#1054438569378332754> \n\n" \
                        f"If you wish to join one of our clans then please follow the steps below.\n\n" \
                        f"**•Step 1** : Post your PLAYER tag\n" \
                        f"**•Step 2** : type this ⚠️ important ⚠️ ```{p}link #your_player_tag``` \n" \
                        f"**•Step 3** : Post a picture of My Profile tab\n" \
                        f"**•Step 4** : Post a picture of your 💎FWA💎 base \n" \
                        f"If you don’t have a 💎FWA💎 base then you can type \n```{p}bases```" \
                        f" OR visit <#1054438501233479760>\n " \
                        f"**•Step 5** : Have some patience, " \
                        f"you will be assisted shortly.\n\nWe may not have an instant space but **ASAP** we have " \
                        f"a space, we will recruit you. Till then we will put you in <#1055439744739315743> " \
                        f"\n\n🚨Note - We don’t recruit FWA BANNED players."
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx) :
    print(ctx)
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
async def role(ctx , user: discord.Member , *roles: discord.Role) :
    if ctx.author.guild_permissions.manage_roles :
        if ctx.guild.me.guild_permissions.manage_roles :
            await user.add_roles(*roles)
            await ctx.message.delete()
        else :
            await ctx.send("I don't have permission to manage roles.")
    else :
        await ctx.send('You do not have permission to manage roles.')


@client.command(name="rm")
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
async def rm_role(ctx , user: discord.Member , *roles: discord.Role) :
    if ctx.author.guild_permissions.manage_roles :
        if ctx.guild.me.guild_permissions.manage_roles :
            await user.remove_roles(*roles)
            await ctx.message.delete()
        else :
            await ctx.send("I don't have permission to manage roles.")
    else :
        await ctx.send('You do not have permission to manage roles.')


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'TSL' , 'WAL' , 'HML')
async def changenick(ctx , member: discord.Member , * , new_nickname) :
    # Check if the bot has the necessary permissions and role hierarchy to change nicknames
    if not ctx.me.top_role > member.top_role :
        await ctx.send("Insufficient permissions or role hierarchy to change the user's nickname.")
        return

    try :
        # Change the user's nickname
        await member.edit(nick=new_nickname)
        embed = Embed(title="Nickname changed" , color=Color.random())
        embed.add_field(name="User" , value=member.mention , inline=False)
        embed.add_field(name="Moderator" , value=ctx.author.mention , inline=False)

        await ctx.send(embed=embed)
    except discord.Forbidden :
        await ctx.send("I do not have permission to change the user's nickname.")
    except discord.HTTPException :
        await ctx.send("An error occurred while changing the user's nickname.")


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'TSL' , 'WAL' , 'HML')
async def removenick(ctx , member: discord.Member) :
    # Check if the bot has the necessary permissions and role hierarchy to change nicknames
    if not ctx.me.top_role > member.top_role :
        await ctx.send("Insufficient permissions or role hierarchy to remove the user's nickname.")
        return

    try :
        # Remove the user's nickname by setting it to None
        await member.edit(nick=None)

        # Create a red embedded message
        embed = Embed(title="Nickname Removed" , color=Color.random())
        embed.add_field(name="User" , value=member.mention , inline=False)
        embed.add_field(name="Moderator" , value=ctx.author.mention , inline=False)

        await ctx.send(embed=embed)
    except discord.Forbidden :
        await ctx.send("I do not have permission to remove the user's nickname.")
    except discord.HTTPException :
        await ctx.send("An error occurred while removing the user's nickname.")


@client.command(name='ts-m' , aliases=['tsm'] , help=f'add player to The shield ' , usage=f'{p}ts-m <@mention>')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'TSL')
async def ts_m(ctx , member: discord.Member) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1055527200193007626)
        with open('userdata.pkl' , 'rb') as f :
            data = pickle.load(f)
        if member.id in data.keys() :
            info = COC.get_user(data[member.id])
        else :
            e = Embed(title='Player data not fount' , colour=Color.red())
            e.description = f'Please link the {member.mention} with the game tag to proced```{client.command_prefix}link #tag```'
            await ctx.send(embed=e)
            return
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='TSC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            embed = Embed(color=Color.green())
            embed.description = f"✅Changed roles for {member.name}, +TSC, +🔰THE FARMERS MEMBERS🔰,-🔸ENTRY🔸"
            await channel.send(embed=embed)
            flag1 = True
        except Exception as e :
            embed = Embed(color=Color.red())
            embed.description = f"❌Failed to change roles for {member.name}\n Reason{e}"
            await ctx.send(embed=embed)
            flag1 = False
        try :
            new_nickname = f'{COC.get_prefix(info["role"])}{info["name"]}'
            await member.edit(nick=new_nickname)
            embed1 = Embed(color=Color.green())
            embed1.description = f"✅Changed name for {member.name} to  {member.mention}"
            await channel.send(embed=embed1)
            flag2 = True
        except Exception as e :
            embed1 = Embed(color=Color.red())
            embed1.description = f"❌Failed to change name for {member.name}\n Reason:{e} "
            await ctx.send(embed=embed1)
            flag2 = False

        if flag1 and flag2 :
            await ctx.send(f"{member.nick} moved to  **THE SHIELD** 🚀")
            await channel.send(f"{member.mention} is now a member of **THE SHIELD**")
            embed3 = Embed(color=Color.green())
            embed3.description = ("🍻 Welcome, this is your clan chat.\n""Make sure to go through the followings -\n"
                                  "\n"
                                  "『📢』**<#1055531962774868038>** - For important clan announcements\n"
                                  "『⚠』**<#1054439098342969425>** - For war rules and instructions\n"
                                  "\n"
                                  "Note - Make Sure To Maintain This In Clan\n"
                                  "✅ Donate\n"
                                  "✅ Attack in wars\n"
                                  "✅ Follow mails\n"
                                  "✅ 2000 in CG\n"
                                  "✅ Participate in Clan-Capitals\n"
                                  "❌ Don’t kick anyone")

            await channel.send(embed=embed3)

    else :
        await ctx.send("MISSING permissions")


@client.command(name='mn-m')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'MSL')
async def mo_m(ctx , member: discord.Member) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1063291093178916884)
        with open('userdata.pkl' , 'rb') as f :
            data = pickle.load(f)
        if member.id in data.keys() :
            info = COC.get_user(data[member.id])
        else :
            e = Embed(title='Player data not fount' , colour=Color.red())
            e.description = f'Please link the {member.mention} with the game tag to proced```{client.command_prefix}link #tag```'
            await ctx.send(embed=e)
            return
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='MSC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            embed = Embed(color=Color.green())
            embed.description = f"✅Changed roles for {member.name}, +HMC, +🔰THE FARMERS MEMBERS🔰,-🔸ENTRY🔸"
            await channel.send(embed=embed)
            flag1 = True

        except Exception as e :
            embed = Embed(color=Color.red())
            embed.description = f"❌Failed to change roles for {member.name}\n Reason{e}"
            await ctx.send(embed=embed)
            flag1 = False
        try :
            new_nickname = f'{COC.get_prefix(info["role"])}{info["name"]}'
            await member.edit(nick=new_nickname)
            embed1 = Embed(color=Color.green())
            embed1.description = f"✅Changed name for {member.name} to  {member.mention}"
            await channel.send(embed=embed1)
            flag2 = True
        except Exception as e :
            embed1 = Embed(color=Color.red())
            embed1.description = f"❌Failed to change name for {member.name}\n Reason:{e} "
            await ctx.send(embed=embed1)
            flag2 = False

        if flag1 and flag2 :
            await ctx.send(f"{member.nick} moved to  **☬M̷O̷N̷S̷T̷E̷R☬**")
            await channel.send(f"{member.mention} is now a member of **☬M̷O̷N̷S̷T̷E̷R☬** 🚀")
            embed3 = Embed(color=Color.green())
            embed3.description = ("🍻 Welcome, this is your clan chat.\n""Make sure to go through the followings -\n"
                                  "\n"
                                  "『📢』**clan-announcements** - For important clan announcements\n"
                                  "『⚠』**<#1054439098342969425>** - For war rules and instructions\n"
                                  "\n"
                                  "Note - Make Sure To Maintain This In Clan\n"
                                  "✅ Donate\n"
                                  "✅ Attack in wars\n"
                                  "✅ Follow mails\n"
                                  "✅ 2000 in CG\n"
                                  "✅ Participate in Clan-Capitals\n"
                                  "❌ Don’t kick anyone")

            await channel.send(embed=embed3)

    else :
        await ctx.send("MISSING permissions")


@client.command(name='wa-m' , aliases=['wam'] , help='Move member to WARNING' , usage=f'{p}wa-m <@mention>')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL')
async def wa_m(ctx , member: discord.Member) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1055527254643445812)
        with open('userdata.pkl' , 'rb') as f :
            data = pickle.load(f)
        if member.id in data.keys() :
            info = COC.get_user(data[member.id])
        else :
            e = Embed(title='Player data not fount' , colour=Color.red())
            e.description = f'Please link the {member.mention} with the game tag to proced```{client.command_prefix}link #tag```'
            await ctx.send(embed=e)
            return
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='WAC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            embed = Embed(color=Color.green())
            embed.description = f"✅Changed roles for {member.name}, +WAC, +🔰THE FARMERS MEMBERS🔰,-🔸ENTRY🔸"
            await channel.send(embed=embed)
            flag1 = True
        except Exception as e :
            embed = Embed(color=Color.red())
            embed.description = f"❌Failed to change roles for {member.name}\n Reason{e}"
            await ctx.send(embed=embed)
            flag1 = False
        try :
            new_nickname = f'{COC.get_prefix(info["role"])}{info["name"]}'
            await member.edit(nick=new_nickname)
            embed1 = Embed(color=Color.green())
            embed1.description = f"✅Changed name for {member.name} to  {member.mention}"
            await channel.send(embed=embed1)
            flag2 = True
        except Exception as e :
            embed1 = Embed(color=Color.red())
            embed1.description = f"❌Failed to change name for {member.name}\n Reason:{e} "
            await ctx.send(embed=embed1)
            flag2 = False

        if flag1 and flag2 :
            await ctx.send(f"{member.nick} moved to  **♤WARNING♤** 🚀")
            await channel.send(f"{member.mention} is now a member of **♤WARNING♤**")
            embed3 = Embed(color=Color.green())
            embed3.description = ("🍻 Welcome, this is your clan chat.\n""Make sure to go through the followings -\n"
                                  "\n"
                                  "『📢』**<#1055532032626806804>** - For important clan announcements\n"
                                  "『⚠』**<#1054439098342969425>** - For war rules and instructions\n"
                                  "\n"
                                  "Note - Make Sure To Maintain This In Clan\n"
                                  "✅ Donate\n"
                                  "✅ Attack in wars\n"
                                  "✅ Follow mails\n"
                                  "✅ 2000 in CG\n"
                                  "✅ Participate in Clan-Capitals\n"
                                  "❌ Don’t kick anyone")

            await channel.send(embed=embed3)

    else :
        await ctx.send("MISSING permissions")


@client.command(name='wfx-m')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WFL')
async def wfx_m(ctx , member: discord.Member) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1056605645836656791)
        with open('userdata.pkl' , 'rb') as f :
            data = pickle.load(f)
        if member.id in data.keys() :
            info = COC.get_user(data[member.id])
        else :
            e = Embed(title='Player data not fount' , colour=Color.red())
            e.description = f'Please link the {member.mention} with the game tag to proced```{client.command_prefix}link #tag```'
            await ctx.send(embed=e)
            return
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='WFC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            embed = Embed(color=Color.green())
            embed.description = f"✅Changed roles for {member.name}, +WFC, +🔰THE FARMERS MEMBERS🔰,-🔸ENTRY🔸"
            await channel.send(embed=embed)
            flag1 = True
        except Exception as e :
            embed = Embed(color=Color.red())
            embed.description = f"❌Failed to change roles for {member.name}\n Reason{e}"
            await ctx.send(embed=embed)
            flag1 = False
        try :
            new_nickname = f'{COC.get_prefix(info["role"])}{info["name"]}'
            await member.edit(nick=new_nickname)
            embed1 = Embed(color=Color.green())
            embed1.description = f"✅Changed name for {member.name} to  {member.mention}"
            await channel.send(embed=embed1)
            flag2 = True
        except Exception as e :
            embed1 = Embed(color=Color.red())
            embed1.description = f"❌Failed to change name for {member.name}\n Reason:{e} "
            await ctx.send(embed=embed1)
            flag2 = False

        if flag1 and flag2 :
            await ctx.send(f"{member.nick} is now a member of **War Farmers x44** 🚀")
            await channel.send(f"{member.mention} is now a member of **War Farmers x44**")
            embed3 = Embed(color=Color.green())
            embed3.description = ("🍻 Welcome, this is your clan chat.\n""Make sure to go through the followings -\n"
                                  "\n"
                                  "『📢』**<#1055532032626806804>** - For important clan announcements\n"
                                  "『⚠』**<#1054439098342969425>** - For war rules and instructions\n"
                                  "\n"
                                  "Note - Make Sure To Maintain This In Clan\n"
                                  "✅ Donate\n"
                                  "✅ Attack in wars\n"
                                  "✅ Follow mails\n"
                                  "✅ 2000 in CG\n"
                                  "✅ Participate in Clan-Capitals\n"
                                  "❌ Don’t kick anyone")

            await channel.send(embed=embed3)

    else :
        await ctx.send("MISSING permissions")


@client.command(name="unq" , aliases=["unqualified"] , help='Move a member to unqualifed ' , usage=f'{p}unq <@mention>')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
async def unq(ctx , member: discord.Member , * , new_nickname=None) :
    gid = ctx.guild.id
    await ctx.message.delete()
    if new_nickname is None :
        await member.edit(nick=f"unq - {member.name}")
    else :
        await member.edit(nick=f"{new_nickname}")
    await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
    info = {1054435038881665024 : ['unqualified❌' , 1055440018279235657] ,
            1152220160028057660 : ['UN-Qualified' , 1152228011798700092]}
    await member.add_roles(discord.utils.get(ctx.guild.roles , name=info[gid][0]))
    channel = client.get_channel(info[gid][1])
    await channel.send(f"{member.mention} has been unqualified by {ctx.author.mention}")
    e = Embed(title="UNQUALIFIED " , color=Color.random())
    e.description = f'⚠️ You have been placed here Because you havent Fulfill the Minimum Requirements to Apply to ' \
                    f'Join our Clans. To check our Requirements please type \n ➡️ !reqs \n\n🔍 We are always here also ' \
                    f'to Assist you.\n❌ Donot request to Join in Game unless Instructed to do so\n🏛️You may stay in ' \
                    f'your current Clan or join a Random Clan while upgrading your base to Meet our Clan Requirements. ' \
                    f'But do not join any FWA Blacklisted clans.\n ✅When your requirements are met, type !wel \n ' \
                    f'\n**please follow all the instructions** \nauthour : {ctx.author.mention}'

    await channel.send(embed=e)


@client.command(name='app' , aliases=['approve'] , help='Move a member to Approved channel' ,
                usage=f'{p}approve @member')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
async def approve(ctx , member: discord.Member) :
    with open('userdata.pkl' , 'rb') as f :
        data = pickle.load(f)
    if member.id in data.keys() :
        info = COC.get_user(data[member.id])
        await member.edit(nick=f'TH {info["townHallLevel"]} - {info["name"]} ')
        await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
        info = {1054435038881665024 : ['approved✅' , 1055439744739315743 , 1126856734095462511] ,  # elites
                1152220160028057660 : ['approved✅' , 1167482592254238740 , 1152229286305079307]}  # jigg
        await member.add_roles(discord.utils.get(ctx.guild.roles , name=info[ctx.guild.id][0]))
        channel = client.get_channel(info[ctx.guild.id][1])
        await channel.send(f"{member.mention} has been approved by {ctx.author.mention}")
        e = Embed(title="APPROVED " , color=Color.random())
        e.description = f'❯ Clan spots will be posted in this {client.get_channel(info[ctx.guild.id][1]).mention}, make sure to check it\n' \
                        f'❯ You will be **@notified** if a spot available for your TH level.\n' \
                        f'❯ Just make sure to reply as fast as possible to ensure your spot.\n' \
                        f'❯ Donot request to join in game unless instructed to do so.\n' \
                        f'❯ You may stay in your **current clan** or join a random clan while waiting for a **spot**.\n' \
                        f'❯ Make sure to have **NO war timer** when you answer for spots.\n' \
                        f'❯ Ask in {client.get_channel(info[ctx.guild.id][2]).mention} if you have any questions. \nauthour : {ctx.author.mention}'
        await channel.send(embed=e)
    else :
        e = Embed(title='Player data not fount' , colour=Color.red())
        e.description = f'Please link the {member.mention} with the game tag to proced```{client.command_prefix}link #tag```'
        await ctx.send(embed=e)
        return


@client.command(name="re" , aliases=['re-apply'] , help="Move player to reapply " ,
                usage="re <member-mention> [new_nickname] \n\tor\t\n re <member-mention>")
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
async def re(ctx , member: discord.Member , * , new_nickname=None) :
    await ctx.message.delete()
    if new_nickname is None :
        await member.edit(nick=f"re - {member.name}")
    else :
        await member.edit(nick=f"{new_nickname}")
    await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
    info = {1054435038881665024 : ['re - apply' , 1055440286806966322] ,
            1152220160028057660 : ['UN-Qualified' , 1152228011798700092]}
    await member.add_roles(discord.utils.get(ctx.guild.roles , name=info[ctx.guild.id][0]))
    channel = client.get_channel(info[ctx.guild.id][1])
    await channel.send(f"{member.mention} has been sent to re-apply by {ctx.author.mention}")
    e = Embed(title="RE-APPLY \nYou have been Placed here due to the Following Reasons\n" , color=Color.random())
    e.description = f'• You have been Inactive from a Long time in our Clans. \n ' \
                    f'• You Left without informing your Clans Leader/Co-Leader.\n' \
                    f'• Your Activity seems Suspicious in the Server.\n' \
                    f'• If you wish to reapply and join us again\n\n' \
                    f'**Do the following**\n' \
                    f'• Ping one of clan leaders using @thiername\n' \
                    f'• Or just type " I need help reapplying "\n' \
                    f'• We will assist you further, be kind and wait until we reply.'
    await channel.send(embed=e)


class Myview(View) :
    def __init__(self , ctx) :
        super().__init__(timeout=40)
        self.ctx = ctx

    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji='✅')
    async def button_callback(self , interaction: discord.Interaction , button: discord.ui.button) :
        self.clear_items()
        await interaction.response.edit_message(view=self)
        if self.ctx.message.mentions :
            await approve(self.ctx , self.ctx.message.mentions[0])
            info = {1054435038881665024 : 1055439744739315743 , 1152220160028057660 : 1167482592254238740}
            await self.ctx.send(f'Moved to <#{info[self.ctx.guild.id]}> ')
        else :
            await self.ctx.send(f'succefully checked')

    async def interaction_check(self , interaction) -> bool :
        if interaction.user != self.ctx.author :
            await interaction.response.send_message(f"only {self.ctx.author.mention} can approve this " ,
                                                    ephemeral=True)
            return False
        else :
            return True


@client.command(name='check' , help='check the player with chocolate clash' , usage=f'{p}check <@mention> or <#tag>')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
async def check(ctx , * , target=None) :
    if target is None :
        e = Embed(title="Please provide a user mention or ID." , color=Color.random())
        await ctx.send(embed=e)
        return
    else :
        if ctx.message.mentions :
            user = ctx.message.mentions[0].id
            with open('userdata.pkl' , 'rb') as f :
                data = pickle.load(f)
            tags = data[user]
        else :
            tags = target
            tags = tags.strip('#')

        try :
            if ctx.channel.id in [1055439542863274038 , 1165189096214368257] :
                opt = Options()
                opt.add_argument('--headless')
                opt.add_argument('--no-sandbox')
                driver = webdriver.Chrome(options=opt)
                clink = 'https://fwa.chocolateclash.com/cc_n/member.php?tag=%23' + tags
                coslink = 'https://www.clashofstats.com/players/' + tags
                driver.get(clink)
                div_element = driver.find_element('css selector' , '#top')
                screenshot = div_element.screenshot_as_png
                screenshot_bytes = io.BytesIO(screenshot)
                screenshot_bytes.seek(0)
                driver.quit()
                e = Embed(title=f'  #{tags} \n\n' , color=Color.blue())
                e.description = f'[**CHOCOLATE CLASH**]({clink}) \n\n[**CLASH OF STATS**]({coslink}) \n' \
                                f'\n**❯** Check the palyer is **Banned** or not ,then confirm the base is correct.'
                screenshot_file = discord.File(screenshot_bytes , filename="screenshot.png")
                e.set_image(url="attachment://screenshot.png")
                e.set_footer(text=f"Requested by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
                await ctx.send(embed=e , file=screenshot_file , view=Myview(ctx))

            else :
                raise Exception('Not in correct channel ?')

        except Exception as er :
            clink = 'https://fwa.chocolateclash.com/cc_n/member.php?tag=%23' + tags
            coslink = 'https://www.clashofstats.com/players/' + tags
            e = Embed(title=f"{tags} \n\n" , color=Color.blue())
            e.description = f'[**CHOCOLATE CLASH**]({clink}) \n\n[**CLASH OF STATS**]({coslink})  \n'
            e.set_footer(text=f"Requested by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e)
            return


@client.command()
async def emoji(ctx) :
    await ctx.send("<:blueBadge:1007628410375372892>")


''''
                                        coc
'''


@client.command(name='link' , help='To link your clash of clans account with your discord account' ,
                usage=f'{p}link <#player_tag> \nexample : {p}link #2UVH89FH')
async def link(ctx , tag=None) :
    await ctx.message.delete()
    if tag is None :
        e = Embed(title="Please provide the player tag ." , color=Color.random())
        await ctx.send(embed=e)
        return
    else :
        tag = tag.strip('#')
        with open('userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if ctx.author.id in user_data.keys() :
            e = Embed(title="You have already linked your account <:ver:1157952898362261564>" , colour=Color.random())
            await ctx.send(embed=e)
            await ctx.send()
            return
        else :
            player = COC.get_user(tag=tag)
            e = Embed(
                title=f'<:th{str(player["townHallLevel"])}:{COC.get_id(player["townHallLevel"])}>  {player["name"]} -{player["tag"]}' ,
                color=Color.random())
            e.description = f'\n<:ver:1157952898362261564> Linked {player["tag"]} to {ctx.author.mention}'
            e.set_footer(text=f"Linked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e)
            user_data[ctx.author.id] = tag
            with open('userdata.pkl' , 'wb') as file :
                pickle.dump(user_data , file)
            return


@client.command(name='unlink' , help='To unlink your clash of clans account with your discord account' ,
                usage=f'{p}unlink <none> or <@mention>')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
async def unlink(ctx , member: discord.Member) :
    with open("userdata.pkl" , "rb") as file :
        user_data = pickle.load(file)

    if member.id in user_data.keys() :
        tag = user_data[member.id]
        player = COC.get_user(tag=tag)
        try :
            del user_data[member.id]
        except :
            user_data.pop(member.id)
        e = Embed(
            title=f'<:th{str(player["townHallLevel"])}:{COC.get_id(player["townHallLevel"])}>  {player["name"]} -{player["tag"]}' ,
            color=Color.random())
        e.description = f'\n<:ver:1157952898362261564>  {player["tag"]} Unlinked with {member.mention}  '
        e.set_footer(text=f"Unlinked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
        await ctx.send(embed=e)
        with open("userdata.pkl" , "wb") as file :
            pickle.dump(user_data , file)


@client.command(name='force_link' , aliases=['fl' , 'force-link' , 'force'] ,
                help='To  link a player clash of clans account with a discord account' ,
                usage=f'{p}force_link <@mention> <#player_tag> \nexample : {p}force_link @moon #JJ0Y71L2' , hidden=True)
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
async def force_link(ctx , member: discord.Member = None , tag=None) :
    await ctx.message.delete()
    if tag is None :
        e = Embed(title="Please provide the player tag ." , color=Color.red())
        await ctx.send(embed=e)
        return
    else :
        tag = tag.strip('#')
        with open('userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if member.id in user_data.keys() :
            e = Embed(title=f"{member.mention} have already linked his account <:ver:1157952898362261564>" ,
                      colour=Color.random())
            await ctx.send(embed=e)
            await ctx.send()
            return
        else :
            player = COC.get_user(tag=tag)
            e = Embed(
                title=f'<:th{str(player["townHallLevel"])}:{COC.get_id(player["townHallLevel"])}>  {player["name"]} -{player["tag"]}' ,
                color=Color.random())
            e.description = f'\n<:ver:1157952898362261564> Linked {player["tag"]} to {member.mention}'
            e.set_footer(text=f"Linked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e)
            user_data[member.id] = tag
            with open('userdata.pkl' , 'wb') as file :
                pickle.dump(user_data , file)
            return


@client.command(name="profile" , help="Shows the profile of the user" ,
                usage=f"{p}profile <none> or <user> \nexample: {p}profile @user")
async def profile(ctx , * , target=None) :
    with open('userdata.pkl' , 'rb') as f :
        user_data = pickle.load(f)
    if target is None :
        if ctx.author.id in user_data.keys() :
            tags = user_data[ctx.author.id].strip('#')
        else :
            e = Embed(title="Please provide a user mention or ID." , color=Color.red())
            await ctx.send(embed=e)
            return
    else :
        if ctx.message.mentions :
            user = ctx.message.mentions[0].id
            if user in user_data :
                tags = user_data[user].strip('#')
            else :
                e = Embed(title="User not found " , color=Color.red())
                await ctx.send(embed=e)
                return
        else :
            tags = target.strip('#')

    try :
        player = COC.get_user(tag=tags)
        url = f'https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23{player["tag"].strip("#")}'
        e = Embed(title=f"{player['name']} - {player['tag']}" , url=url , color=Color.random())
        emoj = discord.utils.get(ctx.guild.emojis , id=int(COC.get_id(player["townHallLevel"])))
        ptag = player["tag"].strip('#')
        x = f'[{player["clan"]["name"]}](https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{player["clan"]["tag"]}) \n Role : **{COC.get_role(player["role"])}**' if "clan" in player else "NO clan"
        e.set_thumbnail(url=emoj.url)
        e.description = f'[CCNS](https://fwa.chocolateclash.com/cc_n/member.php?tag=%23{ptag})   [COS](https://www.clashofstats.com/players/{ptag})\n' \
                        f'\n🏆 {player["trophies"]} \n{x}'

        e.set_footer(text=f"Done by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
        await ctx.send(embed=e)
    except Exception as e :
        e = Embed(title="Error while fe tching" , color=Color.red())
        e.description = str(e)
        await ctx.send(embed=e)


@client.command(name='server_list' , aliases=['sl' , 'server-list'] ,
                help='Shows the list of servers linked to the bot' , usage=f'{p}server_list' , hidden=True)
async def server_list(ctx) :
    await ctx.message.delete()
    with open('userdata.pkl' , 'rb') as f :
        user_data = pickle.load(f)
    user_text = ""
    e = Embed(title="Server List" , color=Color.blue())
    for i in user_data.keys() :
        user_name = await client.fetch_user(int(i))
        user_name = user_name.display_name
        user_text += f'{user_name}  : {user_data[i]} \n'
    e.description = user_text
    e.add_field(name="Server Count" , value=len(user_data) , inline=False)
    e.set_footer(text=f"Requested by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
    await ctx.send(embed=e)


@client.command(name="clan" , help="shows the information of the clan" ,
                usage=f"{p}clan <none> optionol : <clan_tag> \nexample : {p}clan #2Q8URCU88")
async def clan(ctx , target=None) :
    await ctx.message.delete()
    clantag = None
    tags = None
    clanroles = ['WAL' , 'TSL' , 'SNL' , 'WAC' , 'TSC' , 'SNC' , 'SML' , 'SMC']
    lead = {'2Q8URCU88' : 1034730502701203467 , 'U0LPRYL2' : 775168480969621586 , 'LLGJUPPY' : 697865882256408726 ,
            'Y0YY9GUV' : 613736734462836738 , '2LV0UJ28V' : 697865882256408726}
    if target is None or ctx.message.mentions :
        with open('userdata.pkl' , 'rb') as f :
            user_data = pickle.load(f)
        if ctx.message.mentions :
            idd = ctx.message.mentions[0].id
        else :
            idd = ctx.author.id

        if idd in user_data.keys() :
            tags = user_data[idd]

        elif any(role.name in clanroles for role in ctx.author.roles) :
            if any(role.name in ["WAC" , "WAL"] for role in ctx.author.roles) :
                clantag = "2Q8URCU88"
            elif any(role.name in ["TSC" , "TSL"] for role in ctx.author.roles) :
                clantag = "U0LPRYL2"
            elif any(role.name in ["SNC" , "SNL"] for role in ctx.author.roles) :
                clantag = "Y0YY9GUV"
            elif any(role.name in ["SMC" , "SML"] for role in ctx.author.roles) :
                clantag = "LLGJUPPY"

    else :
        if len(target) <= 3 :
            ctags = {'w' : "2Q8URCU88" , "ts" : "U0LPRYL2" , "sns" : "Y0YY9GUV" , "sav" : "LLGJUPPY"}
            clantag = ctags[target]
        elif len(target) >= 4 :
            clantag = target.strip('#')
        else :
            e = Embed(title="Please provide a clan tag or LINK your profile" , color=Color.red())
            await ctx.send(embed=e)
            return
    if clantag is None and tags is not None :
        clantag = COC.get_user(tag=tags)["clan"]["tag"].strip("#")
    clt = COC.getclan(tag=clantag)
    e = Embed(title=f'**{clt["name"]}** - {clt["tag"]}' ,
              url=f'https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{clt["tag"].strip("#")}' ,
              color=Color.random())
    e.set_thumbnail(url=clt["badgeUrls"]["large"])
    ccns = f'https://fwa.chocolateclash.com/cc_n/clan.php?tag={clt["tag"].strip("#")}'
    fwa = "https://sites.google.com/site/fwaguide/"
    cwl = "https://clashofclans.fandom.com/wiki/Clan_War_Leagues"
    cos = f'https://www.clashofstats.com/clans/{clt["tag"].strip("#")}'
    e.description = f'**Info** :\n\n' \
                    f'<:ccns:1159494607760003132> [**Clash of stats**]({cos})\n' \
                    f'💎 [**FWA**]({fwa})\n' \
                    f'<:see:1159496511701385297> [**CCNS**]({ccns})\n' \
                    f'⚔️ [**CWL**]({cwl})\n\n' \
                    f'<:cp:1161299634916966400> : {clt["clanCapital"]["capitalHallLevel"]}    ' \
                    f' <:members:1161298479050670162> : {clt["members"]}/50\n\n' \
                    f'<:saw:1159496168347291698> **Leader**  : \n<@{lead[clt["tag"].strip("#")] if clt["tag"].strip("#") in lead.keys() else "UNKOWN"}>!'
    await ctx.send(embed=e)


@client.command(name='war' , help="war announcement either win or loose or mis match or blacklist clan war" ,
                usage=f"{p}war <win/loose/mismatch/bl> \nexample : {p}war win ,{p}war loose")
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
async def war(ctx , target=None) :
    cid = ctx.channel.category.id
    cidinfo = {1054453503084482580 : ["U0LPRYL2" , 1055418276546629682 , 'THE SHIELD'] ,
               1054458642541334599 : ["2Q8URCU88" , 1055418808833159189 , 'WARNING']}
    await ctx.message.delete()
    if cid in cidinfo.keys() :
        clani = COC.getclan(tag=f"{cidinfo[cid][0]}/currentwar")
    else :
        e = Embed(title="This command wont work here" , color=Color.red())
        await ctx.send(embed=e)
        return
    if target is None :
        e = Embed(title="Check and try again" , color=Color.red())
        await ctx.send(embed=e)
        return
    else :
        your_clan_image_url = clani["clan"]["badgeUrls"]["medium"]
        opponents_clan_image_url = clani["opponent"]["badgeUrls"]["medium"]
        your_clan_image = Image.open(BytesIO(requests.get(your_clan_image_url).content))
        opponents_clan_image = Image.open(BytesIO(requests.get(opponents_clan_image_url).content))
        if target.startswith(("w" , "W")) :
            path = r'templates/win.png'
        elif target.startswith(("l" , "L")) :
            path = r'templates/loose.png'
        elif target.startswith(("m" , "M")) :
            path = r'templates/mis.png'
        elif target.startswith(("b" , "B")) :
            path = r'templates/bl.png'
        else :
            e = Embed(title="Nothing found" , color=Color.red())
            await ctx.send(embed=e)
            return
        template = Image.open(path)
        template.paste(your_clan_image , (80 , 50) , mask=your_clan_image)
        template.paste(opponents_clan_image , (1000 , 50) , mask=opponents_clan_image)
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(r'ArialUnicodeMS.ttf' , 40)
        text = [clani["clan"]["name"] , clani["opponent"]["name"]]
        x = [86 , 697]
        for i in range(len(x)) :
            box_x , box_y , box_width , box_height = x[i] , 300 , 495 , 52
            text_bbox = draw.textbbox((box_x , box_y) , text[i] , font=font)
            text_x = box_x - 10 + (box_width - (text_bbox[2] - text_bbox[0])) // 2
            text_y = box_y - 10 + (box_height - (text_bbox[3] - text_bbox[1])) // 2
            draw.text((text_x , text_y) , text[i] , fill=(0 , 0 , 0) , font=font)
        image_bytes = BytesIO()
        template.save(image_bytes , format="PNG")
        image_bytes.seek(0)
        await ctx.send(f'Hey , <@&{cidinfo[cid][1]}>')
        await ctx.send(file=discord.File(image_bytes , filename="template.png"))


@client.command(name="cwl" , help="get clan war league clan info" ,
                usage=f"{p}cwl <tag> <th level> \neg :{p}cwl #2Q8URCU88 12 13 14")
async def cwl(ctx , tag=None , *th) :
    await ctx.message.delete()
    if tag is None :
        e = Embed(title="Please provide a tag." , color=Color.red())
        await ctx.send(embed=e)
        return
    else :
        tag = tag.strip("#")
        clt = COC.getclan(tag=tag)
        e = Embed(title=f'**{clt["name"]}** - {clt["tag"]}' ,
                  url=f'https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{clt["tag"].strip("#")}' ,
                  color=Color.random())
        e.set_thumbnail(url=COC.leaugeid(clt["warLeague"]["id"]))
        ths = '\n'.join([f'TH : {thvalue}  <:th{thvalue}:{COC.get_id(int(thvalue))}>' for thvalue in th])
        print(ths)
        e.description = f'\n**Info** :\n\n{clt["description"]} '
        e.add_field(name="\n\n**Town hall**\n" , value=f' {ths}')
        await ctx.send(embed=e)


@client.command(name="bases" , help="offical fwa bases" , usage=f"{p}bases")
async def bases(ctx) :
    await ctx.message.delete()
    url15 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH15%3AWB%3AAAAAKQAAAAIPb7TMztzbem-F0y7oXluK"
    url14 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH14%3AWB%3AAAAAQAAAAAG_WV2seLzVBV38HVTPRJCY"
    url13 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH13%3AWB%3AAAAAKwAAAAH9cXxV00w-5lJ2qCJCm8_v"
    url12 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH12%3AWB%3AAAAACwAAAAIzCgaxwgW1UGFUuSFMFvCu"
    url11 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH11%3AWB%3AAAAAKgAAAAH9X8-koI5OUOzBGQx4SKwQ"
    embed = discord.Embed(title="💎 List of all FWA bases" ,
                          description=f"❯ Base: `TownHall 15`\n❯ Link: [Click here for TH15 FWA Base]({url15})\n\n❯ Base: `TownHall 14`\n❯ Link: [Click here for TH14 FWA Base]({url14})\n\n❯ Base: `TownHall 13`\n❯ Link: [Click here for TH13 FWA Base]({url13})\n\n❯ Base: `TownHall 12`\n❯ Link: [Click here for TH12 FWA Base]({url12})\n\n❯ Base: `TownHall 11`\n❯ Link: [Click here for TH11 FWA Base]({url11})\n\nFor detailed infos about our bases, type: !th11 - !th12 - !th13 - !th14 or !th15")
    embed.set_thumbnail(
        url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEO0d84HSbpwy1s8PGoAg3gT6ksu_MeytKAg&usqp=CAU")
    await ctx.send(embed=embed)


@client.command(name="bl-support")
async def bl_support(ctx) :
    clanroles = ['WAL' , 'TSL' , 'SNL' , 'WAC' , 'TSC']
    if ctx.message.mentions :
        if not any(role in clanroles for role in ctx.author.roles) :
            mentioned_user = ctx.message.mentions[0]
            await ctx.send(f'{mentioned_user.nick} \nmoved to blacklist support 🚀')
            await mentioned_user.add_roles(discord.utils.get(ctx.guild.roles , name='bl-war'))
        else :
            return
    else :
        await ctx.send(f'{ctx.author.nick} \nmoved to blacklist support 🚀')
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles , name='bl-war'))


@client.command(name="revoke")
async def revokee(ctx) :
    if isinstance(ctx.channel , discord.TextChannel) :
        role = discord.utils.get(ctx.guild.roles , name='bl-war')
        for member in ctx.channel.members :
            if role in member.roles :
                await member.remove_roles(role)
                await member.send(f'Thanks for your support in the blacklist war  🫡')


@client.command(name='usage' , aliases=['u'])
async def usage(ctx , command_name: str) :
    await ctx.message.delete()
    command = client.get_command(command_name)
    if command :
        help_info = f"```command : {ctx.prefix}{command.name}\nabout  : {command.help}\n\nusage  : {command.usage}```"
        await ctx.send(help_info)
    else :
        await ctx.send("Command not found. Please provide a valid command name.")


if __name__ == '__main__' :
    keep_alive()
    client.run(keyy)
