import pickle

with open("ex.pkl" , "rb") as file :
    user_data = pickle.load(file)

print(user_data)
