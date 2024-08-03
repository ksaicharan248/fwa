import requests
from setkey import auth
import asyncio
import aiohttp
import pickle
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

header = {'Accept' : 'application/json' , 'Authorization' : auth}

verifyheaders = {'Content-Type' : 'application/json' , 'Authorization' : auth}



def get_clan_link(tag):
    return f"https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{tag.strip('#')}"

def get_playe_link(tag):
    return f"https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23{tag.strip('#')}"

def verify(player , token) :
    player = player.strip('#')
    data = {"token" : token}
    url = f'https://api.clashofclans.com/v1/players/%23{player}/verifytoken'
    response = requests.post(url , headers=verifyheaders , json=data)
    s = response.json()
    return response.status_code , s


def get_user(tag) :
    reso = requests.get('https://api.clashofclans.com/v1/players/%23' + tag , headers=header)
    userinfo = reso.json()
    if reso.status_code == 200 :
        return userinfo
    else :
        raise Exception(f"{userinfo}")


def getclan(tag: str) :
    resp = requests.get('https://api.clashofclans.com/v1/clans/%23' + tag.strip('#') , headers=header)
    claninfo = resp.json()
    return claninfo


def getclaninfo() :
    # resso = requests.get('https://api.clashofclans.com/v1/clans/%23U0LPRYL2/warlog?limit=1',headers=header)
    # laninfoo = resso.json()
    url = f'https://api.clashofclans.com/v1/clans/%23U0LPRYL2/warlog?limit=1'
    response = requests.get(url , headers=header)

    # Check if the request was successful (status code 200)
    if response.status_code == 200 :
        # Parse the JSON response
        data = response.json()
        print(data)

        # Extract and print information about each member
        for member in data['memberList'] :
            member_name = member['name']
            war_win_bonus = member['warWinBonus']
            print(f"{member_name}: War Win Bonus - {war_win_bonus}")
    else :
        print(f"Error: {response.status_code}")
        print(response.text)  # return claninfoo


# Associate Professor


def get_id(th) :
    if th == 11 :
        return "1157932788683653170"
    elif th == 12 :
        return "1269136504643653733"
    elif th == 13 :
        return "1250758290384879668"
    elif th == 14 :
        return "1250758245493116938"
    elif th == 15 :
        return "1250758155722428438"
    elif th == 16 :
        return "1250758139427426374"
    else :
        return "1184693650907746324"


def get_random_color() :
    r = random.randint(0 , 255)
    g = random.randint(0 , 255)
    b = random.randint(0 , 255)
    hex_color = f'#{r:02X}{g:02X}{b:02X}'
    return hex_color


def get_role(role: str) :
    if role == "leader" :
        return "Leader"
    elif role == "coLeader" :
        return "Co-Leader"
    elif role == "admin" :
        return "Elder"
    else :
        return "Member"


def get_prefix(role: str) :
    if role == "leader" :
        return "Lead - "
    elif role == "coLeader" :
        return "Co - "
    elif role == "admin" :
        return "Eld - "
    else :
        return "Mb - "


def getcoc(tag) :
    link = f"https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{tag}"
    return link


def leaugeid(id) :
    if id == 48000010 :
        return "https://static.wikia.nocookie.net/clashofclans/images/c/c9/WarCrystalIII.png/revision/latest/?cb=20181024140227"
    elif id == 48000011 :
        return "https://static.wikia.nocookie.net/clashofclans/images/5/5a/WarCrystalII.png/revision/latest/?cb=20181024140227"
    elif id == 48000012 :
        return "https://static.wikia.nocookie.net/clashofclans/images/8/8a/WarCrystalI.png/revision/latest/?cb=20181024140227"
    elif id == 48000013 :
        return "https://static.wikia.nocookie.net/clashofclans/images/3/39/WarMasterIII.png/revision/latest/?cb=20181024140227"
    elif id == 48000014 :
        return "https://static.wikia.nocookie.net/clashofclans/images/8/81/WarMasterII.png/revision/latest/?cb=20181024140227"
    elif id == 48000015 :
        return "https://static.wikia.nocookie.net/clashofclans/images/5/53/WarMasterI.png/revision/latest/?cb=20181024140227"
    elif id == 48000016 :
        return "https://static.wikia.nocookie.net/clashofclans/images/d/d2/WarChampionIII.png/revision/latest/?cb=20181024140228"
    elif id == 48000017 :
        return "https://static.wikia.nocookie.net/clashofclans/images/b/bd/WarChampionII.png/revision/latest/?cb=20181024140228"
    elif id == 48000018 :
        return "https://static.wikia.nocookie.net/clashofclans/images/e/e3/WarChampionI.png/revision/latest/?cb=20181024140228"


def ccns_check(tag: str) :
    url = f"https://fwa.chocolateclash.com/cc_n/member.php?tag={tag.strip('#')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text , "html.parser")
    if soup.select_one('#top > span > b') is not None :
        return [False , False]
    elif soup.select_one('#top > span:nth-child(1)') is not None :
        return [False , True]
    else :
        return [True , True]


def get_points(tag) :
    url = f'https://fwapoints.chocolateclash.com/clan?tag={tag.strip("#")}'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content , 'html.parser')
    winbox = soup.select_one('body > p.winner-box').text

    def find_numeric_positions(tsing) :
        count = 0
        for i in range(len(tsing)) :
            if tsing[i].isdigit() :
                count += 1
        return count

    # Find the index where the string needs to be broken
    break_index_i = winbox.find('Sync #')
    soppe = winbox[break_index_i :break_index_i + 6 + 10]

    break_index_1 = winbox.find('Sync #') + len('Sync #') + find_numeric_positions(soppe)
    break_index_2 = winbox.find('):') + 2

    line1 = winbox[:break_index_1] + '\n' + winbox[break_index_1 :break_index_2] + '\n' + winbox[break_index_2 :]
    return line1


def get_hero_id(id) :
    if id == "Barbarian King" :
        return 1269133097186623528
    elif id == "Archer Queen" :
        return 1269133328150433927
    elif id == "Grand Warden" :
        return 1269133505720487948
    elif id == "Royal Champion" :
        return 1269133507666378792
    else :
        return None


async def fwa_clan_data(tag) :
    url = f"https://fwastats.com/Clan/{tag.strip('#')}/Members.json"
    url2 = f"https://fwastats.com/Clan/{tag.strip('#')}/Weight"

    async with aiohttp.ClientSession() as session :
        async with session.get(url) as response :
            clan_data = await response.json()

        async with session.get(url2) as response :
            html = await response.text()
            soup = BeautifulSoup(html , "html.parser")
            clan_name = soup.select_one('body > div.container.body-content.fill > div.well > div > div > h3').text
            try :
                try :
                    last_date = soup.select_one(
                        'body > div.container.body-content.fill > div.alert.alert-success > strong').text
                except :
                    last_date = soup.select_one(
                        'body > div.container.body-content.fill > div.alert.alert-warning > strong').text
            except :
                last_date = "Clan weight submission was too long ago or did not found"

    clan_weight = {}
    for member in clan_data :
        try :
            player_name = member['name']
            town_hall_level = member['townHall']
            weight = int(member['weight'])
            if 150000 < weight <= 160000 :
                equivalent = 16
            elif 140000 < weight <= 150000 :
                equivalent = 15
            elif 130000 < weight <= 140000 :
                equivalent = 14
            elif 120000 < weight <= 130000 :
                equivalent = 13
            elif 110000 < weight <= 120000 :
                equivalent = 12
            elif 90000 < weight <= 110000 :
                equivalent = 11
            elif 70000 < weight <= 90000 :
                equivalent = 10
            elif 55000 < weight <= 70000 :
                equivalent = 9
            else :
                equivalent = town_hall_level
            clan_weight[player_name] = {"Town hall" : town_hall_level , "weight" : weight , "eqvweight" : equivalent}
        except AttributeError :
            pass
    sorted_clan_weight = dict(sorted(clan_weight.items() , key=lambda item : item[1]["weight"] , reverse=True))

    return clan_name , sorted_clan_weight , last_date


async def fetch_clan_info(session , tag , header , clan_info) :
    async with session.get('https://api.clashofclans.com/v1/clans/%23' + tag.strip('#') , headers=header) as resp :
        clt = await resp.json()
        clan_info[tag] = {"name" : clt["name"] , "badge" : clt["badgeUrls"]["large"] ,
                          'clancapital' : "1" if clt["clanCapital"] == {} else clt["clanCapital"]["capitalHallLevel"] ,
                          'clan_level' : clt["clanLevel"] , 'members' : clt["members"]}


async def list_of_clans() :
    header = {'Accept' : 'application/json' , 'Authorization' : auth}
    clan_info = {}
    with open('datasheets/clan_deltails.pkl' , 'rb') as f :
        data = pickle.load(f)
    clan_tags = [data[key]['clantag'] for key in data.keys()]
    async with aiohttp.ClientSession() as session :
        tasks = [fetch_clan_info(session , tag , header , clan_info) for tag in clan_tags]
        await asyncio.gather(*tasks)

    clan_info = dict(sorted(clan_info.items() , key=lambda item : item[1]['clan_level'] , reverse=True))
    return clan_info


async def fetch_user_info(tag , id , headers , session) :
    if tag :
        url = f'https://api.clashofclans.com/v1/players/%23{tag}'
        async with session.get(url , headers=headers) as response :
            userinfo = await response.json()
            if response.status == 200 :
                return id , userinfo
            else :
                return id , None
    else :
        return id , None


async def fetch_users_info(tags_dict , headers=header) :
    async with aiohttp.ClientSession() as session :
        tasks = [fetch_user_info(tag , id , headers , session) for id , tag in tags_dict.items()]
        results = await asyncio.gather(*tasks)
        return {user[0] : user[1] for user in results}


async def fetch_mu_list(tag , tick , headers , session) :
    if tag :
        url = f'https://api.clashofclans.com/v1/players/%23{tag}'
        async with session.get(url , headers=headers) as response :
            userinfo = await response.json()
            if response.status == 200 :
                return tag , {"name" : userinfo["name"] , "level" : userinfo["townHallLevel"] ,
                              "tick" : f"{tick if tick else '✅'}" ,
                              "clantag" : userinfo["clan"]["tag"] if userinfo.get("clan") else "No clan"}
            else :
                return tag , None
    else :
        return tag , None


async def fetch_my_info(tags_dict , headers=header) :
    async with aiohttp.ClientSession() as session :
        tasks = [fetch_mu_list(tag , value['tick'] , headers=headers , session=session) for tag , value in
                 tags_dict.items()]
        results = await asyncio.gather(*tasks)
        result = {user[0] : user[1] for user in results}
        result = dict(sorted(result.items() , key=lambda item : item[1]['level'] , reverse=True))
        return result


async def fetch_status_of_user(session , key , value) :
    global header
    base_url = "https://api.clashofclans.com/v1/clans/%23"
    url1 = f"{base_url}{value.strip('#')}"
    url2 = f"{base_url}{value.strip('#')}/currentwar"
    async with session.get(url1 , headers=header) as response1 , session.get(url2 , headers=header) as response2 :
        data1 = await response1.json()
        data2 = await response2.json()
        return key , (
        data1["members"] if data1.get("members") else "No members" ,
        data1["name"] if data1.get("name") else "No name" ,
        data2["state"] if data2.get("state") else "No state" ,
        data2["opponent"]["name"] if data2.get("opponent") and data2["opponent"].get("name") else "No opponent" ,
        data2["opponent"]["tag"] if data2.get("opponent") and data2["opponent"].get("tag") else "No opponent")


async def fetch_status_of_clans(keys) :
    async with aiohttp.ClientSession() as session :
        tasks = [fetch_status_of_user(session , key , value["clantag"]) for key , value in keys.items() if
                 value["tick"] != "✅"]
        results = await asyncio.gather(*tasks)
    results_dict = {key : data for key , data in results}
    return results_dict


async def fetch_clan_data_league(tags) :
    async def get_data(tag) :
        if tag == "No clan" :
            return tag , f"No data"
        url = f'https://fwa.chocolateclash.com/cc_n/clan.php?tag={tag}'
        async with aiohttp.ClientSession() as session :
            async with session.get(url) as response :
                if response.status != 200 :
                    raise "Error fetching data"

                text = await response.text()
                soup = BeautifulSoup(text , 'html.parser')

                top_element = soup.select_one('#top')
                if not top_element :
                    return tag , f"No data"

                text = top_element.text
                text_index = text.find('Association: ') + 13

                if text[text_index :].startswith("N") :
                    return tag , text[text_index :].replace('\n' , '')
                else :
                    lastindex = text[text_index :].find('(')
                    if lastindex == -1 :
                        return f"No data"
                    return tag , text[text_index :text_index + lastindex].replace('\n' , '')

    clan_acc = {}
    tasks = [get_data(tag) for tag in tags ]
    results = await asyncio.gather(*tasks)
    for result in results :
        clan_acc[result[0]] = result[1]
    return clan_acc


async def fetch_cwl(tag , header) :
    tag = tag.strip("#")
    base_url = 'https://api.clashofclans.com/v1'

    async def fetch_json(url) :
        async with aiohttp.ClientSession(headers=header) as session :
            async with session.get(url) as response :
                if response.status == 200  or response.status == 404 :
                    return await response.json() if response.status == 200 else "Not Found"
                else :
                    print(f"Failed to fetch data: {response}")
                    return None

    # Fetch the clan's current war league group
    league_group_url = f'{base_url}/clans/%23{tag}/currentwar/leaguegroup'
    clan_info = await fetch_json(league_group_url)
    if clan_info == "Not Found" :
        raise "This clan is not participating in a clan war League"
        return None
    for round_info in clan_info['rounds'] :
        round_info['warTags'] = {war_tag : {} for war_tag in round_info['warTags']}

    async def fetch_war_details(war_tag , round_idx , war_tag_key) :
        war_tag = war_tag_key.strip("#")
        war_url = f'{base_url}/clanwarleagues/wars/%23{war_tag}'
        war_info1 = await fetch_json(war_url)
        war_info = war_info1 if (
                war_info1['opponent']['tag'] == f"#{tag}" or war_info1['clan']['tag'] == f'#{tag}') else {}

        if not war_info :
            del(clan_info['rounds'][round_idx]['warTags'][war_tag_key])
        else:
            clan_info['rounds'][round_idx]['warTags'][war_tag_key] = war_info

    tasks = []
    for round_idx , round_info in enumerate(clan_info['rounds']) :
        for war_tag_key in round_info['warTags'].keys() :
            if war_tag_key != "#0" :
                tasks.append(fetch_war_details(war_tag_key , round_idx , war_tag_key))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)
    return clan_info



if __name__ == '__main__' :
    print(getclan("#2QGRUR0JQ"))
