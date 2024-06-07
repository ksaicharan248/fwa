import asyncio

import discord
from discord.ext import commands
import COC
import pickle
from discord import Embed , Color


def stater_read() :
    with open('datasheets/warstarter.pkl' , 'rb') as file :
        data = pickle.load(file)
    return data



class refresh(discord.ui.View) :
    def __init__(self , ctx , update_value) :
        super().__init__(timeout=43200 * 2)
        self.ctx = ctx
        self.keys = stater_read()
        self.update_value = update_value

    @discord.ui.button(emoji="🔃" , style=discord.ButtonStyle.primary , custom_id="refresh")
    async def refresh(self , interaction: discord.Interaction , button: discord.ui.Button) :
        await interaction.response.defer()
        self.keys = stater_read()
        updated_keys = await COC.fetch_my_info(self.keys)
        stater_write(updated_keys)
        status_data = await COC.fetch_status_of_clans(updated_keys)
        self.update_value = status_data
        await self.update_embed(interaction)

    @discord.ui.button(emoji="🔍" , style=discord.ButtonStyle.primary , custom_id="stop")
    async def stop(self , interaction: discord.Interaction , button: discord.ui.Button) :
        await interaction.response.defer()
        league_tags = [key[4].strip("#") for key in self.update_value.values()]
        farm_league = await COC.fetch_clan_data_league(league_tags)
        await self.update_embed(interaction , farm_league)

    async def update_embed(self , interaction: discord.Interaction , farm_league=None) :
        embed = discord.Embed(title="Status" , colour=Color.random())
        emoji_league = {"Official FWA " : "💎" , "FWA Blacklisted " : "🤬" , "Global Farming League " : "🌍" ,
                        "Probably Orange China " : "🍊" , "1945 League " : "🍀" , 'No League Association' : '⚔️' ,
                        'No data' : ''}

        for tag , value in self.update_value.items() :
            league_info = ""
            if farm_league :
                league_name = farm_league.get(value[4].strip('#') , '')
                league_emoji = emoji_league.get(league_name , '')
                league_info = f"\nleague   : {league_name} {league_emoji}"

            embed.add_field(name=f"{self.keys[tag]['name']}  -  #{tag}" , value=(f"```name     : {value[1]}\n"
                                                                                 f"compo    : {f'{value[0]} ✅' if value[0] == 50 else f'{value[0]} ❌'}\n"
                                                                                 f"status   : {value[2]}\nopponent : {value[3]}\ntag      : {value[4]}{league_info}```") ,
                            inline=False)
        await interaction.message.edit(embed=embed)

    async def interaction_check(self , interaction: discord.Interaction) -> bool :
        if interaction.user != self.ctx.author :
            await interaction.response.send_message(f"Only {self.ctx.author.mention} can do this." , ephemeral=True)
            return False
        return True


class Buttons(discord.ui.View) :

    def __init__(self , ctx , data) :
        super().__init__(timeout=43200 * 2)
        self.data = data
        self.ctx = ctx
        self.used = []
        self.flag = True
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
        if self.flag :
            self.data[idx]['tick'] = "❌"
        else :
            self.data[idx]['tick'] = "✅"
        for tag , values in self.data.items() :
            player_data += f'{values["tick"]} {tag} : {values["name"]}\n'
        embed.description = f'```{player_data}```'
        with open('datasheets/warstarter.pkl' , 'wb') as file :
            pickle.dump(self.data , file)
        if self.flag :
            await interaction.response.defer()
            await interaction.message.edit(embed=embed)
            await interaction.followup.send(embed=embed_sent , ephemeral=True)
        else :
            await interaction.response.defer()
            await interaction.message.edit(embed=embed)

    @discord.ui.button(emoji="❌" , style=discord.ButtonStyle.primary , custom_id="close")
    async def close_stater(self , interaction , button) :
        await interaction.response.defer()
        if self.flag :
            self.flag = False
            await interaction.followup.send("Started Removing" , ephemeral=True)
        else :
            self.flag = True
            await interaction.followup.send("Removing stopped" , ephemeral=True)

    async def interaction_check(self , interaction) -> bool :
        # print(interaction.data,'vars(interaction.data)')
        if interaction.user == self.ctx.author and interaction.data["custom_id"] != "refresh" and interaction.data["custom_id"] != "close" :
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = f'Please invite my account below👇\n(Kindly let me know when it`s done🙂)\nIn-game name : {self.data[interaction.data["custom_id"]]["name"]}\nTag : #{interaction.data["custom_id"]}\nLink : \nhttps://link.clashofclans.com/en?action=OpenPlayerProfile&tag={interaction.data["custom_id"]} '
            tag = interaction.data["custom_id"]
            await self.update_embed(interaction , idx=tag , embed_sent=embed)
            return False
        else :
            return True


def stater_write(update_data) :
    with open('datasheets/warstarter.pkl' , 'wb') as file :
        pickle.dump(update_data , file)


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

    @commands.command(name='create' , aliases=['pm' , 'private-message'] , help="create a private chat using threads")
    @commands.has_any_role('🔰ADMIN🔰' , '💎FWA REPS💎' , '☘️CO-ADMIN☘️' , 'Staff')
    async def thread_add(self , ctx , thread_name="TEAM-ELITES X FWA" , *members: discord.Member) :
        print(type(thread_name))
        thread_name = thread_name if isinstance(thread_name , str) else "Team X Elites"
        auto_archive_duration = 1440
        member_mentions = ' '.join([member.mention for member in members])
        output_message = f'{ctx.author.mention} has invited {member_mentions} to the thread'
        thread = await ctx.channel.create_thread(name=thread_name , auto_archive_duration=auto_archive_duration ,
                                                 invitable=False)
        await thread.send(output_message)

    @commands.command(name='thread-remove' , aliases=['rt'] , help="remove a members from a thread")
    @commands.has_any_role('🔰ADMIN🔰')
    async def remve_from_thread(self , ctx , *members: discord.Member) :
        # Ensure the context is within a thread
        if isinstance(ctx.channel , discord.Thread) :
            # Remove the member from the current thread
            for member in members :
                await ctx.channel.remove_user(member)
        else :
            await ctx.send("This command can only be used inside a thread.")

    @commands.command(name='deletethread' , aliases=['dt'] , help="delete the current thread")
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

    @commands.command(name="starter" , aliases=['st'] , help="View the war starter list")
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

    @commands.command(name="add_acc" , help="add a account to the war starter list")
    @commands.is_owner()
    async def add_acc(self , ctx , *tags: str) :
        for tag in tags :
            tag = tag.strip('#')
            with open('datasheets/warstarter.pkl' , 'rb') as file :
                data = pickle.load(file)
            data[tag] = {'name' : 'name' , 'tick' : '✅'}
            final = await COC.fetch_my_info(data)
            with open('datasheets/warstarter.pkl' , 'wb') as file :
                pickle.dump(final , file)
            await ctx.send(f"Added {final[tag]['name']} with tag {tag} to the war starter list")

    @commands.command(name="remove_acc" , help="remove a account from the war starter list")
    @commands.is_owner()
    async def remove_acc(self , ctx , tag: str) :
        tag = tag.strip('#')
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        del data[tag]
        with open('datasheets/warstarter.pkl' , 'wb') as file :
            pickle.dump(data , file)
        await ctx.send(f"Removed {tag} from the war starter list")

    @commands.command(name="reset_s" , help="reset the war starter list")
    @commands.is_owner()
    async def clear_acc(self , ctx) :
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        for tag , value in data.items() :
            data[tag]['tick'] = '✅'
        with open('datasheets/warstarter.pkl' , 'wb') as file :
            pickle.dump(data , file)
        await ctx.send("Cleared the war starter list")

    @commands.command(name="status_s" , aliases=['sst'] , help="View the war starter status")
    @commands.is_owner()
    async def status_s(self , ctx) :
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        update_data = await COC.fetch_my_info(data)
        status_data = await COC.fetch_status_of_clans(update_data)

        embed = discord.Embed(title="Status" , colour=Color.random())
        for tag , value in status_data.items() :
            embed.add_field(name=f"{update_data[tag]['name']}  -  #{tag}" , value=(f"```name     : {value[1]}\n"
                                                                                   f"compo    : {f'{value[0]} ✅' if value[0] == 50 else f'{value[0]} ❌'}\n"
                                                                                   f"status   : {value[2]}\nopponent : {value[3]}\ntag      : {value[4]}```") ,
                            inline=False)

        stater_write(update_data)
        await ctx.send(embed=embed , view=refresh(ctx , status_data))

    @commands.command(name='downvote' , aliases=['down'] , help="down vote a player from the war starter list")
    @commands.is_owner()
    async def downvote(self , ctx , number: int) :
        with open('datasheets/warstarter.pkl' , 'rb') as file :
            data = pickle.load(file)
        data[list(data.keys())[number]]['tick'] = '✅'
        with open('datasheets/warstarter.pkl' , 'wb') as file :
            pickle.dump(data , file)
        await ctx.send(
            f"Downvoted {list(data.keys())[number]} - {data[list(data.keys())[number]]['name']} to the war starter list")

    async def delete_messages_in_channel(self , channel , user , channels_with_deletions) :
        deleted_messages_count = 0
        try :
            async for message in channel.history(limit=200) :
                if message.author == user :
                    try :
                        await message.delete()
                        deleted_messages_count += 1
                        if channel.name not in channels_with_deletions :
                            channels_with_deletions[channel.name] = 1
                        else :
                            channels_with_deletions[channel.name] += 1
                    except discord.Forbidden :
                        print(f"Bot does not have permission to delete message in {channel.mention}")
                    except discord.NotFound :
                        print(f"Message already deleted in {channel.mention}")
                    except discord.HTTPException as e :
                        print(f"Failed to delete a message in {channel.mention}: {e}")
        except discord.Forbidden :
            print(f"Bot does not have permission to fetch messages in {channel.mention}")
        except discord.HTTPException as e :
            print(f"Failed to fetch messages in {channel.mention}: {e}")
        return deleted_messages_count


    @commands.hybrid_command(name='delete_user_messages' , aliases=['dum'] , help="Delete user messages in guild")
    # @commands.has_permissions(manage_messages=True)
    @commands.has_any_role('🔰ADMIN🔰' , '☘️CO-ADMIN☘️' , 'Staff')
    async def delete_user_messages(self , ctx , user: discord.Member) :

        channels = ctx.guild.text_channels
        await ctx.send(f"Deleting messages from {user.display_name} in {ctx.guild.name} channels...")

        channels_with_deletions = {}
        tasks = []

        for channel in channels :
            tasks.append(self.delete_messages_in_channel(channel , user , channels_with_deletions))

        deleted_messages_count = sum(await asyncio.gather(*tasks))

        if deleted_messages_count > 0 :
            result_message = f"Deleted {deleted_messages_count} messages from {user.display_name} in the following channels:\n"
            for channel_name , count in channels_with_deletions.items() :
                result_message += f"- {channel_name}: {count} messages\n"
        else :
            result_message = f"No messages from {user.display_name} were found in any channels."

        await ctx.send(result_message)


async def setup(client) :
    await client.add_cog(fuunctionmethods(client))
