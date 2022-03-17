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
            repo.dropna(how='all', axis=1, inplace=True)
            repo.dropna(how='all', axis=0, inplace=True)
            return convertNacXls(repo)
        else:
            proto = pd.read_excel(xls, 'Protokoll_Intern')
            proto.dropna(how='all', axis=1, inplace=True)
            proto.dropna(how='all', axis=0, inplace=True)
            return proto.to_string()
    except:
        return ""

def convertNacXls(xls):
#Prepare dataframe for conversion    
    
    #Split header and data into two dataframes
    header = xls.iloc[:10, :28]
    data = xls.iloc[10:18,:28]
    
    #Define DFQ string
    dfq = ""

    #Add Defenite Header Info (Date/Time, Batch Name, # Characterisitics)
    dfq += "K0004 " + str(header.iloc[1,10]) + "\n"
    dfq += "K0006 " + str(header.iloc[1,1]) + "\n"
    dfq += "K0100 " + str(28) + "\n"
    dfq += "K1001/1 " + str(data.iloc[2,0]) +"\n"
    

    #Create loop to iterate df
    for c in range (1,28):
        #Determine characteristic name/value
        r = 0
        dfq += "K0001/" + str(c+1) + " " + str(data.iloc[r+2,c]) + "\n"
        
        dfq += "K2002/" + str(c+1) + " " + str(data.iloc[r,c]) + "\n"
        
        #Determine decimal places
        if c == 1:
            dfq += "K2022/" + str(c+1) + " " + str(0) + "\n"
        elif c == 4 or c == 23 or c == 24 or c== 27:
            dfq += "K2022/" + str(c+1) + " " + str(2) + "\n" 
        else:
            dfq += "K2022/" + str(c+1) + " " + str(3) + "\n" 

        #Determine unit of measurement
        if(str(data.iloc[r+1,c])!="[-]"):
            dfq += "K2142/" + str(c+1) + str(data.iloc[r+1,c]).strip("[]")

    #For loop to dump remain
    for i in range (2,8):
        for j in range (0,28):
            if j != 27:
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
