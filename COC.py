import requests
from setkey import auth
import random

header = {'Accept' : 'application/json' , 'Authorization' : auth}

verifyheaders = {'Content-Type' : 'application/json' , 'Authorization' : auth}





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
    else :
        return "1158776040525680694"

def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
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


if __name__ == '__main__' :
    print(get_user('9JVUQGYLQ'))
