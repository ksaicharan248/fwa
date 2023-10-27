import pickle

'''
with open('userdata.pkl' , 'wb') as file :
    pickle.dump(data , file)
'''
with open('userdata.pkl' , 'rb') as file :
    data = pickle.load(file)
print(data)
