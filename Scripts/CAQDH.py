# Main File

import threading
import watchdogHandler
import getPaths
import os

if __name__ == "__main__":
    paths=getPaths.getPaths_JSON()
    threads=[]
    for i in range(len(paths["input_paths"])):
        threads.append(threading.Thread(target=watchdogHandler.startWatchdog,args=(i,paths["input_paths"][i],paths["output_path"],paths["completed_path"])))
    for i in threads:
        i.start()
    for i in paths["input_paths"]:
        for root, dirs, files in os.walk(i):
            for name in files:
                extension=name.split('.')[-1]
                if(extension=='dfq'):
                    watchdogHandler.processDFQ(os.path.join(root, name),paths["output_path"],paths["completed_path"])
                elif(extension=='xml'):
                    print("XML Detected: "+os.path.join(root, name))
                elif(extension=="dat"):
                    print("DAT detected: "+os.path.join(root, name))
                elif(extension=="xls"):
                    print("XLS dectected: "+os.path.join(root, name))
    for i in threads:
        i.join()