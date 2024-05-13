import asyncio

import discord
from discord.ext import commands
import COC
import pickle
from discord import Embed , Color


class Buttons(discord.ui.View) :

    def __init__(self , ctx , data) :
        super().__init__(timeout=180)
        self.data = data
        self.ctx = ctx
        self.used = []
        self.count = 0  # Initialize count for tracking buttons per row
        row = 0  # Initialize row number
        for tag , values in self.data.items() :
            button = discord.ui.Button(label=values['name'] , style=discord.ButtonStyle.primary , row=row)
            button.custom_id = tag
            self.add_item(button)
            self.count += 1
            if self.count >= 3 :
                self.count = 0  # Reset count to start a new row
                row += 1  # Move to the next row

    async def update_embed(self , interaction , idx , embed_sent) :
        embed = discord.Embed(title="Starter" , colour=discord.Color.random())
        player_data = ""
        self.data[idx]['tick'] = "❌"
        for tag , values in self.data.items() :
            player_data += f'{values["tick"]} {tag} : {values["name"]}\n'
        embed.description = f'```{player_data}```'
        with open('datasheets/warstarter.pkl' , 'wb') as file :
            pickle.dump(self.data , file)
        await interaction.response.defer()
        await interaction.message.edit(embed=embed)
        await interaction.followup.send(embed=embed_sent , ephemeral=True)

    async def interaction_check(self , interaction) -> bool :
        if interaction.user == self.ctx.author :
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = f'Please invite my account below👇\n(Kindly let me know when it`s done🙂)\nIn-game name : {self.data[interaction.data["custom_id"]]["name"]}\nTag : #{interaction.data["custom_id"]}\nLink : \nhttps://link.clashofclans.com/en?action=OpenPlayerProfile&tag={interaction.data["custom_id"]} '
            tag = interaction.data["custom_id"]
            await self.update_embed(interaction , idx=tag , embed_sent=embed)
            return False
        else :
            return True



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

    @commands.command(name='create' ,aliases=['pm', 'private-message'], help="create a private chat using threads")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
    async def thread_add(self , ctx , thread_name=None , *members: discord.Member) :
        thread_name = thread_name if thread_name is not None else "Team X Elites"
        auto_archive_duration = 1440
        member_mentions = ' '.join([member.mention for member in members])
        output_message = f'{ctx.author.mention} has invited {member_mentions} to the thread'
        thread = await ctx.channel.create_thread(name=thread_name , auto_archive_duration=auto_archive_duration ,
                                                 invitable=False)
        await thread.send(output_message)

    @commands.command(name='thread-remove' , aliases=['rt'], help="remove a members from a thread")
    @commands.has_any_role('🔰ADMIN🔰')
    async def remve_from_thread(self , ctx , *members: discord.Member) :
        # Ensure the context is within a thread
        if isinstance(ctx.channel , discord.Thread) :
            # Remove the member from the current thread
            for member in members :
                await ctx.channel.remove_user(member)
        else :
            await ctx.send("This command can only be used inside a thread.")

    @commands.command(name='deletethread' , aliases=['dt'], help="delete the current thread")
    @commands.has_any_role('🔰ADMIN🔰')
    async def thread_delete(self , ctx) :
        if isinstance(ctx.channel , discord.Thread) :
            try :
                await ctx.channel.delete()
            except discord.errors.NotFound :

                pass
        else :
            await ctx.send('This command can only be used in a thread.')

    @commands.command(name='win-check' , aliases=['wc' , 'wincheck' , 'winc'] , help="check your win count")
    async def win_check(self , ctx , tag: str = None) :
        with open('datasheets/userdata.pkl' , 'rb') as f :
            user_data = pickle.load(f)
        if ctx.message.mentions and ctx.message.mentions[0].id in user_data.keys() :
            tag = user_data[ctx.message.mentions[0].id]['clan']
        if tag is None :
            if ctx.author.id in user_data.keys() :
                tag = user_data[ctx.author.id]['clan']
            else :
                await ctx.send('Please provide a tag.')
                return
        else :
            tag = tag.strip('#')
        data = COC.get_points(tag)
        embed = discord.Embed(title=f"Win Check - {tag}" , colour=Color.random())
        embed.description = f"{data}"
        await ctx.send(embed=embed)

    @commands.command(name="starter" , aliases=['st'], help = "View the war starter list")
    async def starter(self , ctx) :
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        if ctx.author.id == 765929481311354881 :
            player_data = ""
            embed = discord.Embed(title="Starter" , colour=Color.random())
            for tag , values in data.items() :
                player_data += f"{values['tick']}  #{tag} : {values['name']}\n"
            embed.description = f'```{player_data}```'

            await ctx.send(embed=embed , view=Buttons(ctx , data))

    @commands.command(name="add_acc",help="add a account to the war starter list")
    @commands.is_owner()
    async def add_acc(self , ctx , *tags : str) :
        for tag in tags:
            tag = tag.strip('#')
            with open('datasheets/warstarter.pkl' , 'rb') as file :
                data = pickle.load(file)
            data[tag] = {'name' : 'name' , 'tick' : '✅'}
            final = await COC.fetch_my_info(data)
            with open('datasheets/warstarter.pkl' , 'wb') as file :
                pickle.dump(final , file)
            await ctx.send(f"Added {final[tag]['name']} with tag {tag} to the war starter list")

    @commands.command(name="remove_acc", help="remove a account from the war starter list")
    @commands.is_owner()
    async def remove_acc(self , ctx , tag : str) :
        tag = tag.strip('#')
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        del data[tag]
        with open('datasheets/warstarter.pkl' , 'wb') as file :
            pickle.dump(data , file)
        await ctx.send(f"Removed {tag} from the war starter list")

    @commands.command(name="reset_s", help="reset the war starter list")
    @commands.is_owner()
    async def clear_acc(self , ctx) :
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        for tag , value in data.items() :
            data[tag]['tick'] = '✅'
        with open('datasheets/warstarter.pkl' , 'wb') as file :
            pickle.dump(data , file)
        await ctx.send("Cleared the war starter list")

    @commands.command(name="status_s" ,  aliases=['sst'])
    @commands.is_owner()
    async def status_s(self , ctx) :
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        copy_data = data.copy()
        for tag , value in data.items() :
            if value['tick'] != '❌' :
                del copy_data[tag]
        update_data = await COC.fetch_my_info(copy_data)
        status_data = await COC.fetch_status_of_clans(update_data)
        embed = discord.Embed(title="Status" , colour=Color.random())
        for tag , value in status_data.items() :
            embed.add_field(name=f"{update_data[tag]['name']}  -  #{tag}" , value=f"```name     : {value[1]}\ncompo    : {value[0]}\nstatus   : {value[2]}\nopponent : {value[3]}\ntag      : {value[4]}```" , inline=False)
        await ctx.send(embed=embed)








async def setup(client) :
    await client.add_cog(fuunctionmethods(client))
