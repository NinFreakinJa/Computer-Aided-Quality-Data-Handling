

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
            elif("#Index" in line):
                read=True
    return complete

if __name__ == "__main__":
    print(read_file("..\\Sample Data\\5551511305C2106151272004_07-20-54.dat").keys())

