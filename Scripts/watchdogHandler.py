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
        print(event.src_path)
        print(self.output_path+"\\"+event.src_path.split('\\')[-1])
        print(event.src_path[-4:])
        switch={
            '.dfq': lambda : shutil.move(event.src_path,self.output_path+"\\"+event.src_path.split('\\')[-1]),
            '.dat': "dat",
            '.xml': "xml",
            '.xls': "xls",
        }
        switch.get(event.src_path[-4:],lambda:"File not appropriate data type")


def startWatchdog(thread_name,source_path,output_path,completed_path):
    src_path = source_path
    event_handler = Handler(thread_name,output_path,completed_path)
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    print("Starting Watchdog")
    startWatchdog("test",r"C:\Users\Jared\Desktop\Random_School\Capstone\Computer-Aided-Quality-Data-Handling\Sample_Data",r"C:\Users\Jared\Desktop\Random_School\Capstone\Computer-Aided-Quality-Data-Handling\Output",r"C:\Users\Jared\Desktop\Random_School\Capstone\Computer-Aided-Quality-Data-Handling\Complete")