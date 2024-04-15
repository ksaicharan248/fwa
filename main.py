import asyncio
import os
import io
import discord
import matplotlib.pyplot as plt
import typing
import warnings
import numpy as np
from PIL import Image , ImageDraw , ImageFont
import requests
from io import BytesIO
from discord.ext import commands
import fwastats
from fwastats import get_nope
import COC
from discord import Embed , Color
from discord.ui import Button , View , Select
from setkey import keyy
from webser import keep_alive
import pickle
from warattacksummary import get_pins , get_clan_tags , fetch_and_count_offline , fetch_data , main , fwa_count


# Define the intents
intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix="$" , intents=intents)
client.remove_command("help")

p = client.command_prefix

warnings.filterwarnings("ignore" , category=UserWarning , message="Glyph.*missing from current font." ,module="tkinter")

@client.event
async def on_ready() :
    print('We have logged in as {0.user}'.format(client))
    await client.tree.sync()


owener_info: int = 765929481311354881


@client.event
async def on_command_error(ctx , error) :
    owner = await client.fetch_user(int(owener_info))
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
        await ctx.send("check and try agian..")

    elif isinstance(error , commands.CommandNotFound) :
        pass

    else :
        embed = discord.Embed(title="WARNING ⚠️⚠️⚠️" ,
                              description="Something went wrong. Please contact the developer." ,
                              color=discord.Color.red())
        await ctx.send(embed=embed)


@client.event
async def on_member_remove(member) :
    owner = await client.fetch_user(int(765929481311354881))
    with open("datasheets/userdata.pkl" , "rb") as file :
        user_data = pickle.load(file)
    with open("datasheets/leader_userdata.pkl" , 'rb') as foo :
        token = pickle.load(foo)
    if member.id in user_data.keys() :
        try :
            del user_data[member.id]
            await owner.send(f'{member} removed from data base.')
        except :
            user_data.pop(member.id)
            await owner.send(f'{member} removed from data base')

        with open("datasheets/userdata.pkl" , "wb") as file :
            pickle.dump(user_data , file)

    if member.id in token.values() :
        for clantag , ids in token.items() :
            if ids == 241897116815851530 :
                pop_tag = clantag
        try :
            del token[pop_tag]
        except :
            token.pop(pop_tag)
        with open("datasheets/leader_userdata.pkl" , "wb") as file :
            pickle.dump(token , file)


@client.event
async def on_member_join(member) :
    if member.guild.id == 1054435038881665024 :
        welcome_channel = client.get_channel(1055439542863274038)
        if welcome_channel :
            p = client.command_prefix
            await member.add_roles(discord.utils.get(member.guild.roles , name='🔸ENTRY🔸'))
            await welcome_channel.send(f'Hello, {member.mention}  !')
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


@client.hybrid_command(name='text-to-image' , help="Ask any thing with AI")
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️')
async def ask(ctx , prompt: typing.Optional[str] = "clash of clans") :
    await ctx.defer()

    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization" : "Bearer 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"}

    def query(payload) :
        response = requests.post(API_URL , headers=headers , json=payload)
        return response.content

    image_bytes = query({"inputs" : f"{prompt}" , })

    image = Image.open(io.BytesIO(image_bytes))

    with BytesIO() as image_binary :
        image.save(image_binary , 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary , filename='image.png')
        await ctx.send(file=file)


@client.command(name='reload' , help="updated the slash command list")
async def reload(ctx) :
    await ctx.send("Reload...")
    synced = await client.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands.")


@commands.has_any_role('🔰ADMIN🔰')
@client.command(name='create_category_channel' , aliases=['ccc'])
async def create_category_channel(ctx , category_name , role_a_name: discord.Role , role_b_name: discord.Role) :
    guild = ctx.guild
    overwrites = {guild.default_role : discord.PermissionOverwrite(view_channel=False)}
    lead_role = discord.utils.get(guild.roles , name=role_a_name.name)
    meber_role = discord.utils.get(guild.roles , name=role_b_name.name)
    # Create category
    category = await guild.create_category(category_name)
    chanel1_create = await category.create_text_channel('『☘』leadership-chat' , overwrites=overwrites)
    await chanel1_create.set_permissions(lead_role , read_messages=True , send_messages=True ,
                                         read_message_history=True , manage_messages=True , attach_files=True ,
                                         mention_everyone=True)
    await chanel1_create.set_permissions(meber_role , read_messages=False)
    chanel2_create = await category.create_text_channel('『💭』clan-chat' , overwrites=overwrites)
    await chanel2_create.set_permissions(lead_role , read_messages=True , send_messages=True ,
                                         read_message_history=True , manage_messages=True , attach_files=True ,
                                         mention_everyone=True , add_reactions=True)
    await chanel2_create.set_permissions(meber_role , read_messages=True , send_messages=True ,
                                         read_message_history=True , manage_messages=False , attach_files=True ,
                                         mention_everyone=True , add_reactions=True)
    chanel3_create = await category.create_text_channel('『📢』clan-announcements' , overwrites=overwrites)
    await chanel3_create.set_permissions(lead_role , read_messages=True , send_messages=True ,
                                         read_message_history=True , manage_messages=True , attach_files=True ,
                                         mention_everyone=True)
    await chanel3_create.set_permissions(meber_role , read_messages=True , send_messages=False ,
                                         read_message_history=True , manage_messages=False , use_external_emojis=False ,
                                         add_reactions=True)
    channel_names = ['『📘』war-tracker' , '『📗』donation-tracker' , '『📕』player-tracker' , '『📙』clan-tracker' ,
                     '『⏱』activity-tracker' , '『📔』raids-tracker' , '『📊』boost-board' , '『🏓』clan-games-tracker']
    for channel_name in channel_names :
        channel = await category.create_text_channel(channel_name , overwrites=overwrites)

        await channel.set_permissions(lead_role , read_messages=True , send_messages=False , read_message_history=True ,
                                      manage_messages=True)
        await channel.set_permissions(meber_role , read_messages=True , send_messages=False ,
                                      read_message_history=True , manage_messages=False , use_external_emojis=False ,
                                      add_reactions=False)
        await ctx.send(f'Category "{category_name}" and channel "{channel_name}" created with permissions!')


@client.command(name='deltac')
@commands.is_owner()
async def delete_all_channels(ctx) :
    guild = ctx.guild

    # Get the category
    category = ctx.channel.category
    if category :
        # Iterate through channels in the category and delete them
        for channel in category.channels :
            await channel.delete()
        await category.delete()
    else :
        await ctx.send(f'Category "{category}" not found.')


@client.command()
async def emoji(ctx) :
    await ctx.send("<:blueBadge:1007628410375372892>")


class Selectmenu1(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=70)

    optoins = [discord.SelectOption(label='MOD COMMANDS🧑‍🔧' , value='1') ,
               discord.SelectOption(label='LEADER COMMANDS 🌿' , value='2') ,
               discord.SelectOption(label='PLAYER COMMANDS 🌙' , value='3')]

    @discord.ui.select(placeholder='Select an option' , options=optoins , min_values=1 , max_values=1)
    async def select(self , interaction: discord.Interaction , select) :
        try :
            if select.values[0] == '1' :
                embed1 = discord.Embed(title='MOD COMMANDS' , colour=Color.random())
                embed1.description = f"{p}wel         - Welome a player\n" \
                                     f"{p}role        - Add a role to member\n" \
                                     f"{p}rm          - Remove roles\n" \
                                     f"{p}changenick  - Change nickname \n" \
                                     f"{p}removenick  - remove nick name\n" \
                                     f"{p}kick        - kick a member from the server" \
                                     f"\n\nfor more info type ```{p}usage <command name>```"
                await interaction.response.defer()
                await interaction.message.edit(embed=embed1)
            elif select.values[0] == '2' :
                embed2 = discord.Embed(title='LEADER COMMANDS' , colour=Color.random())
                embed2.description = f"`{p}mc`          - move a player to your clan chat\n" \
                                     f"`{p}unq`         - add player to unqualified\n" \
                                     f"`{p}app`         - approve the player\n" \
                                     f"`{p}re`          - send the player to reapply \n" \
                                     f"`{p}check`       - check the player with CCNS\n" \
                                     f"`{p}war`         - send war updates\n" \
                                     f"`{p}force_link`     - link any other player with tag " \
                                     f"\n\nfor more info type ```{p}usage <command name>```"

                await interaction.response.defer()
                await interaction.message.edit(embed=embed2)
            elif select.values[0] == '3' :
                embed3 = discord.Embed(title='PLAYER COMMANDS' , colour=Color.random())
                embed3.description = f"`{p}ping`         - Show latency\n" \
                                     f"`{p}link`       - link the bot with player tag \n" \
                                     f"`{p}profile`    - profile of player\n" \
                                     f"`{p}clan`       - clan info\n\nfor more info type " \
                                     f"`{p}listcompo   - lists the clan composition`\n" \
                                     f"`{p}warcompo`        - show war composition\n" \
                                     f"```{p}usage <command name>```"

                await interaction.response.defer()
                await interaction.message.edit(embed=embed3)
        except Exception as e :
            pass


class Selectmenu2(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=70)

    optoins = [discord.SelectOption(label='MOD COMMANDS🧑‍🔧' , value='1') ,
               discord.SelectOption(label='LEADER COMMANDS 🌿' , value='2') ,
               discord.SelectOption(label='PLAYER COMMANDS 🌙' , value='3')]

    @discord.ui.select(placeholder='Select an option' , options=optoins , min_values=1 , max_values=1)
    async def select(self , interaction: discord.Interaction , select) :
        try :
            if select.values[0] == '1' :
                embed1 = discord.Embed(title='MOD COMMANDS' , colour=Color.random())
                embed1.description = f"{p}role        - Add a role to member\n" \
                                     f"{p}rm          - Remove roles\n" \
                                     f"{p}changenick  - Change nickname \n" \
                                     f"{p}removenick  - remove nick name\n" \
                                     f"{p}kick        - kick a member from the server" \
                                     f"\n\nfor more info type ```{p}usage <command name>```"
                await interaction.response.defer()
                await interaction.message.edit(embed=embed1)
            elif select.values[0] == '2' :
                embed2 = discord.Embed(title='LEADER COMMANDS' , colour=Color.random())
                embed2.description = f"`{p}j-m        - add player to Jigglets clan\n" \
                                     f"`{p}i-m          - add player to Illuminati clan\n" \
                                     f"`{p}unq`         - add player to unqualified\n" \
                                     f"`{p}app`         - approve the player\n" \
                                     f"`{p}re`          - send the player to reapply \n" \
                                     f"`{p}check`       - check the player with CCNS\n" \
                                     f"`{p}force_link`     - link any other player with tag " \
                                     f"\n\nfor more info type ```{p}usage <command name>```"
                await interaction.response.defer()
                await interaction.message.edit(embed=embed2)

            elif select.values[0] == '3' :
                embed3 = discord.Embed(title='PLAYER COMMANDS' , colour=Color.random())
                embed3.description = f"`{p}ping`         - Show latency\n" \
                                     f"`{p}link`       - link the bot with player tag \n" \
                                     f"`{p}clan`       - clan info\n\nfor more info type " \
                                     f"```{p}usage <command name>```"

                await interaction.response.defer()
                await interaction.message.edit(embed=embed3)

        except Exception as e :
            pass


@client.hybrid_command(name='help' , help='help')
async def help(ctx) :
    if ctx.guild.id == 1054435038881665024 :
        await ctx.defer()
        await ctx.send(content='HELP COMMAND' , view=Selectmenu1())
    elif ctx.guild.id == 1152220160028057660 :
        await ctx.defer()
        await ctx.send(content='HELP COMMAND' , view=Selectmenu2())


@client.command(name='listcommands' , aliases=["lstcmd"] , help='List all available commands')
async def list_commands(ctx) :
    sorted_commands = sorted(client.commands , key=lambda x : x.name.lower())
    command_info = ""
    for command in sorted_commands :
        aliases = '  -- ' + ', '.join(command.aliases) if command.aliases else " "
        command_info += f"->{client.command_prefix}{command.name}{aliases}\n"

    await ctx.send(f"List of available commands:\n```{command_info}```")


@client.command()
async def ping(ctx) :
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(name='war' , help="war announcement either win or loose or mis match or blacklist clan war" ,
                usage=f"{p}war <win/loose/mismatch/bl> \nexample : {p}war win ,{p}war loose")
@commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
async def war(ctx , target=None) :
    cid = ctx.channel.category.id
    cidinfo = {1054453503084482580 : ["U0LPRYL2" , 1055418276546629682 , 'THE SHIELD'] ,
               1222214889859321919 : ["8G2RJCP0" , 1222212841373696010 , 'GOODVIBES 24/7'] ,
               1063290412397244587 : ["2G9URUGGC" , 1063289659586785362 , 'BROTHERS'] ,
               1196099434333880361 : ["QL9998CC" , 1196090548193345667 , "Pakistan Lovers"] ,
               1188693015921950890 : ["GC8QRPUJ" , 1188693492503957514 , "AVENGERS"]}
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
        font = ImageFont.truetype(r'templates/ArialUnicodeMS.ttf' , 40)
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


@client.command()
async def load(ctx , extension) :
    if ctx.author.id == ctx.author.id :
        await client.load_extension(f'cogs.{extension}')
        my_embed = discord.Embed(title=":white_check_mark: Command load complete" ,
                                 description="Loaded " + f'{extension}!' , color=0x6136c2)
        await ctx.send(embed=my_embed)
    else :
        my_embed = discord.Embed(title=":x: Error" , description="Only the bot owner can use this command" ,
                                 color=0x6136c2)
        await ctx.send(embed=my_embed)


class war_buttons(discord.ui.View) :
    def __init__(self , clan_data: dict , common_clan_data) :
        self.common_clan_data = common_clan_data
        self.clan_data = clan_data
        self.page = 0
        self.lastpage = 3
        super().__init__(timeout=100)

    async def update_embed(self , interaction) :
        clan_list = list(self.clan_data.keys())
        clan = clan_list[self.page]
        embed = discord.Embed(title=f"{clan}" , color=discord.Color.blue())

        # Adding fields for zero attacks
        zero_attacks_field = ""
        attc0 = self.clan_data[clan][0]
        for player in attc0 :
            zero_attacks_field += f"{player['position'] if player['position'] >= 10 else '0' + str(player['position'])}    -   {player['townHall'] if player['townHall'] >= 10 else '0' + str(player['townHall'])}   -  {player['name']}\n"
        embed.description = "**MISSED BOTH ATTACKS**\n" + f"```POSITION  TH  NAME\n{zero_attacks_field}```"

        # Adding fields for single attacks
        single_attacks_field = ""
        attc1 = self.clan_data[clan][1]
        for player in attc1 :
            single_attacks_field += f"{player['position'] if player['position'] >= 10 else '0' + str(player['position'])}   -   {player['townHall'] if player['townHall'] >= 10 else '0' + str(player['townHall'])}   -  {player['name']}\n"
        embed.add_field(name="**MISSED SINGLE ATTACK**\n" , value=f"```POSITION TH  NAME\n{single_attacks_field}```" ,
                        inline=False)
        await interaction.response.defer()
        await interaction.message.edit(embed=embed , attachments=[])

    @discord.ui.button(emoji='⏪' , style=discord.ButtonStyle.secondary)
    async def button1_callback1(self , interaction: discord.Interaction , button: discord.ui.button) :
        if self.page > 0 :
            self.page -= 1
            await self.update_embed(interaction)
        else :
            await interaction.response.defer()

    @discord.ui.button(emoji='⏩' , style=discord.ButtonStyle.secondary)
    async def button1_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        if self.page < self.lastpage - 1 :
            self.page += 1
            await self.update_embed(interaction)
        else :
            await interaction.response.defer()

    @discord.ui.button(emoji='🚀' , style=discord.ButtonStyle.danger)
    async def button1_callback3(self , interaction: discord.Interaction , button: discord.ui.button) :
        await interaction.response.defer()
        data = self.common_clan_data
        data[1] = []
        for sublist in data :
            filtered_data = [(name , counts) for name , counts in sublist if counts['zero'] > 1 or counts['single'] > 1]
            if not filtered_data :
                continue
            names = [item[0] for item in filtered_data]
            zeros = [item[1]['zero'] for item in filtered_data]
            singles = [item[1]['single'] for item in filtered_data]
            fig , ax = plt.subplots()
            width = 0.4
            ind = np.arange(len(names))
            ax.bar(ind - width / 2 , zeros , width , label='Zero attacks used')
            ax.bar(ind + width / 2 , singles , width , label='Single attacks used')
            ax.set_ylabel('Number of missed attacks')
            ax.set_title('Frequency of Names')
            ax.set_xticks(ind)
            ax.set_xticklabels(names)
            ax.legend()
            plt.xticks(rotation=45 , ha='right')
            plt.subplots_adjust(bottom=0.25)
            buffer = io.BytesIO()
            plt.savefig(buffer , format='png')
            buffer.seek(0)

            file = discord.File(buffer , filename='plot.png')
            embed = discord.Embed(color=discord.Color.blue())
            embed.description = "List of common missed attacks\nNote: This data may be captured on the preparation day of the war and may not be accurate if the war has not started yet , please check and ensure if needed"
            embed.set_image(url='attachment://plot.png')
            await interaction.message.edit(embed=embed , attachments=[file])


@client.command(name='war-stats' , aliases=['ws'] , help="Shows the war stats of the clan")
async def warstats(ctx , limit=20) :
    with open('datasheets/userdata.pkl' , 'rb') as f :
        user_data = pickle.load(f)
    if ctx.author.id in user_data.keys() :
        tag = user_data[ctx.author.id]['clan']
    else :
        await ctx.send('Please provide a tag.')
        return
    try :

        data = {}
        clan_user_tags = get_clan_tags(tags=tag)
        pins = get_pins(tag=tag , limit=limit)
        offline , _ = await fetch_and_count_offline(pins , tag=tag)
        sorted_players = sorted(offline[1].items() , key=lambda x : x[1]['zero'] , reverse=True)
        for key , value in sorted_players :
            if key in clan_user_tags and (value['zero'] > 1 or value['single'] > 1) :
                data[key] = value
        count = offline[0]
        players = list(data.keys())
        names = [data[player]['name'] for player in data]
        zeros = [data[player]['zero'] for player in players]
        singles = [data[player]['single'] for player in players]
        bar_width = 0.35
        r1 = np.arange(len(players))
        r2 = [x + bar_width for x in r1]
        plt.figure(figsize=(12 , 8))
        plt.barh(r1 , zeros , color='skyblue' , height=bar_width , edgecolor='grey' ,
                 label=f'Number of Zero attacks in past {count} wars')
        plt.barh(r2 , singles , color='salmon' , height=bar_width , edgecolor='grey' ,
                 label=f'Number of Single attack in past {count} wars')
        plt.xlabel('Number of missed attacks')
        plt.ylabel('Player')
        plt.title(f'Out of past {count} FWA wars')
        plt.yticks([r + bar_width / 2 for r in range(len(players))] , names)
        plt.legend()
        plt.grid(visible=True , axis='x' , which="both")
        buffer = io.BytesIO()
        plt.savefig(buffer , format='png')
        buffer.seek(0)
        file = discord.File(buffer , filename='plot.png')
        await ctx.send(f"List of common missed attacks \n{user_data[ctx.author.id]['clanname']} - {tag}" , file=file)
    except :
        await ctx.send("An error occured. Please try again later.")
        return


@client.command(name='attack-summary' , aliases=['attacks' , 'as'] ,
                help=f"Shows the war stats of the clan\n example: {p}attack-summary <#clan_tag> or<user_mention>")
async def warst(ctx , tag=None) :
    with open('datasheets/userdata.pkl' , 'rb') as f :
        user_data = pickle.load(f)
    if ctx.message.mentions :
        if ctx.message.mentions[0].id in user_data.keys() :
            tag = user_data[ctx.message.mentions[0].id]['clan']
        else :
            await ctx.send("The user you mentioned doest have any linked ID`s ")
            return
    if tag is None :
        if ctx.author.id in user_data.keys() :
            tag = user_data[ctx.author.id]['clan']
        else :
            await ctx.send('Please provide a tag.')
            return
    else :
        tag = tag.strip('#')

    try :
        data = await get_nope(clan_tag=tag)
        clan_data = {}

        for i in [0 , 1 , 2] :
            clanname = data[i][0]['opponentName']
            zeroattcks = []
            oneattacks = []
            for player in data[i] :
                if player['stars1'] == 0 and player['stars2'] == 0 :
                    zeroattcks.append(player)
                elif player['stars1'] == 0 or player['stars2'] == 0 :
                    oneattacks.append(player)
                clan_data[clanname] = [zeroattcks , oneattacks]

        clan = list(clan_data.keys())[0]
        clan_attacks = clan_data[clan]
        embed = discord.Embed(title=f"{clan}" , color=discord.Color.blue())

        # Adding fields for zero attacks
        zero_attacks_field = ""
        attc0 = clan_attacks[0]
        for player in attc0 :
            zero_attacks_field += f"{player['position'] if player['position'] >= 10 else '0' + str(player['position'])}    -   {player['townHall'] if player['townHall'] >= 10 else '0' + str(player['townHall'])}   -  {player['name']}\n"
        embed.description = "**MISSED BOTH ATTACKS**\n" + f"```POSITION  TH  NAME\n------------------\n{zero_attacks_field}```"

        # Adding fields for single attacks
        single_attacks_field = ""
        attc1 = clan_attacks[1]
        for player in attc1 :
            single_attacks_field += f"{player['position'] if player['position'] >= 10 else '0' + str(player['position'])}   -   {player['townHall'] if player['townHall'] >= 10 else '0' + str(player['townHall'])}   -  {player['name']}\n"
        embed.add_field(name="**MISSED SINGLE ATTACK**\n" ,
                        value=f"```POSITION TH  NAME\n------------------\n{single_attacks_field}```" , inline=False)
        common_clan_data = get_common_clan_data(clan_data)
        await ctx.send(embed=embed , view=war_buttons(clan_data=clan_data , common_clan_data=common_clan_data))

    except :
        embed = Embed(title="Attack summary not found on this Tag or ID")
        await ctx.send(embed=embed)


def get_common_clan_data(clan_data) :
    name_counts = {}
    for clan , clanattcks in clan_data.items() :
        for attack0 in clanattcks[0] :
            name = attack0['name']
            if name not in name_counts :
                name_counts[name] = {"zero" : 0 , "single" : 0}
            name_counts[name]["zero"] += 1
        for attc1 in clanattcks[1] :
            name = attc1['name']
            if name not in name_counts :
                name_counts[name] = {"zero" : 0 , "single" : 0}
            name_counts[name]["single"] += 1

    sorted_zero = sorted(name_counts.items() , key=lambda x : x[1]['zero'] , reverse=True)
    sorted_single = sorted(name_counts.items() , key=lambda x : x[1]['single'] , reverse=True)
    return [sorted_zero , sorted_single]


# Reload Cog
@client.command()
async def reloads(ctx , file_name=None) :
    if file_name is None :
        if ctx.author.id == ctx.author.id :
            for filename in os.listdir('./cogs') :
                if filename.endswith('.py') :
                    try :
                        await client.unload_extension(f'cogs.{filename[:-3]}')
                    except :
                        await ctx.send("Error while unloading " + f'{filename[:-3]}')
                    try :
                        await client.load_extension(f'cogs.{filename[:-3]}')
                    except :
                        await ctx.send("Error while unloading " + f'{filename[:-3]}')
                    my_embed = discord.Embed(title=":white_check_mark: Command reload complete" ,
                                             description="Reloaded " + f'{filename[:-3]}!' , color=0x6136c2)
                    await ctx.send(embed=my_embed)


        else :
            my_embed = discord.Embed(title=":x: Error" , description="Only the bot owner can use this command" ,
                                     color=0x6136c2)
            await ctx.send(embed=my_embed)

    else :
        if ctx.author.id == ctx.author.id :
            try :
                await client.unload_extension(f'cogs.{file_name}')
            except :
                await ctx.send("Error while unloading " + f'{file_name}')
            try :
                await client.load_extension(f'cogs.{file_name}')
            except :
                await ctx.send("Error while unloading " + f'{file_name}')
            my_embed = discord.Embed(title=":white_check_mark: Command reload complete" ,
                                     description="Reloaded " + f'{file_name}!' , color=0x6136c2)
            await ctx.send(embed=my_embed)
        else :
            my_embed = discord.Embed(title=":x: Error" , description="Only the bot owner can use this command" ,
                                     color=0x6136c2)
            await ctx.send(embed=my_embed)


@client.command(name="get_back" , aliases=["gb"] , help="Revoke all roles and assign new role to members")
async def get_back(ctx) :
    with open('datasheets/userdata.pkl' , 'rb') as file :
        user_data = pickle.load(file)
    for member in ctx.channel.members :
        try:
            info = COC.get_user(user_data[member.id]['tag'])
            new_nickname = f'{COC.get_prefix(info["role"]) if info["role"] else "Mb - "}{info["name"]}'
            await member.edit(nick=new_nickname)
            await ctx.send(f'Changed nickname of {member.display_name} to {new_nickname}')
        except:
            pass


@client.command(name="clan_revoke", aliases=["cr"], help="Revoke all roles and assign new role to members")
@commands.has_any_role('🔰ADMIN🔰')
async def clan_revoke(ctx, role_to_remove: discord.Role, new_role: discord.Role):
    # Check if the user has administrator permissions
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("You do not have permission to use this command.")

    # Get all members with the specified role
    members_with_role = [member for member in ctx.guild.members if role_to_remove in member.roles]

    # Change the role for each member
    for member in members_with_role:
        try:
            # Remove all roles except @everyone role
            await member.edit(roles=[new_role], nick=f"re - {member.name}")
        except discord.Forbidden:
            await ctx.send(f"Failed to change role for {member.display_name}")

    await ctx.send(f"Removed all roles and assigned {new_role.name} to {len(members_with_role)} members.")



# Unload Cog
@client.command()
async def unload(ctx , extension) :
    if ctx.author.id == ctx.author.id :
        await client.unload_extension(f'cogs.{extension}')
        my_embed = discord.Embed(title=":white_check_mark: Command unload complete" ,
                                 description="Unloaded " + f'{extension}!' , color=0x6136c2)
        await ctx.send(embed=my_embed)
    else :
        my_embed = discord.Embed(title=":x: Error" , description="Only the bot owner can use this command" ,
                                 color=0x6136c2)
        await ctx.send(embed=my_embed)


async def cogs_loader() :
    for filename in os.listdir('./cogs') :
        if filename.endswith('.py') :
            await client.load_extension(f'cogs.{filename[:-3]}')


async def start_alive() :
    await cogs_loader()
    await client.start(keyy)


if __name__ == '__main__' :
    keep_alive()
    asyncio.run(start_alive())
