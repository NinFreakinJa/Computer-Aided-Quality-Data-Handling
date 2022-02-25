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
            return repo
        else:
            proto = pd.read_excel(xls, 'Protokoll_Intern')
            proto.dropna(how='all', axis=1, inplace=True)
            proto.dropna(how='all', axis=0, inplace=True)
            return proto
    except:
        return pd.DataFrame()

def processExcel(filepath,source_path,output_path,archive_path):
    if(os.path.exists(filepath)):
        print(threading.current_thread().name,"- Processing "+filepath)
        with open(filepath, 'r+') as file:
            os.fsync(file)
        with open(output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,"").replace(".xlsx",".txt").replace(".xls",".txt"),"w") as file:
            file.write(read_file(filepath).to_string())
            os.fsync(file)
        shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
        print(threading.current_thread().name,"- Finished Processing "+filepath)