#Method to return filespaths for watchdog
from fileinput import close

def getPaths():
 
    #Set controller file
    src = "paths.txt"
    paths = []

    #Iterate through controller file
    with open(src, 'r') as file:
        #Read Lines
        lines = file.readlines()
        #Strip whitespace and append to paths list
        for i in lines:
            j = i.strip()
            paths.append(j)

            
    return paths        



