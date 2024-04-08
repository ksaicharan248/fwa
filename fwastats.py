import asyncio
import aiohttp


async def fetch_data(url) :
    async with aiohttp.ClientSession() as session :
        async with session.get(url) as response :
            if response.status == 200 :
                return await response.json()


async def get_nope(clan_tag="U0LPRYL2") :
    tasks = []
    for i in [3 , 2 , 1] :
        url = f"https://fwastats.com/Clan/{clan_tag.strip('#')}/WarMembers.json?warNo={i}"
        tasks.append(fetch_data(url))
    results = await asyncio.gather(*tasks)
    return results


async def main() :
    data1 , data2 , data3 = await get_nope()
    return data1 , data2 , data3


if __name__ == "__main__" :
    loop = asyncio.get_event_loop()
    import time

    start = time.time()
    data = loop.run_until_complete(main())
    print(time.time() - start)
    loop.close()
    clan_data = {}
    for i in [0 , 1 , 2] :
        clanname = data[i][0]['opponentName']
        zeroattcks = []
        oneattacks = []
        for player in data[i] :
            if player['stars1'] == 0 and player['stars2'] == 0 :
                zeroattcks.append(player)
            elif player['stars1'] == 0 or player['stars2'] == 0 :
                oneattacks.append(player)
        clan_data[clanname] = [zeroattcks , oneattacks]

    print(clan_data)

    for clan , clan_attacks in clan_data.items() :
        print(f'------------------{clan}--------------------------\n\n')
        attc0 = clan_attacks[0]
        attc1 = clan_attacks[1]
        print('----------------Zero attacks -----------------------')
        for player in attc0 :
            print(f"{player['position']} {player['name']} {player['stars1']} {player['stars2']}")
        print('----------------One attack -----------------------')
        for player in attc1 :
            print(f"{player['position']} {player['name']} {player['stars1']} {player['stars2']}")
        print('\n\n\n')
