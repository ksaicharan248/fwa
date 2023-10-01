import requests
from setkey import auth

header = {'Accept' : 'application/json' , 'Authorization' : auth}

verifyheaders = {'Content-Type' : 'application/json' , 'Authorization' : auth}


def verify(player , token) :
    player = player.strip('#')
    data = {"token" : token}
    url = f'https://api.clashofclans.com/v1/players/%23{player}/verifytoken'
    response = requests.post(url , headers=verifyheaders , json=data)
    s = response.json()
    return response.status_code,s


def get_user(tag) :
    reso = requests.get('https://api.clashofclans.com/v1/players/%23' + tag , headers=header)
    userinfo = reso.json()
    return userinfo


def get_id(th) :
    if th == 11 :
        return "1157932788683653170"
    elif th == 12 :
        return "1157933184529469471"
    elif th == 13 :
        return "1157933611337666620"
    elif th == 14 :
        return "1157934828784734299"
    else:
        return "1157934151584980993"


if __name__ == '__main__' :
    print(get_user('9JVUQGYLQ'))
