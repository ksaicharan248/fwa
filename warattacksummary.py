# https://fwa.chocolateclash.com/cc_n/clan.php?tag=U0LPRYL2
import asyncio
import time
import nope4
import aiohttp
import bs4
import re
import requests
import bs4
from bs4 import BeautifulSoup

fwa_count = 0


def get_clan_tags(tags) :
    url = f"https://fwa.chocolateclash.com/cc_n/clan.php?tag={tags.strip('#')}"
    response = requests.get(url)
    html_content = response.content
    soup = bs4.BeautifulSoup(html_content , 'html.parser')
    datta = soup.find_all('a')
    clan_user_tags = []
    for i in range(6 , 56) :
        if datta[i].get_text().isalnum() :
            clan_user_tags.append(f'#{datta[i].get_text()}')
        else :
            pass

    return clan_user_tags


def get_pins(tag , limit=15) :
    hrefs = []
    url = f"https://fwa.chocolateclash.com/cc_n/warlog.php?tag={tag.strip('#')}"
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content , 'html.parser')
    for tmplink in soup.find_all('a') :
        link = tmplink.get('href')
        if not link.find('warinspect') :
            last = link.find('warinspect.php?n=')
            hrefs.append(link[last + 17 :])
    return hrefs[:limit]


async def fetch_data(pin , offline ) :
    async with aiohttp.ClientSession() as session :
        url = f"https://fwa.chocolateclash.com/cc_n/warinspect.php?n={pin}"
        async with session.get(url) as response :
            html_content = await response.text()
            soup = bs4.BeautifulSoup(html_content , 'html.parser')
            datta = soup.find_all('tr')
            if datta and len(datta) > 1 :
                data_list = datta[1].get_text(separator=",").split(',')
                if data_list[6][0] == "O" and data_list[16][0] == "O" and (
                        data_list[4] == "#U0LPRYL2" or data_list[14] == "#U0LPRYL2") :
                    offline[0] += 1
                    for i in range(3 , 53) :
                        pos = i - 2
                        entries = datta[i].get_text(separator=",").split(',')
                        clan_index = data_list.index("#U0LPRYL2")
                        if clan_index == 4 :
                            player_attack = entries[:entries[1 :].index(str(pos)) + 1]
                        elif clan_index == 14 :
                            player_attack = entries[entries[1 :].index(str(pos)) + 1 :]
                        else :
                            pass
                        if len(player_attack) == 5 :
                            if player_attack[4][0] == 'N' :
                                if player_attack[2] in offline[1].keys() :
                                    offline[1][player_attack[2]]['zero'] += 1
                                else :
                                    offline[1][player_attack[2]] = {'name' : player_attack[1].strip(' (') , 'zero' : 1 ,
                                                                 'single' : 0}
                            else :
                                if player_attack[2] in offline[1].keys() :
                                    offline[1][player_attack[2]]['single'] += 1
                                else :
                                    offline[1][player_attack[2]] = {'name' : player_attack[1].strip(' (') , 'zero' : 0 ,
                                                                 'single' : 1}
                        else :
                            pass
                else :
                    pass
            else :
                pass


async def main(pins , offline ) :
    tasks = [fetch_data(pin , offline ) for pin in pins]
    await asyncio.gather(*tasks)


async def fetch_and_count_offline(pins) :
    offline = [0,{}]
    global fwa_count
    fwa_count = 0
    await main(pins , offline )
    return offline , fwa_count


if __name__ == "__main__" :
    start = time.time()

    data = {}
    clan_user_tags = get_clan_tags(tags="#U0LPRYL2")
    pins = get_pins(tag="#U0LPRYL2",limit=20)
    offline , _ = asyncio.run(fetch_and_count_offline(pins))
    sorted_players = sorted(offline[1].items() , key=lambda x : x[1]['zero'] , reverse=True)
    for key , value in sorted_players :
        if key in clan_user_tags and (value['zero'] > 1 or value['single'] > 1) :
            data[key] = value
            print(f"{key}: {value}")
    print(f"Total time taken: {time.time() - start:.2f} seconds")
    nope4.plot1(data , offline[0])
