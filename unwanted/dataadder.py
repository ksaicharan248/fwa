import pickle

with open('datasheets/userdata.pkl' , 'rb') as f :
    token = pickle.load(f)

for user in token.keys() :
    data = token[user]
    token[user]['tag'] = data['tag'].strip('#')
    token[user]['clan'] = data['clan'].strip('#')

with open("datasheets/userdata.pkl" , "wb") as file :
    pickle.dump(token , file)

with open('datasheets/userdata.pkl' , 'rb') as f :
    data = pickle.load(f)

print(data)
