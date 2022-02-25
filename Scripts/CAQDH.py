# Main File

import threading
import watchdogHandler
import getPaths
import os
import DATProcess
import ExcelProcess
import XMLProcess

# Goes through input folders and processes any files already there.
def initial_pass(paths):
    for i in paths["paths"]:
        for j in i["input_paths"]:
            for root, dirs, files in os.walk(j):
                for name in files:
                    extension=name.split('.')[-1]
                    if(extension=='dfq'):
                        getPaths.checkPathExists(root,j,i["output_path"],i["archive_path"])
                        watchdogHandler.processDFQ(os.path.join(root, name),j,i["output_path"],i["archive_path"])
                    elif(extension=='xml'):
                        getPaths.checkPathExists(root,j,i["output_path"],i["archive_path"])
                        XMLProcess.processXML(os.path.join(root, name),j,i["output_path"],i["archive_path"])
                    elif(extension=="dat"):
                        getPaths.checkPathExists(root,j,i["output_path"],i["archive_path"])
                        DATProcess.processDAT(os.path.join(root, name),j,i["output_path"],i["archive_path"])
                    elif(extension=="xls" or extension=="xlsx"):
                        getPaths.checkPathExists(root,j,i["output_path"],i["archive_path"])
                        ExcelProcess.processExcel(os.path.join(root, name),j,i["output_path"],i["archive_path"])

if __name__ == "__main__":
    paths=getPaths.getPaths_JSON()
    threads=[]
    # Starts a watchdog at each input folder
    for i in paths["paths"]:
        for j in range(len(i["input_paths"])):
            threads.append(threading.Thread(target=watchdogHandler.startWatchdog,args=(i["input_paths"][j],i["output_path"],i["archive_path"])))
    for i in threads:
        i.start()
    initial_pass(paths)
    for i in threads:
        i.join()

