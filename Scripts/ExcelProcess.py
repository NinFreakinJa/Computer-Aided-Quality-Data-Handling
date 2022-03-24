import pandas as pd
import threading
import shutil
import os


def read_file(fileName):
    try:
        #Determine Excel Type
        xls = pd.ExcelFile(fileName)
        numSheets = len(xls.sheet_names)

        if numSheets == 1:
            repo = pd.read_excel(xls, 'Sum Report')
            return convertNacXls(repo)
        else:
            proto = pd.read_excel(xls, 'Protokoll_Intern')
            return convertMatXls(proto)
    except:
        return ""

def convertNacXls(xls):   
    
    #Split header and data into two dataframes
    header = xls.iloc[:10, :]
    pulse = header.iloc[8:10, :]
    data = xls.iloc[10:, :]

    #Create null test dataframe
    dfDimension = data.isna()
    
    #Count Rows
    rc = 0
    while dfDimension.iloc[rc,0] == False:
        rc+= 1 
    
    # Count Columns
    cc = 0
    while dfDimension.iloc[0,cc] == False  and dfDimension.iloc[2,cc] == False:
        cc+= 1

    #Define DFQ string
    dfq = ""

    #Add Defenite Header Info (Date/Time, Batch Name, # Characterisitics)
    dfq += "K0004 " + str(header.iloc[1,10].strftime("%d.%m.%Y")) + "/" + str(header.iloc[1,13]) + "\n"
    dfq += "K0006 " + str(header.iloc[1,1]) + "\n"
    dfq += "K0100 " + str(cc) + "\n"
    dfq += "K1001/1 " + str(data.iloc[2,0]) +"\n"
    
    #Create loop to iterate df
    for c in range (1,cc):

        #Determine characteristic name/value
        r = 0
        rp = 0
        if dfDimension.iloc[r+2,c] == False:
            dfq += "K0001/" + str(c+1) + " " + str(data.iloc[r+2,c]) + "\n"
        
            dfq += "K2002/" + str(c+1) + " " + str(data.iloc[r,c]) 
            
            #Append Qdyn pulse width/period information
            if str(data.iloc[r,c]) == "Qdyn":
                dfq += " " + str(pulse.iloc[rp,0]) + " of " + str(pulse.iloc[rp,c]) + " @ " + str(pulse.iloc[rp+1,0]) + " of " + str(pulse.iloc[rp+1,c])

            dfq += "\n"
        
            #Determine decimal places 
            if(type(data.iloc[r,c])!=str):
                if(len(str(data.iloc[r,c]).split("."))>=2):
                    dfq+="K2022/" + str(c+1) + " " + str(len(str(data.iloc[r,c]).split(".")[1])) + "\n" 
                else:
                    dfq+="K2022/" + str(c+1) + " 0\n"

            #Determine unit of measurement
            if(str(data.iloc[r+1,c])!="[-]"):
                dfq += "K2142/" + str(c+1) + " " + str(data.iloc[r+1,c]).strip("[]") + "\n"

    #For loop to dump remain
    for i in range (2,rc):
        for j in range (0,cc):
            if j != cc-1:
                dfq += str(data.iloc[i,j]) + chr(0x000f)
            else: 
                dfq += str(data.iloc[i,j]) + "\n"  
    
    #Return DFQ
    return dfq    
      
def convertMatXls(xls):   
    
    #Split header and data into two dataframes
    header = xls.iloc[:12, :]
    data = xls.iloc[13:,:]
    
    #Create null test dataframe
    dfDimension = data.isna()
    
    #Count Rows
    rc = 0
    while rc<dfDimension.shape[0] and dfDimension.iloc[rc,0] == False:
        rc+= 1 
    
    # Count Columns
    cc = 26
    # while dfDimension.iloc[0,cc] == False  and dfDimension.iloc[2,cc] == False:
    #     cc+= 1

    #Define DFQ string
    dfq = ""

    #Add Defenite Header Info (Date/Time, Batch Name, # Characterisitics)
    dfq += "K1115 " + str(header.iloc[1,2].strftime("%d.%m.%Y")) + "\n"
    dfq += "K1001 " + str(header.iloc[2,2]) + "\n"
    dfq += "K0100 " + str(cc) + "\n"
    dfq += "K1001/1 " + str(data.iloc[2,4]) +"\n"
    
    charNum=1
    #Create loop to iterate df
    for c in range (1,cc):
        #Determine characteristic name/value
        r = 0
        if dfDimension.iloc[r+2,c] == False:
            dfq += "K0001/" + str(charNum) + " " + str(data.iloc[r+2,c]) + "\n"
        
            dfq += "K2002/" + str(charNum) + " " + str(data.iloc[r,c]) + "\n"
        
            #Determine decimal places
            # if c == 1:
            #     dfq += "K2022/" + str(c+1) + " " + str(0) + "\n"
            # elif c == 4 or c == 23 or c == 24 or c== 27:
            #     dfq += "K2022/" + str(c+1) + " " + str(2) + "\n" 
            # else:
            #     dfq += "K2022/" + str(c+1) + " " + str(3) + "\n" 
            if(type(data.iloc[r,c])!=str):
                if(len(str(data.iloc[r,c]).split("."))>=2):
                    dfq+="K2022/" + str(charNum) + " " + str(len(str(data.iloc[r,c]).split(".")[1])) + "\n" 
                else:
                    dfq+="K2022/" + str(charNum) + " 0\n"

            #Determine unit of measurement
            for i in range (2,rc):
                for j in range (0,cc):
                    if(str(data.iloc[r+1,c]) == "Strahl Winkel ["+chr(0x00b0)+"]"):
                        r+=1
                        dfq += "K2142/" + str(charNum) + " " + str(data.iloc[r+1,c]).append(chr(0x00b0)) + "\n"
                    elif (str(data.iloc[r+1,c]) =="Kappa"):
                        r-=1
                        dfq += "K2142/" + str(charNum) + " " + str(data.iloc[r+1,c]).append("[%") + "\n"
                    elif str(data.iloc[r+1,c]) == "Q1":
                        r+=1
                        dfq += "K2142/" + str(charNum) + " " + str(data.iloc[r+1,c]).append("[%") + "\n"
            charNum+=1

    #For loop to dump remain
    for i in range (2,rc):
        for j in range (0,cc):
            if dfDimension.iloc[i,j]==False:
                if j != cc-1:
                    dfq += str(data.iloc[i,j]) + chr(0x000f)
                else: 
                    dfq += str(data.iloc[i,j]) + chr(0x000f) + "\n"  
    
    return dfq    


def processExcel(filepath,source_path,output_path,archive_path):
    if(os.path.exists(filepath)):
        print(threading.current_thread().name,"- Processing "+filepath)
        with open(filepath, 'r+') as file:
            os.fsync(file)
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".xlsx",".dfq").replace(".xls",".dfq"),"w") as file:
            file.write(read_file(filepath))
            os.fsync(file)
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)
