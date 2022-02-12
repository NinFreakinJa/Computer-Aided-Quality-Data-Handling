# Main File

import threading
import watchdogHandler
import getPaths
import os

def initial_pass(paths):
    for i in paths["input_paths"]:
        for root, dirs, files in os.walk(i):
            for name in files:
                watchdogHandler.checkPathExists(os.path.join(root,name),i,paths["output_path"],paths["archive_path"])
                extension=name.split('.')[-1]
                if(extension=='dfq'):
                    watchdogHandler.processDFQ(os.path.join(root, name),i,paths["output_path"],paths["archive_path"])
                elif(extension=='xml'):
                    print("XML Detected: "+os.path.join(root, name))
                elif(extension=="dat"):
                    print("DAT detected: "+os.path.join(root, name))
                elif(extension=="xls"):
                    print("XLS dectected: "+os.path.join(root, name))

if __name__ == "__main__":
    paths=getPaths.getPaths_JSON()
    threads=[]
    for i in range(len(paths["input_paths"])):
        threads.append(threading.Thread(target=watchdogHandler.startWatchdog,args=(i,paths["input_paths"][i],paths["output_path"],paths["archive_path"])))
    for i in threads:
        i.start()
    initial_pass(paths)
    for i in threads:
        i.join()

