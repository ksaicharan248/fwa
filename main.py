import discord
from discord.ext import commands
from discord import Embed , Color
import webser
from webser import keep_alive

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
    else :
        raise error


@client.event
async def on_member_join(member) :
    welcome_channel_id = 1154448688056385689
    welcome_channel = client.get_channel(welcome_channel_id)
    if welcome_channel :
        await welcome_channel.send(f'Hello, {member.mention} !')
        embed = Embed(title=f"Welcome {member.mention} to to 🛡 — THE SHIELD —🛡 !" , color=Color.green())
        embed.description = f"You can read our rules and details about 💎FWA💎 in {client.get_channel(1154470458314457178).mention} \n\n If you wish to " \
                            f"join one of our clans then please follow the steps below.\n\n**•Step 1** : Post your " \
                            f"PLAYER tag\n**•Step 2** : Post a picture of My Profile tab\n**•Step 3**: Post a picture " \
                            f"of your 💎FWA💎 base \nIf you don’t have a 💎FWA💎 base then you can trigger \n```!th#```\n(" \
                            f"Replace # with your townhall level) OR visit  " \
                            f"{client.get_channel(1154470491856314378).mention}\n**•Step 4**: Have some patience, " \
                            f"you will be assisted shortly.\n\n We may not have an instant space but **ASAP** we have " \
                            f"a space, we will recruit you. Till then we will put you in " \
                            f"{client.get_channel(1154470512257413210).mention} \n\n🚨Note - We don’t recruit FWA " \
                            f"BANNED players."
        await welcome_channel.send(embed=embed)


@client.command(name='wel')
async def welcome(ctx , member: discord.Member) :
    await ctx.send(f'Hello, {member.mention} !')
    embed = Embed(title=f"Welcome {member.mention} to to 🛡 — THE SHIELD —🛡 !" , color=Color.brand_green())
    embed.description = f"You can read our rules and details about 💎FWA💎 in {client.get_channel(1003969955001274429).mention} \n\n If you wish to " \
                        f"join one of our clans then please follow the steps below.\n\n**•Step 1** : Post your " \
                        f"PLAYER tag\n**•Step 2** : Post a picture of My Profile tab\n**•Step 3**: Post a picture " \
                        f"of your 💎FWA💎 base \nIf you don’t have a 💎FWA💎 base then you can trigger \n```!th#```\n(" \
                        f"Replace # with your townhall level) OR visit  " \
                        f"{client.get_channel(1004071348617887774).mention}\n**•Step 4**: Have some patience, " \
                        f"you will be assisted shortly.\n\n We may not have an instant space but **ASAP** we have " \
                        f"a space, we will recruit you. Till then we will put you in " \
                        f"{client.get_channel(1004121615891705948).mention} \n\n🚨Note - We don’t recruit FWA " \
                        f"BANNED players."

    await ctx.send(embed=embed)


@client.command()
async def ping(ctx) :
    print(ctx)
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
@commands.has_any_role("admin" , "red")
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
@commands.has_any_role("admin" , "red")
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
@commands.has_role("admin")  # Replace with the role that has permission to change nicknames
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
@commands.has_role('admin')
async def rmrole(ctx , member: discord.Member) :
    try :
        await member.remove_roles(discord.utils.get(ctx.guild.roles , name='red'))
        await member.remove_roles(discord.utils.get(ctx.guild.roles , name='yellow'))
    except commands.MissingRole :
        await ctx.send("You don't have the required role.")


@client.command()
@commands.has_role('admin')
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
        channel = client.get_channel(1154470458314457178)
        try :
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='TSC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            await member.remove_roles(discord.utils.get(ctx.guild.roles , name='🔸ENTRY🔸'))
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
            await channel.send(f"{member.mention} is the member of THE SHIELD")
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


@client.command(name='hs-m')
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'HML')
async def ts_m(ctx , member: discord.Member , * , new_nickname) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1063291093178916884)
        try :
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='red'))
            await member.remove_roles(discord.utils.get(ctx.guild.roles , name='yellow'))
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
            await channel.send(f"{member.mention} is the member of HINDU SAMRAJYA")
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
async def ts_m(ctx , member: discord.Member , * , new_nickname) :
    if ctx.author.guild_permissions.manage_messages :
        await ctx.message.delete()
        channel = client.get_channel(1055527254643445812)
        try :
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='WAC'))
            await member.add_roles(discord.utils.get(ctx.guild.roles , name='🔰THE FARMERS MEMBERS🔰'))
            await member.remove_roles(discord.utils.get(ctx.guild.roles , name='🔸ENTRY🔸'))
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
            await channel.send(f"{member.mention} is the member of ♠️WARNING♠️")
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


@client.command()
async def emoji(ctx) :
    await ctx.send("<:Super_bowler:1138182991877775370>")


if __name__ == '__main__' :
    keep_alive()
    client.run('MTE1NDM4MTA1NjkwMDg3MDE3NA.GdXsKN.xo3qCy4rkuMWFb_gVvkbLwDSgjWpZFOvxtDkG4')
