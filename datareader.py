import asyncio
import aiohttp
import pickle
import setkey
from setkey import auth

async def fetch_clan_info(session, tag, header, clan_info):
    async with session.get('https://api.clashofclans.com/v1/clans/%23' + tag.strip('#'), headers=header) as resp:
        clt = await resp.json()
        clan_info[tag] = {
            "name": clt["name"],
            "badge": clt["badgeUrls"]["large"],
            'clancapital': "1" if clt["clanCapital"] == {} else clt["clanCapital"]["capitalHallLevel"]
        }

async def main():
    header = {'Accept' : 'application/json' , 'Authorization' : auth}

    clan_info = {}

    with open('datasheets/clan_deltails.pkl', 'rb') as f:
        data = pickle.load(f)

    clan_tags = [data[key]['clantag'] for key in data.keys()]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_clan_info(session, tag, header, clan_info) for tag in clan_tags]
        await asyncio.gather(*tasks)

    print(clan_info)

if __name__ == "__main__":
    asyncio.run(main())
