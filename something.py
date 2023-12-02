import pickle

user_data = [{},{}]
with open('cwlrooster.pkl','wb') as file:
    pickle.dump(user_data,file)

'''
with open('cwlrooster.pkl','rb') as file :
    user_data= pickle.load(file)
print(user_data)'''

