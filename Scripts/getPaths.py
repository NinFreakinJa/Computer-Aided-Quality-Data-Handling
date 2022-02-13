#Method to return filespaths for watchdog
import json
import os

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
        os.mkdir(paths["archive_path"])
        print("Created Directory: "+paths["archive_path"])
    except FileExistsError:
        print("Located Directory: "+paths["archive_path"])
    return(paths)