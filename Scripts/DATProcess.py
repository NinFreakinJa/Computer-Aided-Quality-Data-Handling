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
                    current[line.split("=")[0].strip()]=line.split("=")[1].strip().strip(" \"\"")
                else:
                    current[line.strip()]=OrderedDict()
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
        if(type(input[i])==OrderedDict):
            print_dict(input[i],indent+1)

def format_date(datetime):
    datetime=":".join(datetime.split(":")[1:]).strip().split(" ")
    return datetime[0]+"."+datetime[1].replace("Jan","01").replace("Feb","02").replace("Mar","03").replace("Apr","04").replace("May","05").replace("Jun","06").replace("Jul","07").replace("Aug","08").replace("Sept","09").replace("Sep","09").replace("Oct","10").replace("Nov","11").replace("Dec","12")+"."+datetime[2]+"/"+datetime[4]

# conversion is an array with the dat dictionary in index 0 and the current count of characteristics in index 1 and current converted string in index 2
def conversion(conversion):
    conversion[2]=""
    conversion[2]=conversion[2]+"K1001 "+conversion[0]["Head #Index"]["PartId"]["Data"]+"\n"+"K0004 "+conversion[0]["Date"]+"\n"
    conversion[1]=1
    for i in conversion[0]["Head #Index"]:
       if(i!="PartId" and "Data" in conversion[0]["Head #Index"][i].keys() and "Properties" in conversion[0]["Head #Index"][i].keys() and conversion[0]["Head #Index"][i]["Data"]!=""):
            conversion[2]=conversion[2]+"K0001/"+str(conversion[1])+" "+conversion[0]["Head #Index"][i]["Data"]+"\n"+"K2002/"+str(conversion[1])+" "+conversion[0]["Head #Index"][i]["Properties"]["Label_E"]+"\n"
            if(len(conversion[0]["Head #Index"][i]["Data"].split("."))>=2):
                conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" "+str(len(conversion[0]["Head #Index"][i]["Data"].split(".")[1]))+"\n"
            else:
                conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" 0\n"
            conversion[1]+=1
    conversion=conversion_helper(conversion,conversion[0])
    conversion[1]-=1
    conversion[2]="K0100 "+str(conversion[1])+"\n"+conversion[2]
    return conversion

def conversion_helper(conversion,current):
    for i in current:
        if(i!="Head #Index"):
            if(type(current[i])==OrderedDict):
                conversion=conversion_helper(conversion,current[i])
                if("Properties" in current[i].keys() and "Value" in current[i].keys()):
                    conversion[2]=conversion[2]+"K0001/"+str(conversion[1])+" "+current[i]["Value"]["Data"]+"\n"+"K2002/"+str(conversion[1])+" "+current[i]["Properties"]["Label_E"]+"\n"
                    if(len(current[i]["Value"]["Data"].split("."))>=2):
                        conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" "+str(len(current[i]["Value"]["Data"].split(".")[1]))+"\n"
                    else:
                        conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" 0\n"
                    if("LoLim" in current[i].keys()):
                        conversion[2]=conversion[2]+"K2110/"+str(conversion[1])+" "+current[i]["LoLim"]["Data"]+"\n"
                    if("UpLim" in current[i].keys()):
                        conversion[2]=conversion[2]+"K2111/"+str(conversion[1])+" "+current[i]["UpLim"]["Data"]+"\n"
                    if("Unit" in current[i].keys()):
                        conversion[2]=conversion[2]+"K2142/"+str(conversion[1])+" "+current[i]["Unit"]["Data"]+"\n"
                    conversion[1]+=1
    return conversion


def processDAT(filepath,source_path,output_path,archive_path):
    if(os.path.exists(filepath)):
        print(threading.current_thread().name,"- Processing "+filepath)
        with open(filepath, 'r+') as file:
            os.fsync(file)
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".dat",".dfq"),"wt") as file:
            #pprint.pprint(read_file(filepath), stream=file)
            file.write(conversion([read_file(filepath),0,""])[2])
            os.fsync(file)
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)