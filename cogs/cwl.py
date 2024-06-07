import asyncio
import typing

import discord
from discord import Embed , Color , app_commands
from readwriter import *
from discord.ext import tasks , commands
from discord.ui import Button , View , Select
import COC
import pickle
import requests
from setkey import auth
from unwanted.nope6 import fetch_cwl
from emoji_utlis import find_emoji
from main import p
from datetime import datetime , timezone

header = {'Accept' : 'application/json' , 'Authorization' : auth}

verifyheaders = {'Content-Type' : 'application/json' , 'Authorization' : auth}

status_war = {"preparation" : ["War Starts in :" , "Preparation Day"] ,
                      "inWar" : ["Ending in :" , "Battle Day"] , "warEnded" : ["Ended :" , "War Ended"]}
def get_clan_info(cwl_info_ , pep , tag) :
    info = list(cwl_info_['rounds'][pep]['warTags'].values())[0]
    if info['clan']['tag'] == f"#{tag.strip('#')}" :
        return info['clan'] , info['opponent'] , info['state'] , info['teamSize'] , info['endTime'] if info[
                                                                                                           'state'] != 'preparation' else \
            info['startTime']
    else :
        return info['opponent'] , info['clan'] , info['state'] , info['teamSize'] , info['endTime'] if info[
                                                                                                           'state'] != 'preparation' else \
            info['startTime']

def sort_members_by_map_position(clan_info):
    return sorted(clan_info['members'], key=lambda member: member['mapPosition'])


def count_townhall_levels(data) :
    townhall_count = {}
    for member in data['members'] :
        townhall_level = member['townhallLevel']
        townhall_count[townhall_level] = townhall_count.get(townhall_level , 0) + 1
    new = dict(sorted(townhall_count.items() , reverse=True))
    return new




class round_select_menu(discord.ui.View) :
    def __init__(self , current_round , cwl_info ,clan_tag , method) :
        super().__init__(timeout=100)
        self.current_round = current_round
        self.cwl_info = cwl_info
        self.clan_tag = clan_tag
        self.method = method
        for i in range(1 , current_round +1 + 1) :
            self.callback.add_option(label=f'Round {i}' , value=str(i))

    async def update_embed(self , rounds , cwl_info, method) :
        if method == "lineup":
            current_clan_info , opponent_clan_info , current_state , teamsize , iso_timestamp = get_clan_info(cwl_info ,
                                                                                                              int(rounds)-1 ,
                                                                                                              self.clan_tag.strip(
                                                                                                                  '#'))
            embed = discord.Embed(title=f"War Lineup  \n{current_clan_info['name']}")
            embed.set_thumbnail(url=current_clan_info['badgeUrls']['large'])
            status_war = {"preparation" : ["War Starts in :" , "Preparation Day"] ,
                          "inWar" : ["Ending in :" , "Battle Day"] , "warEnded" : ["Ended :" , "War Ended"]}
            text = f"**War Against** \n" \
                   f"[{opponent_clan_info['name']} - {opponent_clan_info['tag']}]({COC.get_clan_link(opponent_clan_info['tag'])})\n" \
                   f"\n{status_war[current_state][1]} \nTeam size : {teamsize} \n\n**Lineup**\n"
            sorted_members = sort_members_by_map_position(current_clan_info)
            for index , member in enumerate(sorted_members) :
                text += f"{find_emoji(index + 1)} <:{member['townhallLevel']}:{COC.get_id(member['townhallLevel'])}>  {member['name']} \n"
            embed.description = text
            return embed

        elif method == 'info':
            current_clan_info , opponent_clan_info , current_state , teamsize , iso_timestamp = get_clan_info(cwl_info ,
                                                                                                              int(rounds)-1 ,
                                                                                                              self.clan_tag.strip(
                                                                                                                  '#'))
            embed = discord.Embed(title=f"{current_clan_info['name']}" , url=COC.get_clan_link(current_clan_info['tag']) ,
                                  colour=discord.Colour.random())
            embed.set_thumbnail(url=current_clan_info['badgeUrls']['large'])
            status_war = {"preparation" : ["War Starts in :" , "Preparation Day"] ,
                          "inWar" : ["Ending in :" , "Battle Day"] , "warEnded" : ["Ended :" , "War Ended"]}
            text = f"**War Against** \n" \
                   f"[{opponent_clan_info['name']} - {opponent_clan_info['tag']}]({COC.get_clan_link(opponent_clan_info['tag'])})\n" \
                   f"\n{status_war[current_state][1]} \nTeam size : {teamsize} vs {teamsize}\n" \
                   f"\n**{status_war[current_state][0]} <t:{int(datetime.strptime(iso_timestamp , '%Y%m%dT%H%M%S.%fZ').replace(tzinfo=timezone.utc).timestamp())}:R>**"
            if current_state != 'preparation' :
                text += "\n\n __**Stats **__ \n" \
                        f"`{' ' * (6 - len(str(current_clan_info['attacks'])))}{current_clan_info['attacks']}` <a:sword:1231435195811369082> `{opponent_clan_info['attacks']}{' ' * (6 - len(str(opponent_clan_info['attacks'])))}`\n" \
                        f"`{' ' * (6 - len(str(current_clan_info['stars'])))}{current_clan_info['stars']}` <a:sstar:1231596107839176836> `{opponent_clan_info['stars']}{' ' * (6 - len(str(opponent_clan_info['stars'])))}`\n" \
                        f"`{' ' * (6 - len(str(round(current_clan_info['destructionPercentage'] , 1))))}{round(current_clan_info['destructionPercentage'] , 1)}` <:ccns:1159494607760003132> `{round(opponent_clan_info['destructionPercentage'] , 1)}{' ' * (6 - len(str(round(opponent_clan_info['destructionPercentage'] , 1))))}`\n"
            text += f"\n\n **Rosters**\n"
            text += f"**{current_clan_info['name']}** \n"
            for key , value in count_townhall_levels(current_clan_info).items() :
                text += f" <:{key}:{COC.get_id(key)}> {find_emoji(value)} "
            text += f"\n\n**{opponent_clan_info['name']}** \n"
            for key , value in count_townhall_levels(opponent_clan_info).items() :
                text += f" <:{key}:{COC.get_id(key)}> {find_emoji(value)} "
            embed.description = text
            return embed


    @discord.ui.select(placeholder="Select Round" , min_values=1 , max_values=1)
    async def callback(self , interaction , select) :
        await interaction.response.defer()
        await interaction.message.edit(embed=await self.update_embed(select.values[0] , self.cwl_info, self.method) , view=self)


    async def on_timeout(self) -> None :
        for child in self.children :
            self.remove_child(child)


class CWL(commands.Cog) :
    def __init__(self , client) :
        self.client = client

    cwl_group =  app_commands.Group(name="cwl" , description="show cwl stats")
    @cwl_group.command(name="info" , description="show cwl stats")
    async def cwl_info(self , interaction: discord.Interaction , clan: typing.Optional[str] = "#2RPJPR8VY") :
        await interaction.response.defer()
        try :
            cwl_info = await fetch_cwl(tag=clan.strip("#") , header=header)
        except Exception as e :
            await interaction.followup.send(embed=discord.Embed(title=f"Error" , description=f"{e}"))
            return
        prep = -1
        for cwlround in cwl_info['rounds'] :
            if cwlround.get('warTags') and list(cwlround['warTags'].keys())[0] != '#0' :
                prep += 1
        current_clan_info , opponent_clan_info , current_state , teamsize , iso_timestamp = get_clan_info(cwl_info ,
                                                                                                          prep - 1 if prep != -1 else 0 ,
                                                                                                          clan.strip(
                                                                                                              '#'))
        embed = discord.Embed(title=f"{current_clan_info['name']}" , url=COC.get_clan_link(current_clan_info['tag']) ,
                              colour=discord.Colour.random())
        embed.set_thumbnail(url=current_clan_info['badgeUrls']['large'])

        text = f"**War Against** \n" \
               f"[{opponent_clan_info['name']} - {opponent_clan_info['tag']}]({COC.get_clan_link(opponent_clan_info['tag'])})\n" \
               f"\n{status_war[current_state][1]} \nTeam size : {teamsize} vs {teamsize}\n" \
               f"\n**{status_war[current_state][0]} <t:{int(datetime.strptime(iso_timestamp , '%Y%m%dT%H%M%S.%fZ').replace(tzinfo=timezone.utc).timestamp())}:R>**"
        if current_state != 'preparation' :
            text += "\n\n __**Stats **__ \n" \
                    f"`{' ' * (6 - len(str(current_clan_info['attacks'])))}{current_clan_info['attacks']}` <a:sword:1231435195811369082> `{opponent_clan_info['attacks']}{' ' * (6 - len(str(opponent_clan_info['attacks'])))}`\n" \
                    f"`{' ' * (6 - len(str(current_clan_info['stars'])))}{current_clan_info['stars']}` <a:sstar:1231596107839176836> `{opponent_clan_info['stars']}{' ' * (6 - len(str(opponent_clan_info['stars'])))}`\n" \
                    f"`{' ' * (6 - len(str(round(current_clan_info['destructionPercentage'] , 1))))}{round(current_clan_info['destructionPercentage'] , 1)}` <:ccns:1159494607760003132> `{round(opponent_clan_info['destructionPercentage'] , 1)}{' ' * (6 - len(str(round(opponent_clan_info['destructionPercentage'] , 1))))}`\n"
        text += f"\n\n **Rosters**\n"
        text += f"**{current_clan_info['name']}** \n"
        for key , value in count_townhall_levels(current_clan_info).items() :
            text += f" <:{key}:{COC.get_id(key)}> {find_emoji(value)} "
        text += f"\n\n**{opponent_clan_info['name']}** \n"
        for key , value in count_townhall_levels(opponent_clan_info).items() :
            text += f" <:{key}:{COC.get_id(key)}> {find_emoji(value)} "
        embed.description = text
        await interaction.followup.send(embed=embed , view=round_select_menu(current_round=prep , cwl_info=cwl_info,clan_tag=clan.strip("#"),method='info'))

    @cwl_group.command(name="lineup" , description="Get the roster of the clan")
    async def cwl_lineup(self , interaction: discord.Interaction , clan: typing.Optional[str] = "#2RPJPR8VY") :
        await interaction.response.defer()
        try :
            cwl_info = await fetch_cwl(tag=clan.strip("#") , header=header)
        except Exception as e :
            await interaction.followup.send(embed=discord.Embed(title=f"Error" , description=f"{e}"))
            return
        prep = -1
        for cwlround in cwl_info['rounds'] :
            if cwlround.get('warTags') and list(cwlround['warTags'].keys())[0] != '#0' :
                prep += 1
        current_clan_info , opponent_clan_info , current_state , teamsize , iso_timestamp = get_clan_info(cwl_info ,
                                                                                                          prep - 1 if prep != -1 else 0 ,
                                                                                                          clan.strip(
                                                                                                              '#'))
        embed = discord.Embed(title=f"War Lineup  \n{current_clan_info['name']}")
        embed.set_thumbnail(url=current_clan_info['badgeUrls']['large'])
        text = f"**War Against** \n" \
               f"[{opponent_clan_info['name']} - {opponent_clan_info['tag']}]({COC.get_clan_link(opponent_clan_info['tag'])})\n" \
               f"\n{status_war[current_state][1]} \nTeam size : {teamsize} \n\n**Lineup**\n"
        sorted_members = sort_members_by_map_position(current_clan_info)
        for index , member in enumerate(sorted_members) :
            text += f"{find_emoji(index+1)} <:{member['townhallLevel']}:{COC.get_id(member['townhallLevel'])}>  {member['name']} \n"
        embed.description = text
        await interaction.followup.send(embed=embed , view=round_select_menu(current_round=prep,cwl_info=cwl_info,clan_tag=clan.strip("#"),method="lineup"))

    @cwl_lineup.autocomplete('clan')
    async def cwl_lineup(self , interaction: discord.Interaction , current: str) -> typing.List[
        app_commands.Choice[str]] :
        data = []
        cwl_clan_data = read_data()
        for tag , value in cwl_clan_data.items() :
            data.append(app_commands.Choice(name=f'{value["name"]} - {tag}' , value=tag))

        return data


    @cwl_info.autocomplete('clan')
    async def cwl_stats(self , interaction: discord.Interaction , current: str) -> typing.List[
        app_commands.Choice[str]] :
        data = []
        cwl_clan_data = read_data()
        for tag , value in cwl_clan_data.items() :
            data.append(app_commands.Choice(name=f'{value["name"]} - {tag}' , value=tag))

        return data


async def setup(client) :
    await client.add_cog(CWL(client))
