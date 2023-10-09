import io
import discord
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

client.remove_command('help')


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
    if isinstance(error , commands.CommandInvokeError) and isinstance(error.original , discord.HTTPException) :
        embed = discord.Embed(title="WARNING ⚠️⚠️⚠️" , description="something is missing please check and try again." ,
                              color=discord.Color.red())
        await ctx.send(embed=embed)

    else :
        raise error


@client.event
async def on_member_join(member) :
    welcome_channel = client.get_channel(1055439542863274038)
    if welcome_channel :
        await member.add_roles(discord.utils.get(member.guild.roles , name='🔸ENTRY🔸'))
        await welcome_channel.send(f'Hello, {member.mention} !')
        embed = Embed(title=f"Welcome {member.mention} to to 🛡 — THE SHIELD —🛡 !" , color=Color.green())
        embed.description = f"You can read our rules and details about 💎FWA💎 in {client.get_channel(1054438569378332754).mention} \n\n If you wish to " \
                            f"join one of our clans then please follow the steps below.\n\n**•Step 1** : Post your " \
                            f"PLAYER tag\n**•Step 2** : Post a picture of My Profile tab\n**•Step 3**: Post a picture " \
                            f"of your 💎FWA💎 base \nIf you don’t have a 💎FWA💎 base then you can trigger \n```!th#```\n(" \
                            f"Replace # with your townhall level) OR visit  " \
                            f"{client.get_channel(1054438501233479760).mention}\n**•Step 4**: Have some patience, " \
                            f"you will be assisted shortly.\n\n We may not have an instant space but **ASAP** we have " \
                            f"a space, we will recruit you. Till then we will put you in " \
                            f"{client.get_channel(1055439744739315743).mention} \n\n🚨Note - We don’t recruit FWA " \
                            f"BANNED players."
        await welcome_channel.send(embed=embed)


@client.command(name='help')
async def help(ctx) :
    p = client.command_prefix
    embed = discord.Embed(
        description=f"{p}wel                - Welome player\n{p}ping               - Show latency\n{p}help               - Show help\n{p}role                - Add role\n{p}rm                  - Remove role\n{p}changenick  - Change nickname\n{p}changenick  - remove nick name" ,
        colour=0x1f7f5f)

    embed.add_field(name="LEADER COMMANDS" ,
                    value=f"`ts-m`         -  add player to The shield\nusage:  {p}ts-m  @mention Mb/Eld - IGN\n\n`hs-m`         - add player to HINDU SAMRAJYA\nusage:  {p}hs-m  @mention Mb/Eld - IGN\n\n`wa-m`         - add player to warning \nusage:  {p}wa-m  @mention Mb/Eld - IGN\n\n`unq`         - add player to unqualify\nusage:  {p}unq  @mention  IGN\n\n`app`       -  approve the player\nusage -  {p}app @mention TH - IGN\n\n`re`         - send the player to reapply \nusage : {p}re @mention  IGN\n\n`check`        - check the player with chocolate clash\nusage : {p}check playertag \nNOTE : if linked mention player \n\n `force_link`        - link any other player with tag \nusage :||{p}force_link   @mention   #player_tag`||" ,
                    inline=False)
    embed.add_field(name="PLAYER COMMANDS" ,
                    value=f"`link`          - link the bot with player tag \nusage : {p}link  #**player_tag**  "
                          f" \n\n`profile`         - profile of player" , inline=False)

    await ctx.send(embed=embed)


@client.command(name='wel')
async def welcome(ctx , member: discord.Member) :
    await ctx.send(f'Hello, {member.mention} !')
    embed = Embed(title=f"Welcome {member.mention} to to 🛡 — THE SHIELD —🛡 !" , color=Color.brand_green())
    embed.description = f"You can read our rules and details about 💎FWA💎 in {client.get_channel(1054438569378332754).mention} \n\n If you wish to " \
                        f"join one of our clans then please follow the steps below.\n\n**•Step 1** : Post your " \
                        f"PLAYER tag\n**•Step 2** : Post a picture of My Profile tab\n**•Step 3**: Post a picture " \
                        f"of your 💎FWA💎 base \nIf you don’t have a 💎FWA💎 base then you can trigger \n```!th#```\n(" \
                        f"Replace # with your townhall level) OR visit  " \
                        f"{client.get_channel(1054438501233479760).mention}\n**•Step 4**: Have some patience, " \
                        f"you will be assisted shortly.\n\n We may not have an instant space but **ASAP** we have " \
                        f"a space, we will recruit you. Till then we will put you in " \
                        f"{client.get_channel(1055439744739315743).mention} \n\n🚨Note - We don’t recruit FWA " \
                        f"BANNED players."

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
        embed = Embed(title="Nickname changed" , color=Color.green())
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
        embed = Embed(title="Nickname Removed" , color=Color.red())
        embed.add_field(name="User" , value=member.mention , inline=False)
        embed.add_field(name="Moderator" , value=ctx.author.mention , inline=False)

        await ctx.send(embed=embed)
    except discord.Forbidden :
        await ctx.send("I do not have permission to remove the user's nickname.")
    except discord.HTTPException :
        await ctx.send("An error occurred while removing the user's nickname.")


@client.command(name='ts-m')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'TSL')
async def ts_m(ctx , member: discord.Member , * , new_nickname) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1055527200193007626)
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='TSC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            embed = Embed(color=Color.green())
            embed.description = f"✅Changed roles for {member.name}, +TSC, +🔰THE FARMERS MEMBERS🔰,-🔸ENTRY🔸"
            await channel.send(embed=embed)
            flag1 = True
        except :
            embed = Embed(color=Color.red())
            embed.description = f"❌Failed to change roles for {member.name} "
            await channel.send(embed=embed)
            flag1 = False
        try :
            await member.edit(nick=new_nickname)
            embed1 = Embed(color=Color.green())
            embed1.description = f"✅Changed name for {member.name} to  {member.mention}"
            await channel.send(embed=embed1)
            flag2 = True
        except :
            embed1 = Embed(color=Color.red())
            embed1.description = f"❌Failed to change name for {member.name} "
            await channel.send(embed=embed1)
            flag2 = False

        if flag1 and flag2 :
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


@client.command(name='hs-m')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'HML')
async def hs_m(ctx , member: discord.Member , * , new_nickname) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1063291093178916884)
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='HMC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            embed = Embed(color=Color.green())
            embed.description = f"✅Changed roles for {member.name}, +HMC, +🔰THE FARMERS MEMBERS🔰,-🔸ENTRY🔸"
            await channel.send(embed=embed)
            flag1 = True
        except :
            embed = Embed(color=Color.red())
            embed.description = f"❌Failed to change roles for {member.name} "
            await channel.send(embed=embed)
            flag1 = False
        try :
            await member.edit(nick=new_nickname)
            embed1 = Embed(color=Color.green())
            embed1.description = f"✅Changed name for {member.name} to  {member.mention}"
            await channel.send(embed=embed1)
            flag2 = True
        except :
            embed1 = Embed(color=Color.red())
            embed1.description = f"❌Failed to change name for {member.name} "
            await channel.send(embed=embed1)
            flag2 = False

        if flag1 and flag2 :
            await channel.send(f"{member.mention} is now a member of **HINDU SAMRAJYA**")
            embed3 = Embed(color=Color.green())
            embed3.description = ("🍻 Welcome, this is your clan chat.\n""Make sure to go through the followings -\n"
                                  "\n"
                                  "『📢』**clan-announcements** - For important clan announcements\n"
                                  "『⚠』**war-instructions** - For war rules and instructions\n"
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


@client.command(name='wa-m')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL')
async def wa_m(ctx , member: discord.Member , * , new_nickname) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1055527254643445812)
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='WAC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            embed = Embed(color=Color.green())
            embed.description = f"✅Changed roles for {member.name}, +WAC, +🔰THE FARMERS MEMBERS🔰,-🔸ENTRY🔸"
            await channel.send(embed=embed)
            flag1 = True
        except :
            embed = Embed(color=Color.red())
            embed.description = f"❌Failed to change roles for {member.name} "
            await channel.send(embed=embed)
            flag1 = False
        try :
            await member.edit(nick=new_nickname)
            embed1 = Embed(color=Color.green())
            embed1.description = f"✅Changed name for {member.name} to  {member.mention}"
            await channel.send(embed=embed1)
            flag2 = True
        except :
            embed1 = Embed(color=Color.red())
            embed1.description = f"❌Failed to change name for {member.name} "
            await channel.send(embed=embed1)
            flag2 = False

        if flag1 and flag2 :
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


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
async def unq(ctx , member: discord.Member , * , new_nickname=None) :
    await ctx.message.delete()
    if new_nickname is None :
        await member.edit(nick=f"unq - {member.name}")
    else :
        await member.edit(nick=f"{new_nickname}")
    await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
    await member.add_roles(discord.utils.get(ctx.guild.roles , name='unqualified❌'))
    channel = client.get_channel(1055440018279235657)
    await channel.send(f"{member.mention} has been unqualified by {ctx.author.mention}")
    e = Embed(title="UNQUALIFIED " , color=Color.dark_purple())
    e.description = f'⚠️ You have been placed here Because you havent Fulfill the Minimum Requirements to Apply to ' \
                    f'Join our Clans. To check our Requirements please type \n ➡️ !reqs \n\n🔍 We are always here also ' \
                    f'to Assist you.\n❌ Donot request to Join in Game unless Instructed to do so\n🏛️You may stay in ' \
                    f'your current Clan or join a Random Clan while upgrading your base to Meet our Clan Requirements. ' \
                    f'But do not join any FWA Blacklisted clans.\n ✅When your requirements are met, type !wel \n ' \
                    f'\n**please follow all the instructions** \n authour : {ctx.author.mention}'

    await channel.send(embed=e)


@client.command(name='app')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
async def approve(ctx , member: discord.Member , * , new_nickname=None) :
    await ctx.message.delete()
    if new_nickname is None :
        await member.edit(nick=f"TH - {member.name}")
    else :
        await member.edit(nick=f"{new_nickname}")
    await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
    await member.add_roles(discord.utils.get(ctx.guild.roles , name='approved✅'))
    channel = client.get_channel(1055439744739315743)
    await channel.send(f"{member.mention} has been approved by {ctx.author.mention}")
    e = Embed(title="APPROVED " , color=Color.brand_green())
    e.description = f'🎯 Clan spots will be posted in this {client.get_channel(1055439744739315743).mention}, make sure to check it\n' \
                    f'🎯You will be **@notified** if a spot available for your TH level.\n🎯Just make sure to reply as fast as possible to ensure your spot.\n' \
                    f'🎯Donot request to join in game unless instructed to do so.\n' \
                    f'🎯You may stay in your **current clan** or join a random clan while waiting for a **spot**.\n' \
                    f'🎯Make sure to have **NO war timer** when you answer for spots.\n' \
                    f'🎯Ask in {client.get_channel(1126856734095462511).mention} if you have any questions. \n authour : {ctx.author.mention}'
    await channel.send(embed=e)


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
async def re(ctx , member: discord.Member , * , new_nickname=None) :
    await ctx.message.delete()
    if new_nickname is None :
        await member.edit(nick=f"re - {member.name}")
    else :
        await member.edit(nick=f"{new_nickname}")
    await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
    await member.add_roles(discord.utils.get(ctx.guild.roles , name='re - apply'))
    channel = client.get_channel(1055440286806966322)
    await channel.send(f"{member.mention} has been sent to re-apply by {ctx.author.mention}")
    e = Embed(title="RE-APPLY \n📛You have been Placed here due to the Following Reasons📛\n" , color=Color.gold())
    e.description = f'• You have been Inactive from a Long time in our Clans. \n ' \
                    f'• You Left without informing your Clans Leader/Co-Leader.\n' \
                    f'• Your Activity seems Suspicious in the Server.\n' \
                    f'• If you wish to reapply and join us again\n\n' \
                    f'**Do the following**\n' \
                    f'• Ping one of clan leaders using @thiername\n' \
                    f'• Or just type " I need help reapplying "\n' \
                    f'• We will assist you further, be kind and wait until we reply.'
    await channel.send(embed=e)


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML')
async def check(ctx , * , target=None) :
    if target is None :
        e = Embed(title="Please provide a user mention or ID." , color=Color.red())
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
            e = Embed(title="Member Check \n\n" , color=Color.blue())
            e.description = f'[**CHOCOLATE CLASH**]({clink}) \n\n[**CLASH OF STATS**]({coslink}) \n' \
                            f'📛 please check the palyer is **Banned** or not conform the base is correct.'
            screenshot_file = discord.File(screenshot_bytes , filename="screenshot.png")
            e.set_image(url="attachment://screenshot.png")

            e.set_footer(text=f"Requested by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e , file=screenshot_file)
        except Exception as e :
            clink = 'https://fwa.chocolateclash.com/cc_n/member.php?tag=%23' + tags
            coslink = 'https://www.clashofstats.com/players/' + tags
            e = Embed(title="Member Check \n\n" , color=Color.blue())
            e.description = f'[**CHOCOLATE CLASH**]({clink}) \n\n[**CLASH OF STATS**]({coslink}) \n' \
                            f'📛 please check and ensure the palyer is **Banned** or not,then conform the base is correct or not.'

            e.set_footer(text=f"Requested by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e)


@client.command()
async def emoji(ctx) :
    await ctx.send("<:Super_bowler:1138182991877775370>")


''''
                                        coc
'''


@client.command()
async def link(ctx , tag=None) :
    await ctx.message.delete()
    if tag is None :
        e = Embed(title="Please provide the player tag ." , color=Color.red())
        await ctx.send(embed=e)
        return
    else :
        tag = tag.strip('#')
        with open('userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if ctx.author.id in user_data.keys() :
            e = Embed(title="You have already linked your account <:ver:1157952898362261564>" , colour=Color.green())
            await ctx.send(embed=e)
            await ctx.send()
            return
        else :
            player = COC.get_user(tag=tag)
            e = Embed(
                title=f'<:th{str(player["townHallLevel"])}:{COC.get_id(player["townHallLevel"])}>  {player["name"]} -{player["tag"]}' ,
                color=Color.blue())
            e.description = f'\n<:ver:1157952898362261564> Linked {player["tag"]} to {ctx.author.mention}'
            e.set_footer(text=f"Linked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e)
            user_data[ctx.author.id] = tag
            with open('userdata.pkl' , 'wb') as file :
                pickle.dump(user_data , file)
            return


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML')
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
            color=Color.dark_gold())
        e.description = f'\n<:ver:1157952898362261564>  {player["tag"]} Unlinked with {member.mention}  '
        e.set_footer(text=f"Unlinked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
        await ctx.send(embed=e)
        with open("userdata.pkl" , "wb") as file :
            pickle.dump(user_data , file)


@client.command()
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML')
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
                      colour=Color.green())
            await ctx.send(embed=e)
            await ctx.send()
            return
        else :
            player = COC.get_user(tag=tag)
            e = Embed(
                title=f'<:th{str(player["townHallLevel"])}:{COC.get_id(player["townHallLevel"])}>  {player["name"]} -{player["tag"]}' ,
                color=Color.blue())
            e.description = f'\n<:ver:1157952898362261564> Linked {player["tag"]} to {member.mention}'
            e.set_footer(text=f"Linked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e)
            user_data[member.id] = tag
            with open('userdata.pkl' , 'wb') as file :
                pickle.dump(user_data , file)
            return


@client.command(name="profile")
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

    player = COC.get_user(tag=tags)
    url = f'https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23{player["tag"]}'
    e = Embed(title=f"{player['name']} - {player['tag']}" , url=url , color=Color.blue())
    emoj = discord.utils.get(ctx.guild.emojis , id=int(COC.get_id(player["townHallLevel"])))
    ptag = player["tag"].strip('#')
    x = f'[{player["clan"]["name"]}](https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{player["clan"]["tag"]}) \n Role : **{COC.get_role(player["role"])}**' if "clan" in player else "NO clan"
    e.set_thumbnail(url=emoj.url)
    e.description = f'[CCNS](https://fwa.chocolateclash.com/cc_n/member.php?tag=%23{ptag})   [COS](https://www.clashofstats.com/players/{ptag})\n' \
                    f'\n🏆 {player["trophies"]} \n{x}'

    e.set_footer(text=f"Done by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
    await ctx.send(embed=e)


@client.command()
async def server_list(ctx) :
    await ctx.message.delete()
    with open('userdata.pkl' , 'rb') as f :
        user_data = pickle.load(f)
    user_text = ""
    e = Embed(title="Server List" , color=Color.blue())
    for i in user_data.keys() :
        user_name = await client.fetch_user(int(i))
        user_text += f'{user_name}  : {user_data[i]} \n'
    e.description = user_text
    e.set_footer(text=f"Requested by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
    await ctx.send(embed=e)


@client.command("clan")
async def clan(ctx , target=None) :
    await ctx.message.delete()
    clantag = None
    tags = None
    clanroles = ['WAL' , 'TSL' , 'HML' , 'WAC' , 'TSC' , 'HMC']
    lead = {'2Q8URCU88' : 1034730502701203467 , 'U0LPRYL2' : 775168480969621586 , '9JYC9QU9' : 405705743967453184}
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
            elif any(role.name in ["HMC" , "HML"] for role in ctx.author.roles) :
                clantag = "9JYC9QU9"
    else :
        if len(target) == 1 :
            ctags = {'w' : "2Q8URCU88" , "s" : "U0LPRYL2" , "h" : "9JYC9QU9"}
            clantag = ctags[target]
        elif len(target) >= 2 :
            clantag = target.strip('#')
        else :
            e = Embed(title="Please provide a user mention or ID." , color=Color.red())
            await ctx.send(embed=e)
            return
    if clantag is None and tags is not None :
        clantag = COC.get_user(tag=tags)["clan"]["tag"].strip("#")
    clt = COC.getclan(tag=clantag)
    e = Embed(title=f'**{clt["name"]}** - {clt["tag"]}' ,
              url=f'https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{clt["tag"].strip("#")}' ,
              color=Color.blue())
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
                    f'<:saw:1159496168347291698> **Lead**  : \n<@{lead[clt["tag"].strip("#")] if clt["tag"].strip("#") in lead.keys() else "UNKOWN"}> '
    await ctx.send(embed=e)


@client.command()
async def war(ctx , target=None) :
    cid = ctx.channel.category.id
    cidinfo = {1054453503084482580 : "U0LPRYL2" , 1054458642541334599 : "2Q8URCU88"}
    await ctx.message.delete()
    if cid in cidinfo.keys() :
        clani = COC.getclan(tag=f"{cidinfo[cid]}/currentwar")
        clan_link = COC.getcoc(tag=clani['clan']['tag'])
        opponent_link = COC.getcoc(tag=clani['opponent']['tag'])
    else :
        e = Embed(title="This command wont work here" , color=Color.red())
        await ctx.send(embed=e)
        return
    if target is None :
        e = Embed(title="Check and try again" , color=Color.red())
        await ctx.send(embed=e)
        return
    else :
        if target.startswith(("w" , "W")) :
            e = Embed(title="🍻✌️WIN WAR✌️🍻 \n" , color=Color.green())
            e.description = f'\n[__**{clani["clan"]["name"].upper()}**__]({clan_link})    vs    [__**{clani["opponent"]["name"].upper()}**__]({opponent_link})\n\n**__WAR  INSTRUCTIONS__ :**\n\n⚔️1st attack on mirror (opposite same base) for **__3 stars__**🌟( must )\n\n⚔️2nd attack on BASE-1 for**__ 1 star__**🌟(After no. 1 take his mirror)\n\n🧹Clean up :  In last 12 hr. all bases are open for 3 stars🌟'
            e.set_footer(text=f"{clani['clan']['name'].upper()}" , icon_url=clani["clan"]["badgeUrls"]["large"])
            await ctx.send(embed=e)
        elif target.startswith(("l" , "L")) :
            embed = discord.Embed(title="LOOSE WAR 🏳️ \n" , colour=0xe60000)
            embed.description = f'\n[__**{clani["clan"]["name"].upper()}**__]({clan_link})    vs    [__**{clani["opponent"]["name"].upper()}**__]({opponent_link})\n\n**__WAR  INSTRUCTIONS __:**\n\n⚔️1st attack on mirror (opposite same base) for **__2 STARS__**🌟( Compulsory )\n\n⚔️2nd attack on BASE-1 for **__1 STAR__**🌟(After no. 1 take his mirror)\n\n🧹Clean up : In last 12 hr. all bases are open for 2 stars🌟'
            embed.set_footer(text=f"{clani['clan']['name'].upper()}" , icon_url=clani["clan"]["badgeUrls"]["large"])
            await ctx.send(embed=embed)

        else :
            e = Embed(title="Please provide a user mention or ID." , color=Color.red())
            await ctx.send(embed=e)
            return


@client.command()
async def cwl(ctx , tag=None , *,th) :
    ths = ''
    await ctx.message.delete()
    if tag is None :
        e = Embed(title="Please provide a tag." , color=Color.red())
        await ctx.send(embed=e)
        return
    else :
        clt = COC.getclan(tag=tag)
        e = Embed(title=f'**{clt["name"]}** - {clt["tag"]}' ,
                  url=f'https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{clt["tag"].strip("#")}' ,
                  color=Color.blue())
        e.set_thumbnail(url=COC.leaugeid(clt["warLeague"]["id"]))
        for thvalue in th :
            ths += f'<:th{thvalue}:{COC.get_id(thvalue)}> '
        e.description = f'\n**Info** :\n\n{clt["description"]} \n\n "__**Town hall**__"\n {ths}'
        await ctx.send(embed=e)


if __name__ == '__main__' :
    keep_alive()
    client.run(keyy)
