import threading
import shutil
import pprint
from collections import OrderedDict
import os

def read_file(filename):
    complete=OrderedDict()
    current=complete
    stack=[complete]
    read=False
    indentCount=0
    with open(filename, 'r') as file:
        lines=file.readlines()
        for line in lines:
            if(read):
                count=0
                for i in range(0,len(line),2):
                    if(line[i]+line[i+1]=="  "):
                        count+=1
                    else:
                        break
                if(count<indentCount):
                    for i in range(indentCount-count):
                        stack.pop()
                    if(len(stack)==0):
                        return complete
                    current=stack[-1]
                if("=" in line):
                    current[line.split("=")[0].strip()]=line.split("=")[1].strip()
                else:
                    current[line.strip()]=dict()
                    stack.append(current[line.strip()])
                    current=stack[-1]
                indentCount=count
            elif("; Date:" in line):
                current["Date"]=format_date(line)
            elif("#Index" in line):
                read=True
    return complete

def print_dict(input,indent):
    for i in input:
        print((" "*indent)+i)
        if(type(input[i])==dict):
            print_dict(input[i],indent+1)

def format_date(datetime):
    datetime=":".join(datetime.split(":")[1:]).strip()
    datetime=datetime.split(" ")
    return datetime[0]+"."+datetime[1].replace("Jan","01").replace("Feb","02").replace("Mar","03").replace("Apr","04").replace("May","05").replace("Jun","06").replace("Jul","07").replace("Aug","08").replace("Sept","09").replace("Sep","09").replace("Oct","10").replace("Nov","11").replace("Dec","12")+"."+datetime[2]+"/"+datetime[4]

def processDAT(filepath,source_path,output_path,archive_path):
    if(os.path.exists(filepath)):
        print(threading.current_thread().name,"- Processing "+filepath)
        with open(filepath, 'r+') as file:
            os.fsync(file)
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".dat",".dfq"),"wt") as file:
            #pprint.pprint(read_file(filepath), stream=file)
            os.fsync(file)
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)
