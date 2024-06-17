import io
from io import BytesIO
import discord
from discord.ext import commands
import COC
import typing
import pickle
from discord import Embed , Color
from discord.ui import Button , View , Select
from main import p
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Myview(View) :
    def __init__(self , ctx) :
        super().__init__(timeout=100)
        self.ctx = ctx

    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji='✅')
    async def button_callback(self , interaction: discord.Interaction , button: discord.ui.button) :
        self.clear_items()
        await interaction.response.edit_message(view=self)
        if self.ctx.message.mentions :
            cog_instance = self.ctx.bot.get_cog('ClanRoleAdder')
            if cog_instance :
                await cog_instance.approve(self.ctx , self.ctx.message.mentions[0])
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


class ClanRoleAdder(commands.Cog) :
    def __init__(self , client) :
        self.client = client

    @commands.command(name='app' , aliases=['approve'] , help='Move a member to Approved channel' ,
                      usage=f'{p}approve @member')
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
    async def approve(self , ctx , member: discord.Member) :
        with open('datasheets/userdata.pkl' , 'rb') as f :
            data = pickle.load(f)
        if member.id in data.keys() :
            user_info = COC.get_user(data[member.id]['tag'])
            await member.edit(nick=f'TH {user_info["townHallLevel"]} - {user_info["name"]} ')
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            channel_info = {1054435038881665024 : ['approved✅' , 1055439744739315743 , 1126856734095462511]}  # jigg
            await member.add_roles(discord.utils.get(ctx.guild.roles , name=channel_info[ctx.guild.id][0]))
            channel = self.client.get_channel(channel_info[ctx.guild.id][1])
            await channel.send(f"{member.mention} has been approved by {ctx.author.mention}")
            e = Embed(title="APPROVED " , color=Color.random())
            e.description = f'❯ Clan spots will be posted in this {self.client.get_channel(channel_info[ctx.guild.id][1]).mention}, make sure to check it\n' \
                            f'❯ You will be **@notified** if a spot available for your TH level.\n' \
                            f'❯ Just make sure to reply as fast as possible to ensure your spot.\n' \
                            f'❯ Donot request to join in game unless instructed to do so.\n' \
                            f'❯ You may stay in your **current clan** or join a random clan while waiting for a **spot**.\n' \
                            f'❯ Make sure to have **NO war timer** when you answer for spots.\n' \
                            f'❯ Ask in {self.client.get_channel(channel_info[ctx.guild.id][2]).mention} if you have any questions. \nDone by : {ctx.author.mention}'
            await channel.send(embed=e)
            if ctx.guild.id == 1054435038881665024 :
                await self.approve_waiting_list(ctx , level=int(user_info["townHallLevel"]) , up=True , down=False)

        else :
            e = Embed(title='Player data not fount' , colour=Color.red())
            e.description = f'Please link the {member.mention} with the game tag to proced```{self.client.command_prefix}link #tag```'
            await ctx.send(embed=e)
            return

    @commands.command(name='app-wl' , help="update the waiting list in approved channel")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
    async def approve_waiting_list(self , ctx , level=None , up=None , down=None) :
        with open('datasheets/waitinglist.pkl' , 'rb') as f :
            waiting_list = pickle.load(f)
        if level is not None :
            if up == True :
                waiting_list[level] += 1
            elif down == True :
                waiting_list[level] -= 1

        if level == 16 :
            channel = self.client.get_channel(1185800051105218720)
            await channel.edit(name=f"TH 16 : {waiting_list[16]}")
        elif level == 15 :
            channel = self.client.get_channel(1185806717603287102)
            await channel.edit(name=f"TH 15 : {waiting_list[15]}")
        elif level == 14 :
            channel = self.client.get_channel(1185806764164263998)
            await channel.edit(name=f"TH 14 : {waiting_list[14]}")
        elif level == 13 :
            channel = self.client.get_channel(1185806805423632405)
            await channel.edit(name=f"TH 13 : {waiting_list[13]}")
        elif level == 12 :
            channel = self.client.get_channel(1185806849631592600)
            await channel.edit(name=f"TH 12 : {waiting_list[12]}")
        elif level == 11 :
            channel = self.client.get_channel(1185806887292244079)
            await channel.edit(name=f"TH 11 : {waiting_list[11]}")
        elif level is None :
            channel = self.client.get_channel(1185800051105218720)
            await channel.edit(name=f"TH 16 : {waiting_list[16]}")
            channel = self.client.get_channel(1185806717603287102)
            await channel.edit(name=f"TH 15 : {waiting_list[15]}")
            channel = self.client.get_channel(1185806764164263998)
            await channel.edit(name=f"TH 14 : {waiting_list[14]}")
            channel = self.client.get_channel(1185806805423632405)
            await channel.edit(name=f"TH 13 : {waiting_list[13]}")
            channel = self.client.get_channel(1185806849631592600)
            await channel.edit(name=f"TH 12 : {waiting_list[12]}")
            channel = self.client.get_channel(1185806887292244079)
            await channel.edit(name=f"TH 11 : {waiting_list[11]}")
        else :
            pass
        with open('datasheets/waitinglist.pkl' , 'wb') as f :
            pickle.dump(waiting_list , f)

    @commands.command(name="announce")
    async def announce(self , ctx , message) :
        await ctx.message.delete()
        category_info = {1054453503084482580 : ["U0LPRYL2" , 1055418276546629682 , 'THE SHIELD'] ,
                         1054458642541334599 : ["2Q8URCU88" , 1055418808833159189 , 'WARNING']}
        category_id = ctx.channel.category.id
        await ctx.send(f'Hey , <@&{category_info[category_id][1]}>\n{message}')

    @commands.command(name='welcome',aliases=['wel'] , help='Welcome a player')
    async def welcome(self , ctx , member: discord.Member = None) :
        if member is None :
            await ctx.send('welcome !')
        else :
            await ctx.send(f'Hello, {member.mention} !')
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

    @commands.hybrid_command(name='check' , help='check the player with chocolate clash' ,
                             usage=f'{p}check <@mention> or <#tag>' , brief='leader')
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
    async def check(self , ctx , member: typing.Optional[discord.Member] = None ,
                    player_tag: typing.Optional[str] = None) :
        await ctx.defer()
        if player_tag is None and member is None :
            e = Embed(title="Please provide a user mention or ID." , color=Color.random())
            await ctx.send(embed=e)
            return
        else :
            user = member.id if member else (ctx.message.mentions[0].id if ctx.message.mentions else None)
            if user is not None :
                with open('datasheets/userdata.pkl' , 'rb') as f :
                    data = pickle.load(f)
                tags = data[user]['tag'].strip('#')
            elif player_tag is not None :
                tags = player_tag.strip('#')
            else :
                e = Embed(title="Member you are trying to  check does not have any proper profile tag" ,
                          color=Color.random())
                await ctx.reply(embed=e)
                return
            try :
                if ctx.channel.id in [1055439542863274038 , 1165189096214368257 , 1157946757309804604 ,
                                      1172782155772985425] :
                    if ctx.message.mentions or member :
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
                        e = Embed(title=f'{data[user]["name"]} -  #{tags} \n\n' , color=Color.blue())
                        e.description = f'[**CHOCOLATE CLASH**]({clink}) \n\n[**CLASH OF STATS**]({coslink}) \n' \
                                        f'\n**❯** Check the palyer is **Banned** or not ,then confirm the base is correct.'
                        screenshot_file = discord.File(screenshot_bytes , filename="screenshot.png")
                        e.set_image(url="attachment://screenshot.png")
                        e.set_footer(text=f"Requested by {ctx.author.display_name} " ,
                                     icon_url=ctx.author.display_avatar)
                        await ctx.reply(embed=e , file=screenshot_file , view=Myview(ctx))
                    else :
                        raise Exception("not mentioned user")

                else :
                    raise Exception('Not in correct channel ?')

            except Exception as er :
                clink = 'https://fwa.chocolateclash.com/cc_n/member.php?tag=%23' + tags
                coslink = 'https://www.clashofstats.com/players/' + tags
                e = Embed(title=f"{tags} \n\n" , color=Color.blue())
                e.description = f'[**CHOCOLATE CLASH**]({clink}) \n\n[**CLASH OF STATS**]({coslink})  \n'
                e.set_footer(text=f"Requested by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
                await ctx.reply(embed=e)

                return

    @commands.command(name="re" , aliases=['re-apply'] , help="Move player to reapply " ,
                      usage="re <member-mention> [new_nickname] \n\tor\t\n re <member-mention>")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
    async def re(self , ctx , *members: discord.Member ) :
        await ctx.message.delete()
        with open('datasheets/userdata.pkl' , 'rb') as f :
            data = pickle.load(f)
        for member in members:
            name = data[member.id]['name'] if member.id in data.keys() else member.name
            if name :
                await member.edit(nick=f"re - {name}")
            else :
                await ctx.send("Member not found")
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            info = {1054435038881665024 : ['re - apply' , 1055440286806966322] ,
                    1152220160028057660 : ['UN-Qualified' , 1152228011798700092]}
            await member.add_roles(discord.utils.get(ctx.guild.roles , name=info[ctx.guild.id][0]))
            channel = self.client.get_channel(info[ctx.guild.id][1])
            await channel.send(f"{member.mention} has been sent to re-apply by {ctx.author.mention}")
            e = Embed(title="RE-APPLY \nYou have been Placed here due to the Following Reasons\n" ,
                      color=Color.random())
            e.description = f'• You have been Inactive from a Long time in our Clans. \n ' \
                            f'• You Left without informing your Clans Leader/Co-Leader.\n' \
                            f'• Your Activity seems Suspicious in the Server.\n' \
                            f'• If you wish to reapply and join us again\n\n' \
                            f'**Do the following**\n' \
                            f'• Ping one of clan leaders using @thiername\n' \
                            f'• Or just type " I need help reapplying "\n' \
                            f'• We will assist you further, be kind and wait until we reply.'
            await channel.send(embed=e)

    @commands.command(name="unq" , aliases=["unqualified"] , help='Move a member to unqualifed ' ,
                      usage=f'{p}unq <@mention>')
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
    async def unq(self , ctx , member: discord.Member , * , new_nickname=None) :
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
        channel = self.client.get_channel(info[gid][1])
        await channel.send(f"{member.mention} has been unqualified by {ctx.author.mention}")
        e = Embed(title="UNQUALIFIED " , color=Color.random())
        e.description = f'⚠️ You have been placed here Because you havent Fulfill the Minimum Requirements to Apply to ' \
                        f'Join our Clans. To check our Requirements please type \n ➡️ </reqs:1240749660499476521> \n\n🔍 We are always here also ' \
                        f'to Assist you.\n❌ Donot request to Join in Game unless Instructed to do so\n🏛️You may stay in ' \
                        f'your current Clan or join a Random Clan while upgrading your base to Meet our Clan Requirements. ' \
                        f'But do not join any FWA Blacklisted clans.\n ✅When your requirements are met, type !wel \n ' \
                        f'\n**please follow all the instructions** \nauthour : {ctx.author.mention}'

        await channel.send(embed=e)

    @commands.hybrid_command(name='reqs' , help='shows requirements')
    async def ranimated(self , ctx) :
        embed = discord.Embed(
            title="<a:fire1:1221838889195409549>Minimum Requirements to Join us<a:fire1:1221838889195409549>" ,
            description="<a:r3:1221839351760031774> We Accept Only the Town Halls\n     <a:fire1:1221838889195409549>   <:th16:1184685970814156800> <:th15:1158776040525680694>  <:th14:1157934828784734299> <:th13:1157933611337666620>  <:th12:1157933184529469471> <a:fire1:1221838889195409549>\n\n<a:ra:1221838183378194563> We Don't take Rushed Base into our Team   Of Clans <a:th:1221839043340271617>\n\n<a:ra:1221838183378194563> We prefer non-rushed accounts but depending upon the weight of your base we can consider.\n\n<a:ra:1221838183378194563> You must have maxed Defenses, Heroes, Spells, and Troops of your prior townhall level.\n\n<a:ra:1221838183378194563> Meaning if you are Th12 and have Th11  Defenses, Heroes, Spells, and Troops levels it's acceptable.<a:tick33:1221843592826458232>\n\n<a:warn22:1221846589572780114> WE DON’T RECRUIT BANNED\nPLAYERS. <a:ban22:1221846452213645414>\n\n<a:spp:1221850353826529310> If You were ready with you base tag one of our Leaders/Co-Leaders <a:pin:1221838710719643668>" ,
            colour=discord.Colour.random())
        await ctx.send(embed=embed)




    @commands.command(name='move-clan' , aliases=['mc'] , help='Move a player to a specific clan chat' ,
                      usage=f'\n{p}move-clan <clan_name> <@mention> \n{p}move-clan tsm @moon\nclan_name are :\nbtm\navm\ntsm\nwam\nhgm\netc...')
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'BTL' , '☠️| LEADER' , 'Staff' , '🔰ADMIN🔰' ,
                           'GVL' , 'AVL' )
    async def move_clan(self , ctx , clan_name , member: discord.Member) :
        with open('datasheets/clan_deltails.pkl' , 'rb') as f :
            clan_data = pickle.load(f)
        if clan_name not in clan_data :
            valid_clans = '\n'.join([f"{key} - For {data['clan']}" for key , data in clan_data.items()])
            await ctx.send(f"Invalid clan name **{clan_name}**\n\nTry with one of the following:\n{valid_clans}" ,
                           ephemeral=True , delete_after=5)
            return
        await ctx.message.delete()
        channel_id = clan_data[clan_name]['channel_id']
        roles_to_add = clan_data[clan_name]['roles']
        clanInfo = clan_data[clan_name]['clan']

        channel = self.client.get_channel(channel_id)

        with open('datasheets/userdata.pkl' , 'rb') as f :
            data = pickle.load(f)

        if member.id in data.keys() :
            info = COC.get_user(data[member.id]['tag'])

        else :
            e = Embed(title='Player data not found' , colour=Color.red())
            e.description = f'Please link {member.mention} with the game tag to proceed```{self.client.command_prefix}link #tag```'
            await ctx.send(embed=e)
            return
        try :
            await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
            try :
                await member.add_roles(*[discord.utils.get(ctx.guild.roles , name=role) for role in roles_to_add])
            except Exception as e :
                pass
            if info['clan']['tag'] in ['#PUQ2PYGG','#P229L9Q2']:
                clan_name_sort = {'#PUQ2PYGG':'[ILT] - ','#P229L9Q2':'[CC] - '}
                new_nickname = f'{clan_name_sort[info["clan"]["tag"]]}{info["name"]}'
                await member.edit(nick=new_nickname)
                await ctx.send(f"{member.nick} moved to  **{clanInfo.upper()}** 🚀")
                await channel.send(f"{member.mention} is now a member of **{clanInfo.upper()}**")
                message_text = f"""<a:cheers:1252319872025755680> Welcome, this is your clan chat. Make sure to go through the followings -

<a:siren:1250741028915511376> **{clan_data[clan_name]['announcement_channel']}** - For important clan announcements 

Note - Make Sure To Maintain This In Clan 

<a:tick:1250740837990797372>  Donate
<a:tick:1250740837990797372>  Attack in wars
<a:tick:1250740837990797372>  Follow mails
<a:tick:1250740837990797372>  2000 in CG 
<a:tick:1250740837990797372>  Participate in Clan-Capitals raids
<a:PHcross:1250741424601956377>  Don’t kick anyone <a:PHcross:1250741424601956377> """

                embed = Embed(color=Color.random())
                embed.description = message_text
                await channel.send(embed=embed)
            else:
                new_nickname = f'{COC.get_prefix(info["role"]) if info["role"] else "Mb - "}{info["name"]}'
                await member.edit(nick=new_nickname)
                await ctx.send(f"{member.nick} moved to  **{clanInfo.upper()}** 🚀")
                await channel.send(f"{member.mention} is now a member of **{clanInfo.upper()}**")

                embed = Embed(color=Color.random())
                embed.description = ("🍻 Welcome, This is your clan chat.\n"
                                     "Make sure to go through the followings -\n"
                                     "\n"
                                     f"『📢』**<#{clan_data[clan_name]['announcement_channel']}>** \nFor important clan announcements\n"
                                     f"『⚠』**<#1054439098342969425>** \nFor war rules and instructions\n"
                                     "\n"
                                     "Note - Make Sure To Maintain This In Clan\n"
                                     "<:tickup:1196453042464239686> Donate\n"
                                     "<:tickup:1196453042464239686> Attack in wars\n"
                                     "<:tickup:1196453042464239686> Follow mails\n"
                                     "<:tickup:1196453042464239686>2000 in CG\n"
                                     "<:tickup:1196453042464239686> Above 16k in Clan-Capitals raids\n"
                                     "<:tickup:1196453042464239686> Participate in Clan-Capitals\n"
                                     "❌ Don’t kick anyone")
                await channel.send(embed=embed)




        except Exception as e :
            error_embed = Embed(color=Color.red())
            error_embed.description = f"❌Failed to move {member.name} to {clan_name.upper()}\nReason: {e}"
            await ctx.send(embed=error_embed)


async def setup(client) :
    await client.add_cog(ClanRoleAdder(client))
