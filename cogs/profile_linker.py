import COC
import discord
from discord.ext import commands
import pickle
from discord import Embed , Color

from main import p


class profile_link(commands.Cog) :
    def __init__(self , client) :
        self.client = client\

    @commands.hybrid_command(name='link' , help='To link your clash of clans account with your discord account' ,
                             usage=f'{p}link <#player_tag> \nexample : {p}link #2UVH89FH\n/link #2UVH89FH')
    async def link(self , ctx , player_tag=None) :
        await ctx.message.delete()
        if player_tag is None :
            e = Embed(title="Please provide the player tag ." , color=Color.random())
            await ctx.send(embed=e)
            return
        else :
            player_tag = player_tag.strip('#')
            with open('datasheets/userdata.pkl' , 'rb') as file :
                user_data = pickle.load(file)
            if ctx.author.id in user_data.keys() :
                e = Embed(
                    title=f"You have already linked your account <:ver:1157952898362261564>\nLinked account:{user_data[ctx.author.id]['name']} - {user_data[ctx.author.id]['tag']}" ,
                    colour=Color.random())
                await ctx.send(embed=e)
                return
            else :
                player = COC.get_user(tag=player_tag)
                e = Embed(
                    title=f'<:th{str(player["townHallLevel"])}:{COC.get_id(player["townHallLevel"])}>  {player["name"]} -{player["tag"]}' ,
                    color=Color.random())
                e.description = f'\n<:ver:1157952898362261564> Linked {player["tag"]} to {ctx.author.mention}'
                e.set_footer(text=f"Linked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
                await ctx.send(embed=e)
                user_data[ctx.author.id] = {'tag' : player['tag'].strip('#') , 'name' : player['name'] ,
                                            'clan' : player['clan']['tag'] if 'clan' in player else 'no clan' ,
                                            'clanname' : player['clan']['name'] if 'clan' in player else 'no clan'}

                with open('datasheets/userdata.pkl' , 'wb') as file :
                    pickle.dump(user_data , file)
                return

    @commands.command(name='link-leader' , aliases=['ll'] , help="link a clan tag to a leader discord account" ,
                      usage=f"{p}link-leader <@metion user> <tag>\n =eg : {p}link-leader @user #2Q8URCU88")
    @commands.has_any_role('🔰ADMIN🔰')
    async def link_leader(self , ctx , user: discord.Member , tag: str) :
        await ctx.message.delete()
        clantag = tag.strip("#")
        clan = COC.getclan(tag=clantag)
        if clan :
            with open('datasheets/leader_userdata.pkl' , 'rb') as f :
                leader_data = pickle.load(f)
            if clantag in leader_data.keys() :
                await ctx.send(f'{clan["name"]} Leader account is already linked to {user.mention}')
                return
            else :
                leader_data[clantag] = user.id
                with open('datasheets/leader_userdata.pkl', 'wb') as f :
                    pickle.dump(leader_data , f)
                e = discord.Embed(title=f"{user.mention} is linked to {clan['name']}")
                e.description = f'{clan["name"]} Leader account is now linked to {user.mention}'
                e.set_thumbnail(url=clan['badgeUrls']['medium'])
                await ctx.send(embed=e)
        else :
            await ctx.send('Please provide a valid clan tag.')

    @commands.hybrid_command(name='force-link' , aliases=['fl' , 'force_link' , 'force'] ,
                           help='To  link a player clash of clans account with a discord account' ,
                           usage=f'{p}force_link <@mention> <#player_tag> \nexample : {p}force_link @moon #JJ0Y71L2' ,
                           hidden=True)
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
    async def force_link(self , ctx , user_mention: discord.Member = None , player_tag=None) :
        await ctx.message.delete()
        if player_tag is None :
            e = Embed(title="Please provide the player tag ." , color=Color.red())
            await ctx.send(embed=e)
            return
        else :
            player_tag = player_tag.strip('#')
            with open('datasheets/userdata.pkl' , 'rb') as file :
                user_data = pickle.load(file)
            if user_mention.id in user_data.keys() :
                e = Embed(
                    title=f"{user_mention.mention} have already linked his account <:ver:1157952898362261564>\nLinked {user_data[user_mention.id]['name']} - {user_data[user_mention.id]['tag']}" ,
                    colour=Color.random())
                await ctx.send(embed=e)
                await ctx.send()
                return
            else :
                player = COC.get_user(tag=player_tag)
                e = Embed(
                    title=f'<:th{str(player["townHallLevel"])}:{COC.get_id(player["townHallLevel"])}>  {player["name"]} -{player["tag"]}' ,
                    color=Color.random())
                e.description = f'\n<:ver:1157952898362261564> Linked {player["tag"]} to {user_mention.mention}'
                e.set_footer(text=f"Linked by {ctx.author.display_name} " , icon_url=ctx.author.display_avatar)
                await ctx.send(embed=e)
                user_data[user_mention.id] = {'tag' : player['tag'].strip('#') , 'name' : player['name'] ,
                                              'clan' : player['clan']['tag'] if 'clan' in player else 'no clan' ,
                                              'clanname' : player['clan']['name'] if 'clan' in player else 'no clan'}
                with open('datasheets/userdata.pkl' , 'wb') as file :
                    pickle.dump(user_data , file)
                return


    @commands.command(name='setup')
    @commands.has_any_role('🔰ADMIN🔰' )
    async def setup(self , ctx , announcement_channel : int , clan_name : str , clantag : str , member_role : discord.Role ) :
        with open('datasheets/clan_deltails.pkl' , 'rb') as file :
            clan_data = pickle.load(file)
        if clan_name :
            clanInfo = COC.getclan(tag=clantag.strip('#'))
            clan_data[clan_name] = {'channel_id' : ctx.channel.id , 'roles' : [member_role.name , '🔰THE FARMERS MEMBERS🔰'] , 'clan' : clanInfo["name"] , 'announcement_channel' : announcement_channel}
            embed = Embed(title=f'setup completed' , description=f'channel id : <#{ctx.channel.id}> \nroles : <@&{member_role.id}> \nclan : {clanInfo["name"]} \nannouncement channel : <#{announcement_channel}>' , color=Color.random())
            await ctx.send(embed=embed)


        with open('datasheets/clan_deltails.pkl' , 'wb') as file :
            pickle.dump(clan_data , file)

    @commands.command(name="listsetup")
    @commands.has_any_role('🔰ADMIN🔰' )
    async def listsetup(self , ctx) :
        with open('datasheets/clan_deltails.pkl' , 'rb') as file :
            clan_data = pickle.load(file)
        for clan in clan_data.keys() :
            embed = Embed(title=f'{clan_data[clan]["clan"]} ' ,
                              description=f'channel id : <#{clan_data[clan]["channel_id"]}> \nroles : <@&{clan_data[clan]["roles"][0]}> \nclan : {clan_data[clan]["clan"]} \nannouncement channel : <#{clan_data[clan]["announcement_channel"]}>' ,
                          color=Color.random())
            await ctx.send(embed=embed)



    @commands.command(name='unlink' , help='To unlink your clash of clans account with your discord account' ,
                      usage=f'{p}unlink <none> or <@mention>')
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
    async def un_link(self , ctx , member: discord.Member) :
        with open("datasheets/userdata.pkl" , "rb") as file :
            user_data = pickle.load(file)
        if member.id in user_data.keys() :
            tag = user_data[member.id]['tag']
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
            with open("datasheets/userdata.pkl" , "wb") as file :
                pickle.dump(user_data , file)
        else:
            e = Embed(title="Nothing to unlink" , color=Color.red())
            await ctx.send(embed=e)

    @commands.command(name='unlink-leader' , aliases=['ull'] , help="unlink a clan tag to a leader discord account" ,
                    usage=f"{p}unlink-leader <@metion user> or <tag>\neg : {p}link-leader @user or #2Q8URCU88")
    @commands.has_any_role('🔰ADMIN🔰')
    async def unlink_leader(self , ctx , tags: str = None) :
        await ctx.message.delete()
        with open('datasheets/leader_userdata.pkl' , 'rb') as f :
            leader_user_data = pickle.load(f)
        if ctx.message.mentions[0].id in leader_user_data.values() :
            n = list(leader_user_data.keys())[list(leader_user_data.values()).index(ctx.message.mentions[0].id)]
            try :
                del leader_user_data[n]
            except :
                leader_user_data.pop(n)
            await ctx.send(f'{n} leader account is unlinked.')
        elif tags is not None :
            try :
                del leader_user_data[tags.strip("#")]
            except :
                leader_user_data.pop(tags.strip("#"))

        else :
            await ctx.send('Nothing happened as you wondered.')

        with open('datasheets/leader_userdata.pkl', 'wb') as f :
            pickle.dump(leader_user_data , f)

    @commands.command(name='kick' , aliases=['k'] , help='Kick a user' , usage=f'{p}kick <user> <reason>')
    @commands.has_any_role('🔰ADMIN🔰' , '☘️CO-ADMIN☘️')
    async def kick(self , ctx , member: discord.Member , * , reason=None) :
        owner = await self.client.fetch_user(int(765929481311354881))
        await ctx.send(f'{member.nick} has been flew from the server 🍃')
        await member.send(f"You have been kicked from {ctx.guild.name} for {reason}")
        await self.unlink(ctx , member=member)
        await owner.send(f'{member} removed from data base')
        await member.kick(reason=reason)


    @commands.command(name='update_info',aliases=['uinfo'] , help='To update your clash of clans account details with your discord account' ,usage=f'{p}update_info')
    async def update_information(self , ctx , member : discord.Member = None) :
        with open('datasheets/userdata.pkl') as file :
            user_info = pickle.load(file)
        if member is None:
            user_id = ctx.author.id
        else:
            user_id = member.id
        previous_data = user_info[user_id]
        coc_data  = COC.get_user(tag=user_info[user_id]['tag'])
        #775168480969621586: {'tag': 'LVG8YJVRP', 'name': 'AQUAMAN', 'clan': 'U0LPRYL2', 'clanname': 'THE SHIELD'}
        user_info[user_id] = {
            'tag': coc_data['tag'],
            'name': coc_data['name'],
            'clan': coc_data['clan']['tag'],
            'clanname': coc_data['clan']['name']
        }
        if previous_data == user_info[user_id]:
            embed = Embed(title=f'<:th{str(coc_data["townHallLevel"])}:{COC.get_id(coc_data["townHallLevel"])}>  {coc_data["name"]} -{coc_data["tag"]}' ,colour=Color.random())
            embed.description = f'\n```user : {ctx.author.mention if member is None else member.mention}\nname : {user_info[user_id]["name"]}\ntag  : {user_info[user_id]["tag"]}\nclanname : {user_info[user_id]["clanname"]}clan : {user_info[user_id]["clan"]}\n```'
            await ctx.send(embed=embed)
        else:
            embed1 = Embed(
                title=f'<:th{str(coc_data["townHallLevel"])}:{COC.get_id(coc_data["townHallLevel"])}>  {coc_data["name"]} -{coc_data["tag"]}' ,
                colour=Color.random())
            embed1.description = f'\n```user : {ctx.author.mention if member is None else member.mention}\nname : {previous_data["name"]}\ntag  : {previous_data["tag"]}\nclanname : {previous_data["clanname"]}clan : {previous_data["clan"]}\n```'
            await ctx.send(embed=embed1)
            embed = Embed(
                title=f'<:th{str(coc_data["townHallLevel"])}:{COC.get_id(coc_data["townHallLevel"])}>  {coc_data["name"]} -{coc_data["tag"]}' ,
                colour=Color.random())
            embed.description = f'\n```user : {ctx.author.mention if member is None else member.mention}\nname : {user_info[user_id]["name"]}\ntag  : {user_info[user_id]["tag"]}\nclanname : {user_info[user_id]["clanname"]}clan : {user_info[user_id]["clan"]}\n```'
            await ctx.send(embed=embed)
            with open('datasheets/userdata.pkl' , 'wb') as file :
                pickle.dump(user_info, file)
            await ctx.send('Updated')







async def setup(client) :
    await client.add_cog(profile_link(client))
