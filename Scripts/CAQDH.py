# Main File

import threading
import watchdogHandler
import getPaths

if __name__ == "__main__":
    paths=getPaths.getPaths_JSON()
    threads=[]
    for i in range(len(paths["input_paths"])):
        threads.append(threading.Thread(target=watchdogHandler.startWatchdog,args=(i,paths["input_paths"][i],paths["output_path"],paths["completed_path"])))
    for i in threads:
        i.start()
    for i in threads:
        i.join()