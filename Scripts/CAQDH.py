# Main File

import threading
import watchdogHandler

if __name__ == "__main__":
    watchPaths=[r"..\Computer-Aided-Quality-Data-Handling\Sample Data",r"..\Computer-Aided-Quality-Data-Handling\TestPath"]
    output_path=r"..\Computer-Aided-Quality-Data-Handling\Output"
    completed_path=r"..\Computer-Aided-Quality-Data-Handling\Complete"
    threads=[]
    for i in range(len(watchPaths)):
        threads.append(threading.Thread(target=watchdogHandler.startWatchdog,args=(i,watchPaths[i],output_path,completed_path)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()