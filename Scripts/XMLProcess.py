
import xmltodict
import threading
import shutil
import os
from collections import OrderedDict

# Read XML in as OrderedDict
def read_file(fileName):
    try:
        with open(fileName, 'r+', encoding='utf-8') as file:
            os.fsync(file)
            my_xml = file.read()
        return xmltodict.parse(my_xml)
    except:
        return OrderedDict()

# Formats date into correct format
def format_date(date,time):
    datesplit=date.split("/")
    #Leading zeroes
    if(len(datesplit[0])==1):
        datesplit[0]="0"+datesplit[0]
    if(len(datesplit[1])==1):
        datesplit[1]="0"+datesplit[1]
    date=datesplit[1]+"."+datesplit[0]+"."+datesplit[2]
    timeOfDay=time[-2:]
    timeSplit=time[:-3].split(":")
    # Military time
    if(timeOfDay=="PM" and timeSplit[0]!="12"):
        timeSplit[0]=str(int(timeSplit[0])+12)
    elif(timeOfDay=="AM" and timeSplit[0]=="12"):
        timeSplit[0]="00"
    if(len(timeSplit[0])==1):
        timeSplit[0]="0"+timeSplit[0]
    return date+"/"+":".join(timeSplit)

# Conversion to dfq
def conversion(conversion):
    # Current string conversion
    conversion[2]=""
    conversion[2]+="K0004 "+format_date(conversion[0]["Output_Of_Fault_Code_Memory"]["Date"],conversion[0]["Output_Of_Fault_Code_Memory"]["Time"])+"\n"
    # Characteristic count
    conversion[1]=1
    # Dumped values
    conversion[3]=""
    # Head values for dump
    conversion[4]=""
    conversion_helper(conversion,conversion[0]["Output_Of_Fault_Code_Memory"],False,"")
    # Adds line stating number of characteristics
    conversion[2]="K0100 "+str(conversion[1]-1)+"\n"+conversion[2]
    # Adds dump to file
    if(conversion[3]!=""):
        dumpCopy=conversion[3].split("\n")
        conversion[3]=""
        for i in dumpCopy:
            if(i!=""):
                conversion[3]+=conversion[4]+i+"\n"
        conversion[2]+=conversion[3]
    return conversion

def conversion_helper(conversion, current, copy,header):
    for i in current:
        if(i!="Date" and i!="Time"):
            # Further recursion or dump
            if(type(current[i])==OrderedDict):
                if(i=="FaultEntry" and copy):
                    conversion=dump(conversion,current[i])
                    conversion[3]+="\n"
                else:
                    if(i=="FaultEntry" or copy):
                        conversion=conversion_helper(conversion,current[i],True, header+i+"_")
                    else:
                        conversion=conversion_helper(conversion,current[i],False, header+i+"_")
            # Some items are read in as lists of OrderedDicts
            elif(type(current[i])==list):
                for j in range(len(current[i])):
                    # Dump after printing first
                    if(i=="FaultEntry" and j>0):
                        conversion=dump(conversion,current[i][j])
                        conversion[3]+="\n"
                    elif(type(current[i][j])==OrderedDict):
                        # Only other array of this type is Voltage
                        # This is to avoid the characteristics having the same description
                        if("Name" in current[i][j].keys() and "Value" in current[i][j].keys()):
                            conversion[2]+="K0001/"+str(conversion[1])+" "+str(current[i][j]["Value"])+"\nK2002/"+str(conversion[1])+" "+header+i+"_"+str(current[i][j]["Name"])+"\n"
                            conversion[1]+=1
                        else:
                            if(i=="FaultEntry" or copy):
                                conversion=conversion_helper(conversion,current[i][j],True, header+i+"_")
                            else:
                                conversion=conversion_helper(conversion,current[i][j],False, header+i+"_")
            # When a key-value pair, added to dfq
            elif(current[i]!="" and current[i]!=None):
                conversion[2]+="K0001/"+str(conversion[1])+" "+str(current[i])+"\nK2002/"+str(conversion[1])+" "+header+i+"\n"
                # header of dump
                if(not copy):
                    conversion[4]+=str(current[i])+chr(0x000f)
                if(i=="Hours" or i=="Minutes" or i=="Seconds" or i=="Milliseconds"):
                    conversion[2]+="K2142/"+str(conversion[1])+" "+i+"\n"
                conversion[1]+=1
    return conversion

# Same principles as above but adds to dump rather than conversion
def dump(conversion,current):
    for i in current:
        if(type(current[i])==OrderedDict):
            conversion=dump(conversion,current[i])
        elif(type(current[i])==list):
            for j in range(len(current[i])):
                if(type(current[i][j])==OrderedDict and "Name" in current[i][j].keys() and "Value" in current[i][j].keys()):
                    conversion[3]+=str(current[i][j]["Value"])+chr(0x000f)
                else:
                    conversion=dump(conversion,current[i][j])
        elif(current[i]!=""):
            conversion[3]+=current[i]+chr(0x000f)
    return conversion


def processXML(filepath,source_path,output_path,archive_path):
    if(os.path.exists(filepath)):
        print(threading.current_thread().name,"- Processing "+filepath)
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".xml",".dfq"),"wt") as file:
            file.write(conversion([read_file(filepath),1,"","",""])[2])
            os.fsync(file)
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)