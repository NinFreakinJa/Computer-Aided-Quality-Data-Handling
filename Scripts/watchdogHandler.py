# Call each watchdog as thread
# Do an initial passthrough to check for files already in folder
# Send updates to console

import watchdog.events
import watchdog.observers
import time
import shutil

#code modified from https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self,thread_name,output_path,completed_path):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.xml','*.dat','*.dfq','*.xls'],ignore_directories=True, case_sensitive=False)
        self.output_path=output_path
        self.completed_path=completed_path
        self.thread_name=thread_name
  
    def on_created(self, event):
        print("%s - File Created - % s." %(self.thread_name,event.src_path))
        # Event is created, you can process it now
        extension=event.src_path.split('.')[-1]
        if(extension=='dfq'):
            processDFQ(event.src_path,self.output_path,self.completed_path)
        elif(extension=='xml'):
            print("XML Detected")
        elif(extension=="dat"):
            print("DAT detected")
        elif(extension=="xls"):
            print("XLS dectected")
        else:
            print("File type not supported")
        


def startWatchdog(thread_name,source_path,output_path,completed_path):
    src_path = source_path
    event_handler = Handler(thread_name,output_path,completed_path)
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    print("Watchdog "+str(thread_name)+" started at: "+source_path)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def processDFQ(filepath,output_path,completed_path):
    print("Processing "+filepath)
    shutil.copyfile(filepath,output_path+"\\"+filepath.split('\\')[-1])
    shutil.move(filepath,completed_path+"\\"+filepath.split('\\')[-1])
    print("Finished Processing "+filepath)

if __name__ == "__main__":
    startWatchdog("test",r"..\Computer-Aided-Quality-Data-Handling\Sample Data",r"..\Computer-Aided-Quality-Data-Handling\Output",r"..\Computer-Aided-Quality-Data-Handling\Complete")