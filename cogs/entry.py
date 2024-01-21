import discord
from discord.ui import Modal , View , Button , TextInput
from discord.ext import commands
import COC
import pickle



class NewModal(discord.ui.Modal , title="Link your profile") :
    name = discord.ui.TextInput(label='Name' , placeholder="Please enter your in-game name " ,
                                style=discord.TextStyle.short)
    playe_tag = discord.ui.TextInput(label='Player Tag' , placeholder="Please enter your player tag " ,
                                     style=discord.TextStyle.short)

    async def on_submit(self , interaction: discord.Interaction) :
        with open('datasheets/userdata.pkl' , 'rb') as file :
            user_data = pickle.load(file)
        if interaction.user.id in user_data.keys():
            e = discord.Embed(
                title=f"<:ver:1157952898362261564> You have already linked your account \nLinked account:\n{user_data[interaction.user.id]['name']} - {user_data[interaction.user.id]['tag']}" ,
                colour=discord.Color.random())
            await interaction.response.send_message(embed=e, ephemeral=True)
        else :
            try:
                player_data = COC.get_user(tag=self.playe_tag.value.strip('#'))
            except Exception as e:
                player_data = False
            if player_data:
                e2 = discord.Embed(
                    title=f'<:th{str(player_data["townHallLevel"])}:{COC.get_id(player_data["townHallLevel"])}>  {player_data["name"]} -{player_data["tag"]}' ,
                    color=discord.Color.random())
                e2.description = f'\n<:ver:1157952898362261564> Linked {player_data["tag"]} to {interaction.user.mention}'
                e2.set_footer(text=f"Linked by {interaction.user.display_name} " )
                await interaction.response.send_message(embed=e2, ephemeral=True)
                user_data[interaction.user.id] = {'tag' : player_data['tag'].strip('#') , 'name' : player_data['name'] ,
                                            'clan' : player_data['clan']['tag'] if 'clan' in player_data else 'no clan' ,
                                            'clanname' : player_data['clan']['name'] if 'clan' in player_data else 'no clan'}

                with open('datasheets/userdata.pkl' , 'wb') as file :
                    pickle.dump(user_data , file)

            else:
                e = discord.Embed(title="Invalid player tag" ,description=f'No data found on this tag \ntag : {self.playe_tag.value}', colour=discord.Color.red())
                await interaction.response.send_message(embed=e, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) :
        await interaction.response.send_message(error, ephemeral=True)



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
        await interaction.response.send_message(embed=e,ephemeral=True)



class EntrySystem(commands.Cog) :
    def __init__(self , client) :
        self.client = client

    @commands.command(name='linkform' , aliases=['lf'])
    async def linkform(self , ctx) :
        await ctx.message.delete()
        e = discord.Embed(title=f'WELCOME TO \n{ctx.guild.name}\n' ,
                          description='\n-------------------------------\nPlease click the following .  🔗 link button to link your profile with the Discord ID.' ,
                          colour=discord.Colour.blue())
        e.set_thumbnail(url='https://static.wikia.nocookie.net/clashofclans/images/1/1e/Boat.png/revision/latest/scale-to-width-down/100?cb=20230109004815')
        await ctx.send(embed=e , view=FeedbackModal())


async def setup(bot) :
    await bot.add_cog(EntrySystem(bot))
