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
            with open('userdata.pkl' , 'rb') as file :
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

                with open('userdata.pkl' , 'wb') as file :
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
            with open('leader_userdata.pkl' , 'rb') as f :
                leader_data = pickle.load(f)
            if clantag in leader_data.keys() :
                await ctx.send(f'{clan["name"]} Leader account is already linked to {user.mention}')
                return
            else :
                leader_data[clantag] = user.id
                with open('leader_userdata.pkl' , 'wb') as f :
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
            with open('userdata.pkl' , 'rb') as file :
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
                with open('userdata.pkl' , 'wb') as file :
                    pickle.dump(user_data , file)
                return


    @commands.command(name='setup')
    @commands.has_any_role('🔰ADMIN🔰' )
    async def setup(self , ctx , announcement_channel : int , clan_name : str , clantag : str , member_role : discord.Role ) :
        with open('clan_deltails.pkl' , 'rb') as file :
            clan_data = pickle.load(file)
        if clan_name in clan_data.keys() :
            clanInfo = COC.getclan(tag=clantag.strip('#'))
            clan_data[clan_name] = {'channel_id' : ctx.channel.id , 'roles' : [member_role.name , '🔰THE FARMERS MEMBERS🔰'] , 'clan' : clanInfo["name"] , 'announcement_channel' : announcement_channel}
            embed = Embed(title=f'setup completed' , description=f'channel id : <#{ctx.channel.id}> \nroles : <@&{member_role.id}> \nclan : {clanInfo["name"]} \nannouncement channel : <#{announcement_channel}>' , color=Color.random())
            await ctx.send(embed=embed)
        else:
            await ctx.send('Setup has already been done')

        with open('clan_deltails.pkl' , 'wb') as file :
            pickle.dump(clan_data , file)



    @commands.command(name='unlink' , help='To unlink your clash of clans account with your discord account' ,
                      usage=f'{p}unlink <none> or <@mention>')
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'WAL' , 'TSL' , 'HML' , 'Staff')
    async def un_link(self , ctx , member: discord.Member) :
        with open("userdata.pkl" , "rb") as file :
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
            with open("userdata.pkl" , "wb") as file :
                pickle.dump(user_data , file)
        else:
            e = Embed(title="Nothing to unlink" , color=Color.red())
            await ctx.send(embed=e)

    @commands.command(name='unlink-leader' , aliases=['ull'] , help="unlink a clan tag to a leader discord account" ,
                    usage=f"{p}unlink-leader <@metion user> or <tag>\neg : {p}link-leader @user or #2Q8URCU88")
    @commands.has_any_role('🔰ADMIN🔰')
    async def unlink_leader(self , ctx , tags: str = None) :
        await ctx.message.delete()
        with open('leader_userdata.pkl' , 'rb') as f :
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

        with open('leader_userdata.pkl' , 'wb') as f :
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




async def setup(client) :
    await client.add_cog(profile_link(client))
