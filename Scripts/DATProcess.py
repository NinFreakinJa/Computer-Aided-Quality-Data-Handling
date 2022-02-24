import threading
import shutil

def read_file(filename):
    complete=dict()
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
            elif("Date" in line):
                current["Date"]=":".join(line.split(":")[1:]).strip()
            elif("#Index" in line):
                read=True
    return complete

def print_dict(input,indent):
    for i in input:
        print((" "*indent)+i)
        if(type(input[i])==dict):
            print_dict(input[i],indent+1)

def processDAT(filepath,source_path,output_path,archive_path):
    print(threading.current_thread().name,"- Processing "+filepath)
    with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""),"w") as file:
        file.write(str(read_file(filepath)))
    shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
    print(threading.current_thread().name,"- Finished Processing "+filepath)

if __name__ == "__main__":
    file=read_file("..\\Sample Data\\5551511305C2106151272004_07-20-54.dat")
    print_dict(file,0)
    #print(file)

