# Call each watchdog as thread
# Do an initial passthrough to check for files already in folder
# Send updates to console

import watchdog.events
import watchdog.observers
import time
import shutil
from getPaths import checkPathExists

#code modified from https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self,thread_name,source_path,output_path,archive_path):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.xml','*.dat','*.dfq','*.xls'],ignore_directories=False, case_sensitive=False)
        self.output_path=output_path
        self.archive_path=archive_path
        self.thread_name=thread_name
        self.source_path = source_path
  
    def on_created(self, event):
        print("%s - File Created - % s." %(self.thread_name,event.src_path))
        checkPathExists("\\".join(event.src_path.split("\\")[:-1]),self.source_path,self.output_path,self.archive_path)
        # Event is created, you can process it now
        extension=event.src_path.split('.')[-1]
        if(extension=='dfq'):
            processDFQ(event.src_path,self.source_path,self.output_path,self.archive_path)
        elif(extension=='xml'):
            print("XML Detected")
        elif(extension=="dat"):
            print("DAT detected")
        elif(extension=="xls"):
            print("XLS dectected")
        else:
            print("File type not supported")

# Initiallization for watchdog
def startWatchdog(thread_name,source_path,output_path,archive_path):
    src_path = source_path
    event_handler = Handler(thread_name,source_path,output_path,archive_path)
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

# DFQ is copied to output path and original file is moved to archive path
def processDFQ(filepath,source_path,output_path,archive_path):
    print("Processing "+filepath)
    shutil.copyfile(filepath,output_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
    shutil.move(filepath,archive_path+"\\"+source_path.split("\\")[-1]+filepath.replace(source_path,""))
    print("Finished Processing "+filepath)