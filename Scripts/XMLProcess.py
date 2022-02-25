
import xmltodict
import pprint
import threading
import shutil
import os
from collections import OrderedDict

def read_file(fileName):
    with open(fileName, 'r+', encoding='utf-8') as file:
        os.fsync(file)
        my_xml = file.read()
    try:
        return xmltodict.parse(my_xml)
    except:
        return OrderedDict()

def processXML(filepath,source_path,output_path,archive_path):
    if(os.path.exists(filepath)):
        print(threading.current_thread().name,"- Processing "+filepath)
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".xml",".txt"),"wt") as file:
            pprint.pprint(read_file(filepath), stream=file)
            os.fsync(file)
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)