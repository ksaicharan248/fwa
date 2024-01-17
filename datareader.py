import pickle

'''
with open('datasheets/userdata.pkl' , 'wb') as file :
    pickle.dump(data , file)
'''
with open('datasheets/leader_userdata.pkl' , 'rb') as file :
    data = pickle.load(file)
print(data)
