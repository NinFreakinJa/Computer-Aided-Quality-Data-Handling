#Method to return filespaths for watchdog
import json
import os

def getPaths():
 
    #Set controller file
    src = "watchDogPaths.txt"
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



def getPaths_JSON():
    src="pathsConfig.json"
    paths=dict()
    with open(src, 'r') as file:
        paths=json.load(file)
    for i in paths["input_paths"]:
        try:
            os.mkdir(i)
            print("Created Directory: "+i)
        except FileExistsError:
            print("Located Directory: "+i)
    try:
        os.mkdir(paths["output_path"])
        print("Created Directory: "+paths["output_path"])
    except FileExistsError:
        print("Located Directory: "+paths["output_path"])
    try:
        os.mkdir(paths["completed_path"])
        print("Created Directory: "+paths["completed_path"])
    except FileExistsError:
        print("Located Directory: "+paths["completed_path"])
    return(paths)