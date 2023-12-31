import pickle

'''
with open('userdata.pkl' , 'wb') as file :
    pickle.dump(data , file)
'''
with open('leader_userdata.pkl' , 'rb') as file :
    data = pickle.load(file)
print(data)
