# Call each watchdog as thread
# Do an initial passthrough to check for files already in folder
# Send updates to console

import watchdog.events
import watchdog.observers
import time

#code modified from https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.xml','*.dat','*.dfq','*.xls'],ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
        print("File Created - % s." % event.src_path)
        # Event is created, you can process it now


def startWatchdog(source_path,output_path,completed_path):
    src_path = source_path
    event_handler = Handler()
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
    startWatchdog(r"..\Computer-Aided-Quality-Data-Handling\Sample Data",r"..\Computer-Aided-Quality-Data-Handling\Output",r"..\Computer-Aided-Quality-Data-Handling\Complete")