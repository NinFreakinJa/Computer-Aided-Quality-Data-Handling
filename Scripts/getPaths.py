#Method to return filespaths for watchdog
import json
import os
import threading

# Creates the structure for the inputted filepath iteratively
def createFileStructure(filepath):
    structure=filepath.split("\\")
    for i in range(1,len(structure)+1):
        if((not os.path.exists("\\".join(structure[:i]))) and structure[i-1]!=".." and (not ":" in structure[i-1])):
            try:
                os.mkdir("\\".join(structure[:i]))
                print(threading.current_thread().name,"- Created Directory: "+"\\".join(structure[:i]))
            except:
                print(threading.current_thread().name,"- Could not create directory: "+"\\".join(structure[:i]))

# Checks that file structure exists in archive and output folders to support new file
def checkPathExists(file_path,source_path,output_path,archive_path):
    createFileStructure(archive_path+"\\"+source_path.split("\\")[-1]+file_path.replace(source_path,""))
    createFileStructure(output_path+"\\"+source_path.split("\\")[-1]+file_path.replace(source_path,""))

# Gets paths from the pathsConfig.json
def getPaths_JSON():
    src="pathsConfig.json"
    paths=dict()
    with open(src, 'r') as file:
        paths=json.load(file)
    # Structure of pathsConfig.json is an array "paths" of dictionaries with objects "ouput_path", "archive_path", and array "input_paths"
    for i in paths["paths"]:
        for j in i["input_paths"]:
            createFileStructure(j)
        createFileStructure(i["output_path"])
        createFileStructure(i["archive_path"])
    return(paths)