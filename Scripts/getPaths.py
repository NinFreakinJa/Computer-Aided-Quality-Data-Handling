#Method to return filespaths for watchdog
import json
import os

def getPaths_JSON():
    src="pathsConfig.json"
    paths=dict()
    with open(src, 'r') as file:
        paths=json.load(file)
    for i in paths["paths"]:
        for j in i["input_paths"]:
            try:
                os.mkdir(j)
                print("Created Directory: "+j)
            except FileExistsError:
                print("Located Directory: "+j)
        try:
            os.mkdir(i["output_path"])
            print("Created Directory: "+i["output_path"])
        except FileExistsError:
            print("Located Directory: "+i["output_path"])
        try:
            os.mkdir(i["archive_path"])
            print("Created Directory: "+i["archive_path"])
        except FileExistsError:
            print("Located Directory: "+i["archive_path"])
    return(paths)