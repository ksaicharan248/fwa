import discord
from discord.ui import Modal , View , Button , TextInput
from discord.ext import commands
import COC
import pickle


class clan_list(discord.ui.View) :
    def __init__(self ,interacted_user) :
        self.interacted_user = interacted_user
        super().__init__(timeout=None)


    options_data = [
        {'label' : 'The Shield' , 'description' : 'Level : 21 | 💎FWA💎 | leader : AQUAMAN' , 'value' : 'U0LPRYL2'} ,
        {'label' : 'Pakistan Lovers' , 'description' : 'Level : 20 | 💎FWA💎 | leader : king802' , 'value' : 'QL9998CC'} ,
        {'label' : 'Avengers' , 'description' : 'Level : 18 | 💎FWA💎 | leader : Mai2' , 'value' : 'GC8QRPUJ'} ,
        {'label' : '♤WARNING♤' , 'description' : 'Level : 12 | 💎FWA💎 | leader : Tiger' , 'value' : '2Q8URCU88'} ,
        {'label' : 'BROTHERS' , 'description' : 'Level : 7 | 💎FWA💎 | leader : ᵀᵒᵖᴳᵘⁿ『Maverick' ,
         'value' : '2G9URUGGC'} ,
        {'label' : '♤HOGWARTS♤' , 'description' : 'Level : 4 | 💎FWA💎 | leader : Tiger' , 'value' : '2G9V8PQJP'} ,
        {'label' : '! The Order !' , 'description' : 'Level : 3 | 💎FWA💎 | leader : Umer Raheeq' ,
         'value' : '2QR0Q8QYL'}]

    options = [discord.SelectOption(label=data['label'], description=data['description'], value=data['value']) for data in options_data]


    @discord.ui.select(placeholder="Select your clan" , options=options , min_values=1 , max_values=1)
    async def select_callback(self , interaction: discord.Interaction , select: discord.ui.select) :
        if select.values[0] :
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
            await interaction.followup.send(embed=e ,view=new(clan_tag=clantag))


    @discord.ui.button(style=discord.ButtonStyle.red , label="Close" , custom_id="1" , row=1)
    async def button_callback1(self , interaction: discord.Interaction , button: discord.ui.button) :
        roles_to_check = ['🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️','LEADERS' ,'CO-LEADERS']
        member = interaction.user
        has_any_role = any(role.name in roles_to_check for role in member.roles)
        if has_any_role :
            guild = interaction.guild
            close_channel = guild.get_channel(1198542899139325962)
            embed = discord.Embed(title=f"{interaction.channel.name} is closed by {interaction.user.display_name} ")
            await close_channel.send(embed=embed)
            await interaction.channel.delete()
            with open('datasheets/tickets.pkl','rb') as f:
                user_data = pickle.load(f)
            player_idd = self.interacted_user.id
            if player_idd in user_data.keys() :
                try:
                    del user_data[player_idd]
                except:
                    user_data[player_idd].pop()
            with open('datasheets/tickets.pkl' , 'wb') as f:
                pickle.dump(user_data , f)

        else :
            await interaction.response.send_message(f'{member.mention} does not have any of the specified roles.',ephemeral=True)


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
    def __init__(self , clan_tag ) :
        self.clanTag = clan_tag.strip('#')
        super().__init__(timeout=None)

    role = {'U0LPRYL2' : ['TSL' , 'THE SHIELD - #U0LPRYL2'] , '2Q8URCU88' : ['WAL' , '♤WARNING♤ - #2Q8URCU88'] ,
            '2G9URUGGC' : ['BTL' , 'BROTHERS - #2G9URUGGC'] , 'GC8QRPUJ' : ['AVL' , 'AVENGERS - #GC8QRPUJ'] ,
            'QL9998CC' : ['PKL' , 'Pakistan Lovers - #QL9998CC'] ,'2QR0Q8QYL' : ['TOL' , '! The Order ! - #2QR0Q8QYL'] ,
            '2G9V8PQJP' : ['HGL' , '♤HOGWARTS♤ - #2G9V8PQJP']}

    @discord.ui.button(style=discord.ButtonStyle.green , emoji='✅' , custom_id="1" , row=1)
    async def button_callback(self , interaction: discord.Interaction , button: discord.ui.button) :
        self.clear_items()
        await interaction.response.edit_message(view=self)
        guild = interaction.guild
        rolename = discord.utils.get(guild.roles , name=self.role[self.clanTag][0])
        channel = interaction.channel
        await channel.set_permissions(rolename , read_messages=True , send_messages=True , read_message_history=True ,
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

            else :
                e = discord.Embed(title="Invalid player tag" ,
                                  description=f'No data found on this tag \ntag : {self.playe_tag.value}' ,
                                  colour=discord.Color.red())
                await interaction.response.send_message(embed=e , ephemeral=True)

    async def on_error(self , interaction: discord.Interaction , error: Exception) :
        await interaction.response.send_message(error , ephemeral=True)


class FeedbackModal(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.green , label="🔗 Link Account" , custom_id="1" , row=1)
    async def button_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        modal = NewModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(style=discord.ButtonStyle.red , label="Help" , custom_id="2" , row=1)
    async def button_callback1(self , interaction: discord.Interaction , button: discord.ui.button) :
        e = discord.Embed(title="To Find a player tag" , colour=discord.Colour.random())
        e.description = f'- Open Game\n' \
                        '- Navigate to your accounts profile\n' \
                        '- Near top left click copy icon to copy player tag to clipboard\n' \
                        '- Make sure it is the player tag & not the clan\n' \
                        '- View photo below for reference '
        e.set_image(url='https://pixelcrux.com/Clash_of_Clans/Images/Game_UI/Player_Tag.png')
        await interaction.response.send_message(embed=e , ephemeral=True)


class tickets(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=None)

    async def send_msg(self , channel: discord.TextChannel , guild: discord.Guild ,user) :
        embed = discord.Embed(title=f'Welcome to {guild.name}' , colour=discord.Colour.random())
        embed.description = f'Instructions : \n' \
                            f'- To join a Clan select a clan below\n' \
                            f'- If you select a clan then respective team gets arrived\n' \
                            f'- If you need help use the button below\n' \
                            f'- To close the ticket use the button below\n' \
                            f'- Thank you '
        await channel.send(embed=embed , view=clan_list(user))

    @discord.ui.button(style=discord.ButtonStyle.green , label="🎟 Create Ticket" , custom_id="1" , row=1)
    async def button_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        await interaction.response.defer()
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
                await self.send_msg(channel1 , guild , user)
                e = discord.Embed(title=f"Ticket created: {channel1.mention}" , color=discord.Color.green())
                await interaction.response.send_message(embed=e , ephemeral=True)
                entrychannel = guild.get_channel(1198542838699409439)
                await entrychannel.send(embed=e)
                with open('datasheets/tickets.pkl' , 'wb') as file :
                    pickle.dump(ticket_data , file)

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

    @commands.command(name='tickets' , aliases=['tok'])
    async def create_tickets(self , ctx) :
        await ctx.message.delete()
        await ctx.send('Hello wanna join in any of our Team of clans then follow the below steps ')
        embed = discord.Embed(title=f"{ctx.guild.name}\n" , colour=discord.Colour.random())
        embed.description=f'\n- To joins us please hit the ticket create button below \n\n**WE ACCEPT ONLY FOLLOWING Townhalls\n\n**' \
                          f'    <:th16:1184685970814156800> <:th15:1158776040525680694> <:th14:1157934828784734299> <:th13:1157933611337666620> <:th12:1157933184529469471> <:th11:1157932788683653170>'
        await ctx.send(embed=embed,view=tickets())

    @commands.command(name='close')
    async def create_close(self , ctx , user : discord.Member = None) :
        with open('datasheets/tickets.pkl','rb') as f:
            user_data = pickle.load(f)
        await ctx.message.delete()
        if user is None:
            del user_data[ctx.author.id]
        else:
            del user_data[user.id]

        await ctx.send('done')
        with open('datasheets/tickets.pkl' , 'wb') as f:
            pickle.dump(user_data , f)




async def setup(bot) :
    await bot.add_cog(EntrySystem(bot))
