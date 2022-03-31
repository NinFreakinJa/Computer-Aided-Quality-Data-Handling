
import xmltodict
import pprint
import threading
import shutil
import os
from collections import OrderedDict

def read_file(fileName):
    try:
        with open(fileName, 'r+', encoding='utf-8') as file:
            os.fsync(file)
            my_xml = file.read()
        return xmltodict.parse(my_xml)
    except:
        return OrderedDict()

def format_date(date,time):
    datesplit=date.split("/")
    if(len(datesplit[0])==1):
        datesplit[0]="0"+datesplit[0]
    if(len(datesplit[1])==1):
        datesplit[1]="0"+datesplit[1]
    date=datesplit[1]+"."+datesplit[0]+"."+datesplit[2]
    timeOfDay=time[-2:]
    timeSplit=time[:-3].split(":")
    if(timeOfDay=="PM" and timeSplit[0]!="12"):
        timeSplit[0]=str(int(timeSplit[0])+12)
    elif(timeOfDay=="AM" and timeSplit[0]=="12"):
        timeSplit[0]="00"
    if(len(timeSplit[0])==1):
        timeSplit[0]="0"+timeSplit[0]
    return date+"/"+":".join(timeSplit)

def conversion():
    # Current string conversion
    conversion[2]=""
    conversion[2]+="K0004 "+format_date(conversion[0]["Output_Of_Fault_Code_Memory"]["Date"],conversion[0]["Output_Of_Fault_Code_Memory"]["Time"])+"\n"
    # Characteristic count
    conversion[1]=0
    # Dumped values
    conversion[3]=""
    # Head values for dump
    conversion[4]=""
    # Tail values for dump
    conversion[5]=""
    # Alternate values for characteristics
    conversion[6]=OrderedDict()

    return conversion

def processXML(filepath,source_path,output_path,archive_path):
    if(os.path.exists(filepath)):
        print(threading.current_thread().name,"- Processing "+filepath)
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".xml",".txt"),"wt") as file:
            pprint.pprint(read_file(filepath), stream=file)
            os.fsync(file)
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)