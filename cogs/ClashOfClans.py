import asyncio
import discord
import requests
from discord.ext import commands
import COC
import pickle
from discord import Embed , Color
from discord.ui import Button , View , Select
from setkey import auth
from main import p

header = {'Accept' : 'application/json' , 'Authorization' : auth}

verifyheaders = {'Content-Type' : 'application/json' , 'Authorization' : auth}


class cwlbutton(View) :
    def __init__(self , ctx , round) :
        super().__init__(timeout=None)
        self.ctx = ctx
        self.round = round

    async def update_embed(self , interaction , user_data) :
        embed = Embed(title=f"CWL ROSTER -ROUND {self.round}" , colour=Color.random())
        clan_one = '\n'.join(user_data[0].values())
        # clan_two = '\n'.join(user_data[1].values())
        embed.add_field(name="LAZY CWL 15 -#2R0GRURJG" , value=f'{clan_one}')
        # embed.add_field(name="SHIELD LAZY CWL -#2GPLGG820" , value=f'{clan_two}')
        await interaction.response.defer()
        await interaction.message.edit(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple , label="LAZY CWL 15" , custom_id="1" , row=1)
    async def button_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        with open('datasheets/cwlrooster.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if interaction.user.id in user_data[0] :
            await interaction.response.send_message("You have already enrolled for the CWL." , ephemeral=True)
        else :
            user_data[0][interaction.user.id] = interaction.user.nick
            await self.update_embed(interaction , user_data)
            with open('datasheets/cwlrooster.pkl' , 'wb') as f :
                pickle.dump(user_data , f)

    '''@discord.ui.button(style=discord.ButtonStyle.green , label="SHEILD LAZY CWL" , custom_id="2" , row=1)
    async def button_callback1(self , interaction: discord.Interaction , button: discord.ui.button) :
        with open('datasheets/cwlrooster.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if interaction.user.id in user_data[1] :
            await interaction.response.send_message("You have already enrolled for the CWL." , ephemeral=True)
        else :
            user_data[1][interaction.user.id] = interaction.user.nick
            await self.update_embed(interaction , user_data)
            with open('datasheets/cwlrooster.pkl' , 'wb') as f :
                pickle.dump(user_data , f)'''

    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji="❌" , custom_id="3" , row=1)
    async def button_callbackcros(self , interaction: discord.Interaction , button: discord.ui.button) :
        with open('datasheets/cwlrooster.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if interaction.user.id in user_data[0] or interaction.user.id in user_data[1] :
            if interaction.user.id in user_data[0] :
                user_data[0].pop(interaction.user.id , None)
            if interaction.user.id in user_data[1] :
                user_data[1].pop(interaction.user.id , None)
            await self.update_embed(interaction , user_data)
            with open('datasheets/cwlrooster.pkl' , 'wb') as f :
                pickle.dump(user_data , f)
        else :
            await interaction.response.send_message("You have not enrolled for the CWL." , ephemeral=True)


class My_View(View) :
    def __init__(self , ctx , clan_name , last_updated , total_count , output) :
        super().__init__(timeout=100)
        self.ctx = ctx
        self.pageno = 0
        self.clan_name = clan_name
        self.total_count = total_count
        self.last_updated = last_updated
        self.output_msg = output
        self.last_page = len(output)

    async def update_embed(self , interaction) :
        embed = Embed(
            title=f"War Compo - {self.clan_name}\n\n★ TH : {16 - self.pageno if self.pageno < 5 else 'Less than Th 11'}\n\nTown hall   ~ weight   ~  Name\n" ,
            colour=Color.random())
        embed.description = f"{self.output_msg[self.pageno]}\n{self.last_updated}"
        embed.set_footer(text=f"{self.total_count}/50 ")
        await interaction.response.defer()
        await interaction.message.edit(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji='⬅️')
    async def button_callback2(self , interaction: discord.Interaction , button: discord.ui.button) :
        if self.pageno > 0 :
            self.pageno -= 1
            await self.update_embed(interaction)
        else :
            await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji='➡️')
    async def button_callback(self , interaction: discord.Interaction , button: discord.ui.button) :
        if self.pageno < self.last_page - 1 :
            self.pageno += 1
            await self.update_embed(interaction)
        else :
            await interaction.response.defer()


class clashofclansmethods(commands.Cog) :
    def __init__(self , client) :
        self.client = client

    @commands.hybrid_command(name="th" , help="Shows FWA bases for the town hall \nex : $th 12" , usage=f"{p}war")
    async def war(self , ctx , thlevel: int = None) :
        url16 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH16%3AWB%3AAAAABQAAAAKdkupDxXH2zHolZEYsi4Jy"
        url15 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH15%3AWB%3AAAAAQAAAAAHyGoAkx6dj6GPei5fv9aC4"
        url14 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH14%3AWB%3AAAAAKwAAAAIy_E5glvJjSIWnUv2njqcR"
        url13 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH13%3AWB%3AAAAAKwAAAAH9cXxV00w-5lJ2qCJCm8_v"
        url12 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH12%3AWB%3AAAAACwAAAAIzCgaxwgW1UGFUuSFMFvCu"
        url11 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH11%3AWB%3AAAAAKgAAAAH9X8-koI5OUOzBGQx4SKwQ"

        if thlevel is None :
            embed = Embed(title=f"➡ NOTE :" , colour=Color.random())
            embed.description = f"We Are Currently Recruiting The Players Of The Following TownHalls"
            image = r'templates/thall.png'
            image = discord.File(image)
            embed.set_image(url="attachment://thall.png")
            await ctx.send(embed=embed , file=image)
            for i in [16 , 15 , 14 , 13 , 12 , 11] :
                embed = Embed(title=f"<:th{i}:{COC.get_id(i)}>TH {i} FWA BASE LINK" , colour=Color.random())
                thlink = url16 if i == 16 else url15 if i == 15 else url14 if i == 14 else url13 if i == 13 else url12 if i == 12 else url11
                emoji = discord.utils.get(ctx.guild.emojis , id=int(COC.get_id(i)))
                if emoji is not None :
                    embed.set_thumbnail(url=emoji.url)
                embed.description = f'\n[💎Click here for base link💎]({thlink}) \n'
                embed.set_image(url=f"http://walkwithusclan.com/img/th{i}.jpg")
                await ctx.send(embed=embed)
        else :
            embed = Embed(title=f"<:th{thlevel}:{COC.get_id(int(thlevel))}>TH {thlevel} FWA BASE" ,
                          colour=Color.random())
            thlink = url16 if thlevel == 16 else url15 if thlevel == 15 else url14 if thlevel == 14 else url13 if thlevel == 13 else url12 if thlevel == 12 else url11
            emoji = discord.utils.get(ctx.guild.emojis , id=int(COC.get_id(thlevel)))
            if emoji is not None :
                embed.set_thumbnail(url=emoji.url)
            embed.description = f'[💎Click here for base link💎]({thlink})'
            embed.set_image(url=f"http://walkwithusclan.com/img/th{thlevel}.jpg")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="bases" , help="offical fwa bases" , usage=f"{p}bases")
    async def bases(self , ctx) :
        url16 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH16%3AWB%3AAAAABQAAAAKdkupDxXH2zHolZEYsi4Jy"
        url15 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH15%3AWB%3AAAAAQAAAAAHyGoAkx6dj6GPei5fv9aC4"
        url14 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH14%3AWB%3AAAAAKwAAAAIy_E5glvJjSIWnUv2njqcR"
        url13 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH13%3AWB%3AAAAAKwAAAAH9cXxV00w-5lJ2qCJCm8_v"
        url12 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH12%3AWB%3AAAAACwAAAAIzCgaxwgW1UGFUuSFMFvCu"
        url11 = "https://link.clashofclans.com/en?action=OpenLayout&id=TH11%3AWB%3AAAAAKgAAAAH9X8-koI5OUOzBGQx4SKwQ"
        embed = discord.Embed(title="💎 List of all FWA bases" ,
                              description=f"❯ Base: `TownHall 16`\n❯ Link: [Click here for TH16 FWA Base]({url16})\n\n❯ Base: `TownHall 15`\n❯ Link: [Click here for TH15 FWA Base]({url15})\n\n❯ Base: `TownHall 14`\n❯ Link: [Click here for TH14 FWA Base]({url14})\n\n❯ Base: `TownHall 13`\n❯ Link: [Click here for TH13 FWA Base]({url13})\n\n❯ Base: `TownHall 12`\n❯ Link: [Click here for TH12 FWA Base]({url12})\n\n❯ Base: `TownHall 11`\n❯ Link: [Click here for TH11 FWA Base]({url11})\n\nFor detailed infos about our bases, type: !th11 - !th12 - !th13 - !th14 - !th15 - !th16")
        embed.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEO0d84HSbpwy1s8PGoAg3gT6ksu_MeytKAg&usqp=CAU")
        await ctx.send(embed=embed)

    @commands.command(name="clan" , help="shows the information of the clan" ,
                      usage=f"{p}clan <none> optionol : <clan_tag> \nexample : {p}clan #2Q8URCU88")
    async def clan(self , ctx , target=None , render=True) :
        if render :
            await ctx.message.delete()
        clantag = None
        tags = None
        with open('datasheets/leader_userdata.pkl' , 'rb') as f :
            lead = pickle.load(f)
        if target is None or ctx.message.mentions :
            with open('datasheets/userdata.pkl' , 'rb') as f :
                user_data = pickle.load(f)
            if ctx.message.mentions :
                idd = ctx.message.mentions[0].id
            else :
                idd = ctx.author.id
            if idd in user_data.keys() :
                clantag = user_data[idd]['clan']
            else :
                embeed = Embed(title=f"No id is linked with the specific account" , color=Color.red())
                await ctx.send(embed=embeed)
                return
        else :
            if len(target) <= 3 :
                ctags = {'pl' : 'QL9998CC' , 'gv' : '8G2RJCP0' , "ts" : "U0LPRYL2" , 'bt' : '2G9URUGGC' ,
                         'av' : 'GC8QRPUJ'}
                clantag = ctags[target]
            elif len(target) >= 4 :
                clantag = target.strip('#')
            else :
                e = Embed(title="Please provide a clan tag or LINK your profile" , color=Color.red())
                await ctx.send(embed=e)
                return
        if clantag is None and tags is not None :
            clantag = COC.get_user(tag=tags)["clan"]["tag"].strip("#")
        clt = COC.getclan(tag=clantag.strip('#'))
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
                        f'<:cp:1161299634916966400> : {"1" if clt["clanCapital"] == {} else clt["clanCapital"]["capitalHallLevel"]}    ' \
                        f' <:members:1161298479050670162> : {clt["members"]}/50\n\n' \
                        f'<:saw:1159496168347291698> **Leader**  : \n<@{lead[clt["tag"].strip("#")] if clt["tag"].strip("#") in lead.keys() else "UNKOWN"}>'
        await ctx.send(embed=e)

    @commands.command(name="list_clan" , aliases=["lc"] , help="list all the clans" , usage=f"{p}list_clan")
    async def list_clan(self , ctx) :
        await ctx.message.delete()
        with open(r'datasheets\leader_userdata.pkl' , 'rb') as f :
            lead = pickle.load(f)
        clandata = await COC.list_of_clans()
        print(clandata)
        print(lead)
        for tag , clt in clandata.items() :
            e = Embed(title=f'**{clt["name"]}** - {tag}' ,
                      url=f'https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{tag.strip("#")}' ,
                      color=discord.Colour.random())
            e.set_thumbnail(url=clt["badge"])
            ccns = f'https://fwa.chocolateclash.com/cc_n/clan.php?tag={tag.strip("#")}'
            fwa = "https://sites.google.com/site/fwaguide/"
            cwl = "https://clashofclans.fandom.com/wiki/Clan_War_Leagues"
            cos = f'https://www.clashofstats.com/clans/{tag.strip("#")}'
            e.description = f'**Info** :\n\n' \
                            f'<:ccns:1159494607760003132> [**Clash of stats**]({cos})\n' \
                            f'💎 [**FWA**]({fwa})\n' \
                            f'<:see:1159496511701385297> [**CCNS**]({ccns})\n' \
                            f'⚔️ [**CWL**]({cwl})\n\n' \
                            f'<:cp:1161299634916966400> : {clt["clancapital"]}    ' \
                            f' <:members:1161298479050670162> : {clt["members"]}/50\n\n' \
                            f'<:saw:1159496168347291698> **Leader**  : \n<@{lead[tag.strip("#")] if tag.strip("#") in lead.keys() else "UNKOWN"}>'
            await ctx.send(embed=e)


    @commands.command(name="cwl" , help="get clan war league clan info" ,
                      usage=f"{p}cwl <tag> <th level> \neg :{p}cwl #2Q8URCU88 12 13 14")
    async def cwl(self , ctx , tag=None , *th) :
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
            e.description = f'\n**Info** :\n\n{clt["description"]} '
            e.add_field(name="\n\n**Town hall**\n" , value=f' {ths}')
            await ctx.send(embed=e)

    @commands.command(name="cwl-roster" , aliases=['cwlr'] , help="CWL rooster announcement")
    async def cwl_compo(self , ctx , round='') :
        await ctx.message.delete()
        await ctx.send(
            f"Hey <@&{1055418276546629682}>\n🔔🚨Select the clan below to enroll in the CWL compo. 🚨🔔\nIf you have not enrolled, we don't take any responsibility \nFirst come, first served.\n---------------------------------\n ")
        await ctx.send(f"CWL ROUND {round}" , view=cwlbutton(ctx , round))

    @commands.command(name="rest-cwl" , aliases=['rstcwl'] , help="CWL rooster rester")
    async def cwl_compo_rest(self , ctx) :
        user_data = [{} , {}]
        with open('datasheets/cwlrooster.pkl' , "wb") as f :
            pickle.dump(user_data , f)
        await ctx.send("CWL roster reseted")

    @commands.command(name="cwl-roster-info" , aliases=['cwlr-info'] , help="CWL rooster info")
    async def cwl_compo_info(self , ctx) :
        with open('datasheets/cwlrooster.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        embed = Embed(title=f"CWL ROSTER -ROUND {self.round}" , colour=Color.random())

    @commands.hybrid_command(name='listcompo' , help='list the individual war compo for every player in the clan ')
    async def listcompo(self , ctx , clan_tag: str = None) :
        with open('datasheets/userdata.pkl' , 'rb') as f :
            token = pickle.load(f)
        if clan_tag is None :
            if ctx.author.id in token.keys() :
                clan_tag = token[ctx.author.id]['clan']
            else :

                e = Embed(title="Please provide me a tag" , color=Color.red())
                await ctx.reply(embed=e)
                return
        else :
            clan_tag = clan_tag.strip("#")
        if clan_tag :
            try :
                clani = COC.fwa_clan_data(tag=clan_tag)

            except :
                e = Embed(title="Not a Fwa Clan" , color=Color.red())
                await ctx.reply(embed=e)
                return
            clan_weight = clani[1]
            output1 = output2 = output3 = output4 = output5 = outputelse = ""
            for player_name , player_data in clan_weight.items() :
                if player_data["eqvweight"] == 16 :
                    output1 += f'<:th{player_data["Town hall"]}:{COC.get_id(player_data["Town hall"])}> ~ <:th{player_data["eqvweight"]}:{COC.get_id(player_data["eqvweight"])}>   ~    {player_data["weight"]}  ~    `{player_name}`\n\n'
                elif player_data["eqvweight"] == 15 :
                    output2 += f'<:th{player_data["Town hall"]}:{COC.get_id(player_data["Town hall"])}> ~ <:th{player_data["eqvweight"]}:{COC.get_id(player_data["eqvweight"])}>   ~    {player_data["weight"]}  ~    `{player_name}`\n\n'
                elif player_data["eqvweight"] == 14 :
                    output3 += f'<:th{player_data["Town hall"]}:{COC.get_id(player_data["Town hall"])}> ~ <:th{player_data["eqvweight"]}:{COC.get_id(player_data["eqvweight"])}>   ~    {player_data["weight"]}  ~    `{player_name}`\n\n'
                elif player_data["eqvweight"] == 13 :
                    output4 += f'<:th{player_data["Town hall"]}:{COC.get_id(player_data["Town hall"])}> ~ <:th{player_data["eqvweight"]}:{COC.get_id(player_data["eqvweight"])}>   ~    {player_data["weight"]}  ~    `{player_name}`\n\n'
                elif player_data["eqvweight"] == 12 :
                    output5 += f'<:th{player_data["Town hall"]}:{COC.get_id(player_data["Town hall"])}> ~ <:th{player_data["eqvweight"]}:{COC.get_id(player_data["eqvweight"])}>   ~    {player_data["weight"]}  ~    `{player_name}`\n\n'
                elif player_data["eqvweight"] <= 11 :
                    outputelse += f'<:th{player_data["Town hall"]}:{COC.get_id(player_data["Town hall"])}> ~ <:th{player_data["eqvweight"]}:{COC.get_id(player_data["eqvweight"])}>   ~    {player_data["weight"]} ~    `{player_name}`\n\n'
                else :
                    pass
            clan_name: str = clani[0]
            last_updated: str = clani[2]
            counter_num: int = len(clan_weight.keys())
            e = Embed(title=f"War Compo - {clan_name}\n\n★ TH : 16\n\nTown hall   ~ weight   ~  Name\n" ,
                      color=Color.random())
            e.description = f"\n{output1}\n{last_updated}"
            e.set_footer(text=f"{counter_num}/50 ")
            output = [output1 , output2 , output3 , output4 , output5 , outputelse]
            view = My_View(ctx , clan_name , last_updated , counter_num , output)
            await ctx.reply(embed=e , view=view)

    @commands.hybrid_command(name="profile" , aliases=['p'] , help="Shows the profile of the user" ,
                             usage=f"{p}profile <none> or <user> \nexample: {p}profile @user")
    async def profile(self , ctx , player_tag=None , user: discord.Member = None) :
        with open('datasheets/userdata.pkl' , 'rb') as f :
            user_data = pickle.load(f)
        if player_tag is None and user is None :
            if ctx.author.id in user_data.keys() :
                player_tags = user_data[ctx.author.id]['tag'].strip('#')
            else :
                e = Embed(title="No data exists on this profile" , color=Color.red())
                await ctx.send(embed=e)
                return
        else :
            if user is not None or ctx.message.mentions :
                try :
                    user = ctx.message.mentions[0].id
                except :
                    user = user.id
                if user in user_data :
                    player_tags = user_data[user]['tag'].strip('#')
                else :
                    e = Embed(title="User not found " , color=Color.red())
                    await ctx.send(embed=e)
                    return
            elif player_tag is not None or ctx.message.startswith('#') :
                player_tags = player_tag.strip('#')
            else :
                e = Embed(description="No player tag is found on this profile" , color=Color.red())
                await ctx.send(embed=e)
                return
        if player_tags is not None :
            try :
                player = COC.get_user(tag=player_tags)
            except Exception as e :
                e = Embed(title="Error while fetching" , color=Color.red())
                e.description = str(e)
                await ctx.send(embed=e)
                return
            url = f'https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23{player["tag"].strip("#")}'
            e = Embed(title=f"{player['name']} - {player['tag']}" , url=url , color=Color.random())
            emoj = discord.utils.get(ctx.guild.emojis , id=int(COC.get_id(player["townHallLevel"])))
            ptag = player["tag"].strip('#')
            player_details = f'[{player["clan"]["name"]}](https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{player["clan"]["tag"].strip("#")}) \n Role : **{COC.get_role(player["role"])}**' if "clan" in player else "NO clan"
            e.description = f'[CCNS](https://fwa.chocolateclash.com/cc_n/member.php?tag=%23{ptag})   [COS](https://www.clashofstats.com/players/{ptag})\n' \
                            f'\n🏆 {player["trophies"]} \n{player_details}'
            heros = []
            for hero in player["heroes"] :
                hero_id = COC.get_hero_id(hero["name"])
                if hero_id is not None :
                    emoji_declartion = f'<:{str(hero["name"]).replace(" " , "")}:{hero_id}> {hero["level"]}'
                    heros.append(emoji_declartion)
            e.set_thumbnail(url=emoj.url)
            e.add_field(value=f'{" ".join(heros)}' , name="Heroes")
            e.set_footer(text=f"Done by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
            await ctx.send(embed=e)

    @commands.hybrid_command(name='warcompo' , help='claclulate the war compo basd on fwa data sheet')
    async def warcompo(self , ctx , clan_tag=None) :
        await ctx.defer()
        with open('datasheets/userdata.pkl' , 'rb') as f :
            token = pickle.load(f)
        if clan_tag is None :
            if ctx.author.id in token.keys() :
                clan_tag = token[ctx.author.id]['clan']
            else :
                e = Embed(title="Please provide me a tag" , color=Color.red())
                await ctx.reply(embed=e)
                return
        else :
            clan_tag = clan_tag.strip("#")
        if clan_tag :
            try :
                claninfoo = COC.fwa_clan_data(tag=clan_tag)
            except :
                e = Embed(title="Not a Fwa Clan" , color=Color.red())
                await ctx.reply(embed=e)
                return
            merged_info = {}
            average_townhalls = 0
            average_equivalent = 0
            output = ""
            clan_weight = claninfoo[1]
            total_sum_weight = 0
            NotWeighted = 0
            for i in clan_weight :
                if clan_weight[i]["weight"] > 0 :
                    total_sum_weight += clan_weight[i]["weight"]
                else :
                    NotWeighted += 1
            endingline = f'★ EstWeight: {total_sum_weight}  ({len(clan_weight.keys()) - NotWeighted} / {len(clan_weight.keys())}) '
            for player_name , player_data in clan_weight.items() :
                town_hall_level = player_data.get('Town hall')
                eqvweight = player_data.get('eqvweight')
                if town_hall_level is not None :
                    merged_info.setdefault(town_hall_level , {'actual_count' : 0 , 'equivalent' : 0})
                    merged_info[town_hall_level]['actual_count'] += 1
                if eqvweight is not None :
                    merged_info.setdefault(eqvweight , {'actual_count' : 0 , 'equivalent' : 0})
                    merged_info[eqvweight]['equivalent'] += 1
            for level , counts in merged_info.items() :
                output += f'<:th{level}:{COC.get_id(level)}> Townhall {level}   : {counts["actual_count"]}  ~ {counts["equivalent"]} \n\n'
                average_townhalls += int(level) * int(counts["actual_count"])
                average_equivalent += int(level) * int(counts["equivalent"])
            e = Embed(title=f"War Compo - {claninfoo[0]} " , color=Color.random())
            average = f'★ AvgTh : {round(average_townhalls / len(clan_weight.keys()) , 2)}  ~  {round(average_equivalent / len(clan_weight.keys()) , 2)}'
            e.description = output + f"\n{endingline}\n{average}\n{claninfoo[2]}"
            await ctx.reply(embed=e , ephemeral=True)


async def setup(bot) :
    await bot.add_cog(clashofclansmethods(bot))
