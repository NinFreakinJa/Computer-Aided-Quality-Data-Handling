import threading
import shutil
import pprint
from collections import OrderedDict
import os

# Reads the dat file into an OrderedDict based on the number of indents in the line
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
                # Counts the number of indents
                for i in range(0,len(line),2):
                    if(line[i]+line[i+1]=="  "):
                        count+=1
                    else:
                        break
                # If indent is less than previous line, will unwind the stack of dicts the appropriate amount
                if(count<indentCount):
                    for i in range(indentCount-count):
                        stack.pop()
                    if(len(stack)==0):
                        return complete
                    current=stack[-1]
                # An = in a line indicates a key value pair to be added to the current dict
                if("=" in line):
                    current[line.split("=")[0].strip()]=line.split("=")[1].strip().strip(" \"\"")
                # Otherwise it is another section header represented by another dict in the current dict
                # This dict becomes the new current dict and is added to the stack
                else:
                    current[line.strip()]=OrderedDict()
                    stack.append(current[line.strip()])
                    current=stack[-1]
                indentCount=count
            # Reads and properly formats the date
            elif("; Date:" in line):
                current["Date"]=format_date(line)
            # Where the data starts
            elif("#Index" in line):
                read=True
    return complete

# Prints out dicts recursively with imbedded dicts represented by indents
def print_dict(input,indent):
    for i in input:
        print((" "*indent)+i)
        if(type(input[i])==OrderedDict):
            print_dict(input[i],indent+1)

# Correctly formats the date in DD.MM.YYYY/HH:MM:SS
def format_date(datetime):
    datetime=":".join(datetime.split(":")[1:]).strip().split(" ")
    return datetime[0]+"."+datetime[1].replace("Jan","01").replace("Feb","02").replace("Mar","03").replace("Apr","04").replace("May","05").replace("Jun","06").replace("Jul","07").replace("Aug","08").replace("Sept","09").replace("Sep","09").replace("Oct","10").replace("Nov","11").replace("Dec","12")+"."+datetime[2]+"/"+datetime[4]

# conversion is an array with the dat dictionary in index 0 and the current count of characteristics in index 1 and current converted string in index 2 and dumped values in index 3 and head values to be copied to the dump in index 4 and tail values to be copied to the dump in index 5 and extra characteristic values in index 6
def conversion(conversion):
    # Current string conversion
    conversion[2]=""
    # Different part id locations in different formats
    alternateType=False
    if("PartId" in conversion[0]["Head #Index"].keys()):
        conversion[2]=conversion[2]+"K1001 "+conversion[0]["Head #Index"]["PartId"]["Data"]+"\n"+"K0004 "+conversion[0]["Date"]+"\n"
    else:
        conversion[2]=conversion[2]+"K1001 "+conversion[0]["MesUniqueID"]["Data"]+"\n"+"K0004 "+conversion[0]["Date"]+"\n"
        alternateType=True
    # Characteristic count
    conversion[1]=1
    # Dumped values
    conversion[3]=""
    # Head values for dump
    conversion[4]=""
    # Tail values for dump
    conversion[5]=""
    # Alternate values for characteristics
    conversion[6]=OrderedDict()
    if(not alternateType):
        # Reading in the head
        for i in conversion[0]["Head #Index"]:
            # Checks for data fields that are not null
            if(i!="PartId" and "Data" in conversion[0]["Head #Index"][i].keys() and "Properties" in conversion[0]["Head #Index"][i].keys() and conversion[0]["Head #Index"][i]["Data"]!=""):
                conversion[2]=conversion[2]+"K0001/"+str(conversion[1])+" "+conversion[0]["Head #Index"][i]["Data"]+"\n"+"K2002/"+str(conversion[1])+" "+conversion[0]["Head #Index"][i]["Properties"]["Label_E"]+"\n"
                # Adds the number of decimal points for value
                if(len(conversion[0]["Head #Index"][i]["Data"].split("."))>=2):
                    conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" "+str(len(conversion[0]["Head #Index"][i]["Data"].split(".")[1]))+"\n"
                else:
                    conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" 0\n"
                conversion[4]+=conversion[0]["Head #Index"][i]["Data"]+chr(0x000f)
                conversion[1]+=1
        # Calls recursive helper method for the rest of the file
        conversion=conversion_helper(conversion,conversion[0],True)
        # Adds line stating number of characteristics
        conversion[2]="K0100 "+str(conversion[1]-1)+"\n"+conversion[2]
        # Adds alternate values for characteristics
        split=conversion[2].split("\n")
        for i in conversion[6]:
            for j in conversion[6][i].keys():
                # Only entered if values are different
                if(type(conversion[6][i][j])==list and len(set(conversion[6][i][j]))>1):
                    for k in range(len(split)):
                        if(j+"/"+str(conversion[6][i]["CharNum"]) in split[k]):
                            split[k]=j+"/"+str(conversion[6][i]["CharNum"])+" "
                            for l in conversion[6][i][j]:
                                split[k]+=str(l)+"/"
                            break
        conversion[2]="\n".join(split)
        # Adds dump to file
        if(conversion[3]!=""):
            dumpCopy=conversion[3].split("\n")
            conversion[3]=""
            for i in dumpCopy:
                if(i!=""):
                    conversion[3]+=conversion[4]+i+conversion[5]+"\n"
            conversion[2]+=conversion[3]
    else:
        conversion=conversion_helper_alt(conversion,conversion[0],"")
        conversion[2]="K0100 "+str(conversion[1]-1)+"\n"+conversion[2]
    return conversion

# Recursive helper method for reading characteristics
# Conversion is the same as above
# Current is the current dict used
# Copy is used to determine if values are being copied for the tail of dump or not
def conversion_helper(conversion,current,copy):
    for i in current:
        if(i!="Head #Index"):
            #Determines if key is another dict to go deeper in recursion
            if(type(current[i])==OrderedDict):
                # Checks for array to create dump values instead
                if("[" in i and not "[1]" in i):
                    conversion=dump(conversion,current[i])
                    conversion[3]+="\n"
                else:
                    # Furthers recursion
                    if("[" in i or not copy):
                        conversion=conversion_helper(conversion,current[i],False)
                    else:
                        conversion=conversion_helper(conversion,current[i],True)
                    # Looking for key value pairs in the DAT file
                    if(("Properties" in current[i].keys() or not copy) and "Value" in current[i].keys()):
                        if(copy):
                            conversion[2]=conversion[2]+"K0001/"+str(conversion[1])+" "+current[i]["Value"]["Data"]+"\n"+"K2002/"+str(conversion[1])+" "+current[i]["Properties"]["Label_E"]+"\n"
                            conversion[5]+=current[i]["Value"]["Data"]+chr(0x000f)
                        else:
                            conversion[2]=conversion[2]+"K0001/"+str(conversion[1])+" "+current[i]["Value"]["Data"]+"\n"+"K2002/"+str(conversion[1])+" "+i.replace(" #Index","")+"\n"
                            conversion[6][i.replace(" #Index","")]=OrderedDict()
                            conversion[6][i.replace(" #Index","")]["CharNum"]=conversion[1]
                        # Number of decimal points
                        if(len(current[i]["Value"]["Data"].split("."))==2):
                            conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" "+str(len(current[i]["Value"]["Data"].split(".")[1]))+"\n"
                            if(not copy):
                                conversion[6][i.replace(" #Index","")]["K2022"]=[len(current[i]["Value"]["Data"].split(".")[1])]
                        else:
                            conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" 0\n"
                            if(not copy):
                                conversion[6][i.replace(" #Index","")]["K2022"]=[0]
                        # Lower limit, upper limit, and unit values
                        if("LoLim" in current[i].keys() and current[i]["LoLim"]["Data"]!=""):
                            conversion[2]=conversion[2]+"K2110/"+str(conversion[1])+" "+current[i]["LoLim"]["Data"]+"\n"
                            if(not copy):
                                conversion[6][i.replace(" #Index","")]["K2110"]=[current[i]["LoLim"]["Data"]]
                        if("UpLim" in current[i].keys() and current[i]["UpLim"]["Data"]!=""):
                            conversion[2]=conversion[2]+"K2111/"+str(conversion[1])+" "+current[i]["UpLim"]["Data"]+"\n"
                            if(not copy):
                                conversion[6][i.replace(" #Index","")]["K2111"]=[current[i]["UpLim"]["Data"]]
                        if("Unit" in current[i].keys() and current[i]["Unit"]["Data"]!=""):
                            conversion[2]=conversion[2]+"K2142/"+str(conversion[1])+" "+current[i]["Unit"]["Data"]+"\n"
                            if(not copy):
                                conversion[6][i.replace(" #Index","")]["K2142"]=[current[i]["Unit"]["Data"]]
                        conversion[1]+=1
    return conversion

def conversion_helper_alt(conversion, current, header):
    for i in current:
        if(i!="MesUniqueID"):
            #Determines if key is another dict to go deeper in recursion
            if(type(current[i])==OrderedDict):
                if("SetValue" in current[i].keys()):
                    conversion[2]=conversion[2]+"K0001/"+str(conversion[1])+" "+current[i]["SetValue"]["Data"]+"\n"+"K2002/"+str(conversion[1])+" "+header+current[i]["Properties"]["Label_E"]+"\n"
                    # Number of decimal points
                    if(len(current[i]["SetValue"]["Data"].split("."))==2):
                        conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" "+str(len(current[i]["SetValue"]["Data"].split(".")[1]))+"\n"
                    else:
                        conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" 0\n"
                    # Lower limit, upper limit, and unit values
                    if("LoLim" in current[i].keys() and current[i]["LoLim"]["Data"]!=""):
                        conversion[2]=conversion[2]+"K2110/"+str(conversion[1])+" "+current[i]["LoLim"]["Data"]+"\n"
                    if("UpLim" in current[i].keys() and current[i]["UpLim"]["Data"]!=""):
                        conversion[2]=conversion[2]+"K2111/"+str(conversion[1])+" "+current[i]["UpLim"]["Data"]+"\n"
                    if("Label2_E" in current[i]["SetValue"]["Properties"].keys()):
                        if(current[i]["SetValue"]["Properties"]["Label2_E"]==""):
                            conversion[2]=conversion[2]+"K2142/"+str(conversion[1])+" "+current[i]["SetValue"]["Properties"]["Label2_D"]+"\n"
                        else:
                            conversion[2]=conversion[2]+"K2142/"+str(conversion[1])+" "+current[i]["SetValue"]["Properties"]["Label2_E"]+"\n"
                    conversion[1]+=1                
                else:
                    if("#Index" in i):
                        if("Properties" in current[i].keys()):
                            conversion=conversion_helper_alt(conversion,current[i],header+current[i]["Properties"]["Label_E"]+"_")
                        else:
                            conversion=conversion_helper_alt(conversion,current[i],header+i.replace(" #Index","")+"_")
                    else:
                        conversion=conversion_helper_alt(conversion,current[i],header)
                    if("Properties" in current[i].keys() and "Data" in current[i].keys() and "Label_E" in current[i]["Properties"].keys()):
                        conversion[2]=conversion[2]+"K0001/"+str(conversion[1])+" "+current[i]["Data"]+"\n"+"K2002/"+str(conversion[1])+" "+header+current[i]["Properties"]["Label_E"]+"\n"
                        # Number of decimal points
                        if(len(current[i]["Data"].split("."))==2):
                            conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" "+str(len(current[i]["Data"].split(".")[1]))+"\n"
                        else:
                            conversion[2]=conversion[2]+"K2022/"+str(conversion[1])+" 0\n"
                        if("Label2_E" in current[i]["Properties"].keys()):
                            if(current[i]["Properties"]["Label2_E"]==""):
                                conversion[2]=conversion[2]+"K2142/"+str(conversion[1])+" "+current[i]["Properties"]["Label2_D"]+"\n"
                            else:
                                conversion[2]=conversion[2]+"K2142/"+str(conversion[1])+" "+current[i]["Properties"]["Label2_E"]+"\n"
                        conversion[1]+=1
    return conversion
                

# Recursive helper method for dumping values
def dump(conversion, current):
    for i in current:
        if(i!="Head #Index"):
            if(type(current[i])==OrderedDict):
                if("[" in i and not "[1]" in i):
                    conversion=dump(conversion,current[i])
                else:
                    conversion=dump(conversion,current[i])
                    # Looks for values to be dumped
                    if("Value" in current[i].keys()):
                        conversion[3]+=current[i]["Value"]["Data"]+chr(0x000f)
                        # Number of decimal points
                        if(len(current[i]["Value"]["Data"].split("."))>=2):
                            conversion[6][i.replace(" #Index","")]["K2022"].append(len(current[i]["Value"]["Data"].split(".")[1]))
                        else:
                            conversion[6][i.replace(" #Index","")]["K2022"].append(0)
                        # Lower limit, upper limit, and unit values
                        if("LoLim" in current[i].keys() and current[i]["LoLim"]["Data"]!=""):
                            conversion[6][i.replace(" #Index","")]["K2110"].append(current[i]["LoLim"]["Data"])
                        if("UpLim" in current[i].keys() and current[i]["UpLim"]["Data"]!=""):
                            conversion[6][i.replace(" #Index","")]["K2111"].append(current[i]["UpLim"]["Data"])
                        if("Unit" in current[i].keys() and current[i]["Unit"]["Data"]!=""):
                            conversion[6][i.replace(" #Index","")]["K2142"].append(current[i]["Unit"]["Data"])
                    if("[" in i):
                        conversion[3]+="\n"
    return conversion

def processDAT(filepath,source_path,output_path,archive_path):
    # Checks to see path is still valid
    if(os.path.exists(filepath)):
        # Print to user
        print(threading.current_thread().name,"- Processing "+filepath)
        # Ensures all filewriting to file is complete
        with open(filepath, 'r+') as file:
            os.fsync(file)
        # Writes new dfq file in appropriate location
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".dat",".dfq"),"wt") as file:
            #pprint.pprint(read_file(filepath), stream=file)
            # Calls the conversion method with the dict returned by the read_file method
            file.write(conversion([read_file(filepath),1,"","","","",OrderedDict()])[2])
            os.fsync(file)
        # Moves original file to archive location
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)