#Output Path Creation
#Import OS Interface
import os

path0 = input("Specify folder location for original files:")
path1 = input("Specify folder location for processed files:")

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


