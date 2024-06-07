import pickle


def read_starter():
    with open('./datasheets/warstarter.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

def write_starter(data):
    with open('./datasheets/warstarter.pkl', 'wb') as file:
        pickle.dump(data, file)



def write_leader(data):
    with open('./datasheets/leader_userdata.pkl', 'wb') as file:
        pickle.dump(data, file)

def read_leader():
    with open('./datasheets/leader_userdata.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


def read_user(data):
    with open('./datasheets/userdata.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
def write_user(data):
    with open('./datasheets/userdata.pkl', 'wb') as file:
        pickle.dump(data, file)


def read_data():
    with open('./datasheets/cwldata.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

def write_data(data):
    with open('./datasheets/cwldata.pkl', 'wb') as file:
        pickle.dump(data, file)


if __name__ == '__main__':
    data = {
        '#2RYGCY2QJ':{'name': 'TEAM ELITES', 'round1':'', 'round2':'', 'round3':'', 'round4':'', 'round5':'', 'round6':'', 'round7':''},
        '#2J28YUU0R': {'name': 'THE ELITES', 'round1':'', 'round2':'', 'round3':'', 'round4':'', 'round5':'', 'round6':'', 'round7':''},
        '#2RV9P0RCL': {'name': 'LAZY CWL - 15', 'round1':'', 'round2':'', 'round3':'', 'round4':'', 'round5':'', 'round6':'', 'round7':''},
        '#2RPJPR8VY' : {'name' : 'TÉÃM ËLÏTËS -16' , 'round1' : '' , 'round2' : '' , 'round3' : '' , 'round4' : '' ,'round5' : '' , 'round6' : '' , 'round7' : ''}
    }
    write_data(data)
    print(read_data())
