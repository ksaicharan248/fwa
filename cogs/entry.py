import discord
from discord.ui import Modal , View , Button , TextInput
from discord.ext import commands
import COC
import pickle


class FeedbackModal(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.green , label="🔗 Link Account" , custom_id="1" , row=1)
    async def button_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        modal = NewModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(style=discord.ButtonStyle.gray , label='Unlink' , custom_id="2" , row=1)
    async def button_callback3(self , interaction: discord.Interaction , button: discord.ui.button) :
        with open('datasheets/userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if interaction.user.id in user_data.keys() :
            del user_data[interaction.user.id]
            with open('datasheets/userdata.pkl' , 'wb') as file :
                pickle.dump(user_data , file)
            e = discord.Embed(title="Unlinked" , colour=discord.Color.random())
            await interaction.response.send_message(embed=e , ephemeral=True)
        else :
            e = discord.Embed(title="You Don`t have any account linked yet" , colour=discord.Color.red())
            await interaction.response.send_message(embed=e , ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.red , label="Help" , custom_id="3" , row=1)
    async def button_callback1(self , interaction: discord.Interaction , button: discord.ui.button) :
        e = discord.Embed(title="To Find a player tag" , colour=discord.Colour.random())
        e.description = f'- Open Game\n' \
                        '- Navigate to your accounts profile\n' \
                        '- Near top left click copy icon to copy player tag to clipboard\n' \
                        '- Make sure it is the player tag & not the clan\n' \
                        '- View photo below for reference '
        e.set_image(url='https://pixelcrux.com/Clash_of_Clans/Images/Game_UI/Player_Tag.png')
        await interaction.response.send_message(embed=e , ephemeral=True)




class NewModal(discord.ui.Modal , title="Link your profile") :
    name = discord.ui.TextInput(label='Name' , placeholder="Please enter your in-game name " ,
                                style=discord.TextStyle.short)
    playe_tag = discord.ui.TextInput(label='Player Tag' , placeholder="Please enter your player tag " ,
                                     style=discord.TextStyle.short)

    async def on_submit(self , interaction: discord.Interaction) :
        with open('datasheets/userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if interaction.user.id in user_data.keys() :
            e = discord.Embed(
                title=f"<:ver:1157952898362261564> You have already linked your account \nLinked account:\n{user_data[interaction.user.id]['name']} - {user_data[interaction.user.id]['tag']}" ,
                colour=discord.Color.random())
            await interaction.response.send_message(embed=e , ephemeral=True)
        else :
            try :
                player_data = COC.get_user(tag=self.playe_tag.value.strip('#'))
            except Exception as e :
                player_data = False
            if player_data :
                e2 = discord.Embed(
                    title=f'<:th{str(player_data["townHallLevel"])}:{COC.get_id(player_data["townHallLevel"])}>  {player_data["name"]} -{player_data["tag"]}' ,
                    color=discord.Color.random())
                e2.description = f'\n<:ver:1157952898362261564> Linked {player_data["tag"]} to {interaction.user.mention}'
                e2.set_footer(text=f"Linked by {interaction.user.display_name} ")
                await interaction.response.send_message(embed=e2 , ephemeral=True)
                user_data[interaction.user.id] = {'tag' : player_data['tag'].strip('#') , 'name' : player_data['name'] ,
                                                  'clan' : player_data['clan'][
                                                      'tag'] if 'clan' in player_data else 'no clan' ,
                                                  'clanname' : player_data['clan'][
                                                      'name'] if 'clan' in player_data else 'no clan'}

                with open('datasheets/userdata.pkl' , 'wb') as file :
                    pickle.dump(user_data , file)

                role_name = '🔸ENTRY🔸'

                if role_name in [role.name for role in interaction.user.roles] :
                    verification = COC.ccns_check(tag=self.playe_tag.value.strip('#'))
                    if verification[1] == True :
                        if not verification[0] :
                            await interaction.user.edit(nick=f'TH {player_data["townHallLevel"]} - {player_data["name"]} (flagged)')
                        else :
                            await interaction.user.edit(nick=f'TH {player_data["townHallLevel"]} - {player_data["name"]}')
                        await interaction.user.remove_roles(
                            *[role for role in interaction.user.roles if role != interaction.user.guild.default_role])
                        channel_info = {
                            1054435038881665024 : ['approved✅' , 1055439744739315743 , 1126856734095462511] ,
                            1250477280426201181 : ['approved✅' , 1250529194090172517 , 1250842431432429689]}
                        await interaction.user.add_roles(
                            discord.utils.get(interaction.user.guild.roles , name=channel_info[interaction.user.guild.id][0]))
                        channel = interaction.user.guild.get_channel(channel_info[interaction.user.guild.id][1])
                        await channel.send(f"{interaction.user.mention} has been approved by <@1154381056900870174>")
                        e = discord.Embed(title="APPROVED " , color=discord.Color.random())
                        e.description = f'❯ Clan spots will be posted in this {interaction.user.guild.get_channel(channel_info[interaction.user.guild.id][1]).mention}, make sure to check it\n' \
                                        f'❯ You will be **@notified** if a spot available for your TH level.\n' \
                                        f'❯ Just make sure to reply as fast as possible to ensure your spot.\n' \
                                        f'❯ Donot request to join in game unless instructed to do so.\n' \
                                        f'❯ You may stay in your **current clan** or join a random clan while waiting for a **spot**.\n' \
                                        f'❯ Make sure to have **NO war timer** when you answer for spots.\n' \
                                        f'❯ Ask in {interaction.user.guild.get_channel(channel_info[interaction.user.guild.id][2]).mention} if you have any questions. \nDone by : <@1154381056900870174>'
                        await channel.send(embed=e)
                    else :
                        channel = interaction.user.guild.get_channel(1072557906509189191)
                        await channel.send(f"{interaction.user.mention} is fwa  banned player")

            else :
                e = discord.Embed(title="Invalid player tag" ,
                                  description=f'No data found on this tag \ntag : {self.playe_tag.value}' ,
                                  colour=discord.Color.red())
                await interaction.response.send_message(embed=e , ephemeral=True)

    async def on_error(self , interaction: discord.Interaction , error: Exception) :
        await interaction.response.send_message(error , ephemeral=True)




class tickets(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=None)

    async def send_msg(self , channel: discord.TextChannel , guild: discord.Guild , user , th) :
        embed = discord.Embed(title=f'Welcome to {guild.name}' , colour=discord.Colour.random())
        embed.description = f"You can read our rules and details about 💎FWA💎 in <#1054438569378332754> \n\n" \
                            f"If you wish to join one of our clans then please follow the steps below.\n\n" \
                            f"- **Step 1** : Post a picture of My Profile tab\n" \
                            f"- **Step 2** : Post a picture of your 💎FWA💎 base \n" \
                            f"If you don’t have a 💎FWA💎 base then you can type \n```$bases```" \
                            f" OR visit <#1054438501233479760>\n " \
                            f"**•Step 3** : Have some patience, and select the clan you wish to join. " \
                            f"you will be assisted shortly.\n\n" \
                            f'Instructions : \n' \
                            f'- To join a Clan select a clan below\n' \
                            f'- If you select a clan then respective team gets arrived\n' \
                            f'- If you need help use the button below\n' \
                            f'- To close the ticket ping the Helpers\n' \
                            f'\n\n🚨Note - We don’t recruit FWA BANNED players'
        await channel.send(embed=embed , view=clan_list(user , th))

    @discord.ui.button(style=discord.ButtonStyle.green , label="🎟 Create Ticket" , custom_id="1" , row=1)
    async def button_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        with open('datasheets/userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if interaction.user.id not in user_data.keys() :
            e = discord.Embed(title="Please link your account here\n<#1198540991020400672>" ,
                              colour=discord.Colour.red())
            await interaction.response.send_message(embed=e , ephemeral=True)
        else :
            with open('datasheets/tickets.pkl' , 'rb') as file :
                ticket_data = pickle.load(file)
            if interaction.user.id in ticket_data.keys() :
                e = discord.Embed(title="You already have an active ticket" , colour=discord.Colour.red())
                await interaction.response.send_message(embed=e , ephemeral=True)

            else :
                user_coc_data = COC.get_user(tag=user_data[interaction.user.id]['tag'].strip('#'))
                ticket_data[interaction.user.id] = 1
                guild = interaction.guild
                user = interaction.user
                category = guild.get_channel(1198538979755180142)
                channel_name = f'Th-{user_coc_data["townHallLevel"]}-{user_coc_data["name"]}'
                overwrites = {guild.default_role : discord.PermissionOverwrite(read_messages=False) ,
                              user : discord.PermissionOverwrite(read_messages=True , send_messages=True)}
                channel1 = await guild.create_text_channel(channel_name , category=category , overwrites=overwrites)
                e = discord.Embed(title=f"Ticket created: {channel1.name} by {user.name}" , color=discord.Color.green())
                await interaction.response.send_message(embed=e , ephemeral=True)
                entrychannel = guild.get_channel(1198542838699409439)
                await entrychannel.send(embed=e)
                await self.send_msg(channel1 , guild , user , user_coc_data["townHallLevel"])
                await interaction.response.defer()
                with open('datasheets/tickets.pkl' , 'wb') as file :
                    pickle.dump(ticket_data , file)


class clan_list(discord.ui.View) :

    def __init__(self , interacted_user , th) :
        super().__init__(timeout=None)
        self.interacted_user = interacted_user
        self.th = th
        self.optionsd()

    def optionsd(self) :
        townhall = self.th
        with open('datasheets/optimaltownhall.pkl' , 'rb') as file :
            options_data = pickle.load(file)
        self.select_callback.options = []
        for values , data in options_data.items() :
            if townhall in data['Townhall'] :
                label = data['label']
                description = data['description']
                value = data['value']
                self.select_callback.add_option(label=label , value=value , description=description)


    @discord.ui.select(placeholder="currently available clans" , min_values=1 , max_values=1)
    async def select_callback(self , interaction: discord.Interaction , select: discord.ui.select) :
        if select.values[0] and self.interacted_user.id == interaction.user.id :
            select.disabled = True
            await interaction.response.edit_message(view=self)
            clantag = select.values[0]
            clt = COC.getclan(tag=clantag.strip('#'))
            with open('datasheets/leader_userdata.pkl' , 'rb') as f :
                lead = pickle.load(f)
            e = discord.Embed(title=f'**{clt["name"]}** - {clt["tag"]}' ,
                              url=f'https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{clt["tag"].strip("#")}' ,
                              color=discord.Color.random())
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
                            f'<:cp:1161299634916966400> : {"1" if clt["clanCapital"] == {} else clt["clanCapital"]["capitalHallLevel"]}    ' \
                            f' <:members:1161298479050670162> : {clt["members"]}/50\n\n' \
                            f'<:saw:1159496168347291698> **Leader**  : \n<@{lead[clt["tag"].strip("#")] if clt["tag"].strip("#") in lead.keys() else "UNKOWN"}>'
            await interaction.followup.send(embed=e , ephemeral=True , view=new(clan_tag=clantag))
        else :
            await interaction.response.send_message('you are not supposed to change the clan' , ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.red , label="Close" , custom_id="1" , row=1)
    async def button_callback1(self , interaction: discord.Interaction , button: discord.ui.button) :
        roles_to_check = ['🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'LEADERS' , 'CO-LEADERS']
        member = interaction.user
        has_any_role = any(role.name in roles_to_check for role in member.roles)
        if has_any_role :
            guild = interaction.guild
            close_channel = guild.get_channel(1198542899139325962)
            embed = discord.Embed(title=f"{interaction.channel.name} is closed by {interaction.user.display_name} ")
            await close_channel.send(embed=embed)
            await interaction.channel.delete()
            with open('datasheets/tickets.pkl' , 'rb') as f :
                user_data = pickle.load(f)
            player_idd = self.interacted_user.id
            if player_idd in user_data.keys() :
                try :
                    del user_data[player_idd]
                except :
                    user_data[player_idd].pop()
            with open('datasheets/tickets.pkl' , 'wb') as f :
                pickle.dump(user_data , f)

        else :
            await interaction.response.send_message(
                f'{member.mention} you cant close the chat make sure to ping any helpers or leaders' , ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.green , label="🔃" , custom_id="3" , row=1)
    async def button_callback3(self , interaction: discord.Interaction , button: discord.ui.button) :
        select = self.children[0]
        select.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple , label="help" , custom_id="2" , row=1)
    async def button_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        guild = interaction.guild
        role = discord.utils.get(guild.roles , id=1198545083117617173)
        channel = interaction.channel
        await channel.set_permissions(role , read_messages=True , send_messages=True , read_message_history=True ,
                                      manage_messages=True , attach_files=True , mention_everyone=True)
        e = discord.Embed(title="Human support" , colour=discord.Colour.random())
        e.description = '<@&1198545083117617173> \n will assist you further here'
        await interaction.response.send_message(embed=e , ephemeral=True)


class new(discord.ui.View) :
    def __init__(self , clan_tag) :
        self.clanTag = clan_tag.strip('#')
        super().__init__(timeout=None)

    role = {'U0LPRYL2' : ['TSL' , 'THE SHIELD - #U0LPRYL2'] , '2Q8URCU88' : ['WAL' , '♤WARNING♤ - #2Q8URCU88'] ,
            '2G9URUGGC' : ['BTL' , 'BROTHERS - #2G9URUGGC'] , 'GC8QRPUJ' : ['AVL' , 'AVENGERS - #GC8QRPUJ'] ,
            'QL9998CC' : ['PKL' , 'Pakistan Lovers - #QL9998CC'] ,
            '2QR0Q8QYL' : ['TOL' , '! The Order ! - #2QR0Q8QYL'] , '2G9V8PQJP' : ['HGL' , '♤HOGWARTS♤ - #2G9V8PQJP']}

    @discord.ui.button(style=discord.ButtonStyle.green , emoji='✅' , custom_id="1" , row=1)
    async def button_callback(self , interaction: discord.Interaction , button: discord.ui.button) :
        self.clear_items()
        await interaction.response.edit_message(view=self)
        guild = interaction.guild
        rolename = discord.utils.get(guild.roles , name=self.role[self.clanTag][0])
        leaders = discord.utils.get(guild.roles , name='LEADERS')
        channel = interaction.channel
        await channel.set_permissions(rolename , read_messages=True , send_messages=True , read_message_history=True ,
                                      manage_messages=True , attach_files=True , mention_everyone=True)
        await channel.set_permissions(leaders , read_messages=True , send_messages=True , read_message_history=True ,
                                      manage_messages=True , attach_files=True , mention_everyone=True)
        embed = discord.Embed(title=f"{self.role[self.clanTag][1]}")
        embed.description = '- Respective team will be arrived shortly\n- Please wait patiently,They will get back to you soon '
        await channel.send(embeds=[embed])
        await channel.send(f'{rolename.mention} please assist the further process')

        await interaction.response.delete_message()

    @discord.ui.button(style=discord.ButtonStyle.gray , emoji='❌' , custom_id="2" , row=1)
    async def button_callback1(self , interaction: discord.Interaction , button: discord.ui.button) :
        self.clear_items()
        await interaction.response.edit_message(view=self)
        await interaction.delete_original_response()



class EntrySystem(commands.Cog) :
    def __init__(self , client) :
        self.client = client

    @commands.command(name='linkform' , aliases=['lf'])
    async def linkform(self , ctx) :
        await ctx.message.delete()
        e = discord.Embed(title=f'WELCOME TO \n{ctx.guild.name}\n' ,
                          description='\n-------------------------------\nPlease click the following .  🔗 link button to link your profile with the Discord ID.' ,
                          colour=discord.Colour.blue())
        e.set_thumbnail(
            url='https://static.wikia.nocookie.net/clashofclans/images/1/1e/Boat.png/revision/latest/scale-to-width-down/100?cb=20230109004815')
        await ctx.send(embed=e , view=FeedbackModal())

    @commands.command(name='ticketsi' , aliases=['toki'])
    async def create_tickets(self , ctx) :
        await ctx.message.delete()
        await ctx.send('Hello wanna join in any of our Team of clans then follow the below steps ')
        embed = discord.Embed(title=f"{ctx.guild.name}\n" , colour=discord.Colour.random())
        embed.description = f'\n- To joins us please hit the ticket create button below \n\n**WE ACCEPT ONLY FOLLOWING Townhalls\n\n**' \
                            f'    <:th16:1184685970814156800> <:th15:1158776040525680694> <:th14:1157934828784734299> <:th13:1157933611337666620> <:th12:1157933184529469471> <:th11:1157932788683653170>'
        await ctx.send(embed=embed , view=tickets())

    @commands.command(name='close')
    async def create_close(self , ctx , user: discord.Member = None) :
        with open('datasheets/tickets.pkl' , 'rb') as f :
            user_data = pickle.load(f)
        await ctx.message.delete()
        if user is None :
            del user_data[ctx.author.id]
        else :
            del user_data[user.id]

        await ctx.send('done')
        with open('datasheets/tickets.pkl' , 'wb') as f :
            pickle.dump(user_data , f)




async def setup(bot) :
    await bot.add_cog(EntrySystem(bot))
