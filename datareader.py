import pickle

with open('datasheets/clan_deltails.pkl' , 'rb') as f :
    clan_data = pickle.load(f)

print(clan_data)
