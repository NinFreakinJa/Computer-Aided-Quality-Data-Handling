import threading
import watchdogHandler


class myThread (threading.Thread):
   def __init__(self, threadID, name, watchPath):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.watchPath = watchPath
   def run(self):
        print ("Starting " + self.name)
        watchdogHandler.startWatchdog(self.name,self.watchPath,r"..\Computer-Aided-Quality-Data-Handling\Output",r"..\Computer-Aided-Quality-Data-Handling\Complete")
        print ("Exiting " + self.name)


# Create new threads
thread1 = myThread(1, "Thread-1", r"..\Computer-Aided-Quality-Data-Handling\Sample_Data")
thread2 = myThread(2, "Thread-2", r"..\Computer-Aided-Quality-Data-Handling\TestPath")

# Start new Threads
thread1.start()
thread2.start()

print ("Exiting Main Thread")