# Main File

import threading
import watchdogHandler
import getPaths
import os

# Goes through input folders and processes any files already there.
def initial_pass(paths):
    for i in paths["paths"]:
        for j in i["input_paths"]:
            for root, dirs, files in os.walk(j):
                for name in files:
                    getPaths.checkPathExists(root,j,i["output_path"],i["archive_path"])
                    extension=name.split('.')[-1]
                    if(extension=='dfq'):
                        watchdogHandler.processDFQ(os.path.join(root, name),j,i["output_path"],i["archive_path"])
                    elif(extension=='xml'):
                        print("XML Detected: "+os.path.join(root, name))
                    elif(extension=="dat"):
                        print("DAT detected: "+os.path.join(root, name))
                    elif(extension=="xls"):
                        print("XLS dectected: "+os.path.join(root, name))

if __name__ == "__main__":
    paths=getPaths.getPaths_JSON()
    threads=[]
    threadcount=0
    # Starts a watchdog at each input folder
    for i in paths["paths"]:
        for j in range(len(i["input_paths"])):
            threads.append(threading.Thread(target=watchdogHandler.startWatchdog,args=(threadcount,i["input_paths"][j],i["output_path"],i["archive_path"])))
            threadcount+=1
    for i in threads:
        i.start()
    initial_pass(paths)
    for i in threads:
        i.join()

