import discord
from discord.ext import commands
import COC
import pickle
from discord import Embed , Color


class fuunctionmethods(commands.Cog) :
    def __init__(self , client) :
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def audit(self , ctx) :
        x , y , z = 0 , 0 , 0
        notinanyserver = []
        elites = []
        fwaa = []
        elite = ""
        noneelite = ""
        fwa = ""
        with open('datasheets/userdata.pkl' , 'rb') as f :
            userdata = pickle.load(f)
        guild = self.client.get_guild(1054435038881665024)
        guild2 = self.client.get_guild(1152220160028057660)
        for member in userdata.keys() :
            if guild.get_member(int(member)) :
                elite += f'{x}  . {member}\n'
                elites.append(member)

                x += 1
            elif guild2.get_member(int(member)) :
                fwa += f'{y}  . {member}\n'
                fwaa.append(member)
                y += 1
            else :
                noneelite += f'{z} . {member}\n'
                z += 1
                notinanyserver.append(member)

        embed = discord.Embed(title=f'Team elites -{len(elites)} ' , description=elite , colour=Color.random())
        embed2 = discord.Embed(title=f'empire x fwa -{len(fwaa)}' , description=fwa , colour=Color.random())
        embed3 = discord.Embed(title=f'Not in any server - {len(notinanyserver)}' , description=noneelite ,
                               colour=Color.random())
        embed4 = discord.Embed(title='count' ,
                               description=f"total:{len(userdata.keys())}\n Elite: {len(elites)}\n FWA: {len(fwaa)} \n None Elite: {len(notinanyserver)}" ,
                               colour=Color.random())
        await ctx.send(embeds=[embed , embed2 , embed3 , embed4])
        for outsider in notinanyserver :
            del userdata[outsider]
        with open('datasheets/userdata.pkl' , 'wb') as f :
            pickle.dump(userdata , f)
        await ctx.send(f'{len(userdata.keys())}')

    @commands.command(name='pm' , help="create a private chat using threads")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
    async def thread_add(self , ctx , thread_name=None , *members: discord.Member) :
        thread_name = thread_name if thread_name is not None else "Team X Elites"
        auto_archive_duration = 1440
        member_mentions = ' '.join([member.mention for member in members])
        output_message = f'{ctx.author.mention} has invited {member_mentions} to the thread'
        thread = await ctx.channel.create_thread(name=thread_name , auto_archive_duration=auto_archive_duration ,
                                                 invitable=False)
        await thread.send(output_message)

    @commands.command(name='deletethread' , aliases=['dt'])
    @commands.has_any_role('🔰ADMIN🔰')
    async def thread_delete(self , ctx) :
        if isinstance(ctx.channel , discord.Thread) :
            try :
                await ctx.channel.delete()
            except discord.errors.NotFound :

                pass
        else :
            await ctx.send('This command can only be used in a thread.')

    @commands.command(name='win-check' , aliases=['wc' , 'wincheck' ,  'winc'])
    async def win_check(self , ctx , tag : str= None) :
        with open('datasheets/userdata.pkl' , 'rb') as f :
            user_data = pickle.load(f)
        if ctx.message.mentions and ctx.message.mentions[0].id in user_data.keys():
            tag = user_data[ctx.message.mentions[0].id]['clan']
        if tag is None :
            if ctx.author.id in user_data.keys():
                tag = user_data[ctx.author.id]['clan']
            else:
                await ctx.send('Please provide a tag.')
                return
        else:
            tag = tag.strip('#')
        data = COC.get_points(tag)
        embed = discord.Embed(title=f"Win Check - {tag}" , colour=Color.random())
        embed.description = f"{data}"
        await ctx.send(embed=embed)





async def setup(client) :
    await client.add_cog(fuunctionmethods(client))
