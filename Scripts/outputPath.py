#Output Path Creation
#Import OS Interface
import os

src = "outputPaths.txt"
outputPaths = []

#Iterate through controller file (outputPaths.txt)
with open(src, 'r') as file:
    #Read Lines
    lines = file.readlines()
    #Strip whitespace and append to paths list
    for i in lines:
        j = i.strip()
        outputPaths.append(j)


#Close controller file
file.close()

#Set path variables
path0 = outputPaths[0]
path1 = outputPaths[1]

#Convert to originalFiles path
os.chdir(path0)

#Try block for originalFiles Directory
try:
    os.mkdir('originalFiles')
except FileExistsError:
    print("Original Directory already exists.")

#Change to convertedFiles path
os.chdir(path1)

#Try block for convertedFiles Directory
try:
    os.mkdir('convertedFiles')
except FileExistsError:
    print("Converted Directory already exists.")


