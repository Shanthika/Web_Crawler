import os

filename=os.listdir("./static")
print(filename)
rm_file="./static/"+filename[0]
os.system('rm '+rm_file)

filename=os.listdir("./static")
print(filename)