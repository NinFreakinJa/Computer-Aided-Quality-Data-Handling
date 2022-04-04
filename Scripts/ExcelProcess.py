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
            proto.dropna(how='all', axis=1, inplace=True)
            proto.dropna(how='all', axis=0, inplace=True)
            return convertMatXls(proto)
    except:
        return "Error converting file"

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
    dfq += "K0100 " + str(cc) + "\n"
    dfq += "K0004 " + str(header.iloc[1,10].strftime("%d.%m.%Y")) + "/" + str(header.iloc[1,13]) + "\n"
    dfq += "K0006 " + str(header.iloc[1,1]) + "\n"
    dfq += "K1001/1 " + str(data.iloc[2,0]) +"\n"
    
    #Create loop to iterate df
    for c in range (1,cc):

        #Determine characteristic name/value
        r = 0
        rp = 0
        if dfDimension.iloc[r+2,c] == False:
            dfq += "K0001/" + str(c+1) + " " + str(data.iloc[r+2,c]) + "\n"
        
            dfq += "K2002/" + str(c+1) + " " + str(data.iloc[r,c]) 
            
            #Append Qdyn/Qstat pulse width/period information
            if str(data.iloc[r,c]) == "Qdyn" or str(data.iloc[r,c]) == "Qstat" :
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
    header = xls.iloc[:11, :]
    data = xls.iloc[11:,:]
    header=header.dropna(how='all', axis=1).copy()
    header=header.dropna(how='all', axis=0).copy()
    data =data.dropna(how='all', axis=1).copy()
    data =data.dropna(how='all', axis=0).copy()
    #Create null test dataframe
    dfDimension = data.isna()
    #Create null test dataframe
    dfDimension = data.isna()
    headDimension = header.isna()
    #Count Rows
    rc = 0
    while rc<dfDimension.shape[0] and dfDimension.iloc[rc,0] == False:
        rc+= 1 
    
    # Count Columns
    cc = 0
    while cc<dfDimension.shape[1] and dfDimension.iloc[0,cc] == False:
        cc+= 1
    #Define DFQ string
    dfq = ""

    #Add Defenite Header Info (Date/Time, Batch Name, # Characterisitics)
    dfq += "K0100 " + str(cc) + "\n"
    dfq += "K1115 " + str(header.iloc[0,2].strftime("%d.%m.%Y")) + "\n"
    dfq += "K1001 " + str(header.iloc[1,2]) + "\n"
    
    charNum=1
    titleC=0
    #Create loop to iterate df
    for c in range (0,cc):
        #Determine characteristic name/value
        r = 0
        if dfDimension.iloc[r,c] == False:
            dfq += "K0001/" + str(charNum) + " " + str(data.iloc[r,c]) + "\n"

            # Determine Characteristic Name
            while(headDimension.iloc[-1,titleC] and headDimension.iloc[-2,titleC]):
                titleC+=1
            if(not headDimension.iloc[-1,titleC]):
                dfq += "K2002/" + str(charNum) + " " + str(header.iloc[-1,titleC]).replace("\n"," ") + "\n"
            else:
                titleCC=titleC
                while titleCC>=0:
                    if(not headDimension.iloc[-2,titleCC]):
                        dfq += "K2002/" + str(charNum) + " " + str(header.iloc[-2,titleCC]).replace("\n"," ") + "\n"
                        break
                    else:
                        titleCC-=1
        
            #Determine decimal places

            if(type(data.iloc[r,c])!=str):
               if(len(str(data.iloc[r,c]).split("."))>=2):
                   dfq+="K2022/" + str(charNum) + " " + str(len(str(data.iloc[r,c]).split(".")[1])) + "\n" 
               else:
                   dfq+="K2022/" + str(charNum) + " 0\n"

            #Determine unit of measurement

            for i in range(titleC,0,-1):
                if(not headDimension.iloc[-2,i]):
                    if("[" in header.iloc[-2,i]):
                        dfq += "K2142/" + str(charNum) + " " + str(header.iloc[-2,i])[str(header.iloc[-2,i]).find("[")+1:str(header.iloc[-2,i]).find("]")] + "\n"
                    break
            charNum+=1
            titleC+=1

    #For loop to dump remain
    for i in range (1,rc):
        for j in range (0,cc):
            if not dfDimension.iloc[i,j]:
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
        
