import requests
from setkey import auth
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



header = {'Accept' : 'application/json' , 'Authorization' : auth}

verifyheaders = {'Content-Type' : 'application/json' , 'Authorization' : auth}


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
    return userinfo


def getclan(tag) :
    resp = requests.get('https://api.clashofclans.com/v1/clans/%23' + tag , headers=header)
    claninfo = resp.json()
    return claninfo


def get_id(th) :
    if th == 11 :
        return "1157932788683653170"
    elif th == 12 :
        return "1157933184529469471"
    elif th == 13 :
        return "1157933611337666620"
    elif th == 14 :
        return "1157934828784734299"
    elif th == 15 :
        return "1158776040525680694"
    elif th == 16 :
        return "1184685970814156800"
    else:
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






def get_hero_id(id) :
    if id == "Barbarian King":
        return 1172564470984347678
    elif id == "Archer Queen":
        return 1172566801259954196
    elif id == "Grand Warden":
        return 1172565750133837844
    elif id == "Royal Champion":
        return 1172566389131841547
    else:
        return None




def fwa_clan_data(tag) :
    tag.strip("#")
    clan_weight = {}
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1024 , 768)
    driver.get(f"https://fwastats.com/Clan/{tag}/Weight")
    s = driver.find_element(By.CSS_SELECTOR , "#myTable > tbody > tr:nth-child(1) > td:nth-child(2) > span").text
    for i in range(1 , 51) :
        try :
            player_name = driver.find_element(By.CSS_SELECTOR ,
                                              f"#myTable > tbody > tr:nth-child({i}) > td:nth-child(2) > a").text
            town_hall_level = int(driver.find_element(By.CSS_SELECTOR ,
                                                      f"#myTable > tbody > tr:nth-child({i}) > td:nth-child(2) > span").text)
            weight = int(driver.find_element(By.CSS_SELECTOR ,
                                             f"#myTable > tbody > tr:nth-child({i}) > td:nth-child(3) > div > input").get_attribute(
                'value'))
            if weight > 150000 and weight <= 160000:
                equvweiht = 16
            elif weight > 140000 and weight <= 150000:
                equvweiht = 15
            elif weight > 130000 and weight <= 140000:
                equvweiht = 14
            elif weight > 120000 and weight <= 130000:
                equvweiht = 13
            elif weight > 110000 and weight <= 120000:
                equvweiht = 12
            elif weight >90000 and weight <= 110000:
                equvweiht = 11
            elif weight > 70000 and weight <= 90000:
                equvweiht = 10
            elif weight > 55000 and weight <= 70000:
                equvweiht = 9
            else:
                equvweiht = town_hall_level

            clan_weight[player_name] = {"Town hall" : town_hall_level , "weight" : weight ,
                                        "eqvweight" : equvweiht}
        except :
            pass
    last_date = driver.find_element(By.CSS_SELECTOR ,
                            "body > div.container.body-content.fill > div.alert.alert-success > strong").text
    return clan_weight ,last_date


def hoq(target=None , *  th) :
    ths = ""
    if target is not None :
        print(target)

    x = ""  # Initialize an empty string
    cidinfo = {1054453503084482580 : ["U0LPRYL2" , 1055418276546629682] ,
               1054458642541334599 : ["2Q8URCU88" , 1055418808833159189]}

if __name__ == '__main__' :

    print(get_user("9JVUQGYLQ"))
