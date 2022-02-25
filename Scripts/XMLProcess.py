
import xmltodict
import pprint
import threading
import shutil

def read_file(fileName):
    with open(fileName, 'r', encoding='utf-8') as file:
        my_xml = file.read()

    return xmltodict.parse(my_xml)

def processXML(filepath,source_path,output_path,archive_path):
    print(threading.current_thread().name,"- Processing "+filepath)
    with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".xml",".txt"),"wt") as file:
        pprint.pprint(read_file(filepath), stream=file)
    shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
    print(threading.current_thread().name,"- Finished Processing "+filepath)